import pandas as pd
import ezsheets
import os
import time
from pathlib import Path


def _resolve_credentials_file() -> str | None:
    """Resuelve el archivo de credenciales de Google Sheets.

    Prioridad:
    1) GOOGLE_SHEETS_CREDENTIALS_FILE
    2) EZSHEETS_CREDENTIALSFILENAME
    3) credentials-sheets.json en la raíz del proyecto
    """
    env_candidate = os.getenv("GOOGLE_SHEETS_CREDENTIALS_FILE") or os.getenv("EZSHEETS_CREDENTIALSFILENAME")
    if env_candidate:
        path = Path(env_candidate).expanduser()
        if not path.is_absolute():
            path = Path.cwd() / path
        if path.exists():
            return str(path)
        return None

    default_path = Path.cwd() / "credentials-sheets.json"
    if default_path.exists():
        return str(default_path)
    return None


def _iter_exception_chain(exc: BaseException):
    seen: set[int] = set()
    stack: list[BaseException | None] = [exc]
    while stack:
        current = stack.pop()
        if current is None:
            continue
        key = id(current)
        if key in seen:
            continue
        seen.add(key)
        yield current
        stack.append(getattr(current, "__cause__", None))
        stack.append(getattr(current, "__context__", None))
        for arg in getattr(current, "args", ()):
            if isinstance(arg, BaseException):
                stack.append(arg)


def _is_transient_network_error(exc: BaseException) -> bool:
    transient_winerrors = {10053, 10054, 10060}
    transient_markers = (
        "winerror 10053",
        "winerror 10054",
        "winerror 10060",
        "connection aborted",
        "connection reset",
        "timed out",
        "timeout",
        "temporarily unavailable",
        "broken pipe",
    )

    for error in _iter_exception_chain(exc):
        if getattr(error, "winerror", None) in transient_winerrors:
            return True
        msg = str(error).lower()
        if any(marker in msg for marker in transient_markers):
            return True

    return False


class GoogleSheetsClient:
    def __init__(self, sheet_id):
        self.sheet_id = sheet_id
        self.max_retries = self._read_int_env("GOOGLE_SHEETS_MAX_RETRIES", 3)
        self.retry_backoff_seconds = self._read_float_env("GOOGLE_SHEETS_RETRY_BACKOFF_SECONDS", 1.0)
        credentials_file = _resolve_credentials_file()
        if not credentials_file:
            cwd = Path.cwd()
            raise FileNotFoundError(
                "No se encontró el archivo de credenciales de Google Sheets. "
                f"Esperado en: {cwd / 'credentials-sheets.json'}. "
                "Descárgalo desde Google Cloud OAuth client credentials "
                "y guárdalo con ese nombre, o define la variable de entorno "
                "GOOGLE_SHEETS_CREDENTIALS_FILE con la ruta correcta."
            )

        # ezsheets usa esta variable para ubicar el archivo de credenciales OAuth.
        os.environ["EZSHEETS_CREDENTIALSFILENAME"] = credentials_file
        self._connect_sheet()

    @staticmethod
    def _read_int_env(var_name: str, default: int) -> int:
        value = os.getenv(var_name)
        if not value:
            return default
        try:
            parsed = int(value)
            return max(1, parsed)
        except (TypeError, ValueError):
            return default

    @staticmethod
    def _read_float_env(var_name: str, default: float) -> float:
        value = os.getenv(var_name)
        if not value:
            return default
        try:
            parsed = float(value)
            return max(0.1, parsed)
        except (TypeError, ValueError):
            return default

    def _connect_sheet(self):
        self.sheet = ezsheets.Spreadsheet(self.sheet_id)

    def _run_with_retries(self, operation_name: str, action):
        last_error = None
        for attempt in range(1, self.max_retries + 1):
            try:
                return action()
            except Exception as e:
                last_error = e
                should_retry = _is_transient_network_error(e) and attempt < self.max_retries
                if not should_retry:
                    raise

                print(
                    f"⚠️ {operation_name} falló (intento {attempt}/{self.max_retries}): {e}. "
                    "Reintentando..."
                )
                try:
                    self._connect_sheet()
                except Exception:
                    pass
                time.sleep(self.retry_backoff_seconds * (2 ** (attempt - 1)))

        if last_error is not None:
            raise last_error

    def get_sheet(self):
        return self.sheet

    def download_sheet_as_csv(self, output_file):
        self._run_with_retries(
            "Descarga de Google Sheets",
            lambda: self.sheet.downloadAsCSV(output_file),
        )
        self.csv_file = output_file

    def upload_csv_to_sheet(self, file_path=None):
        """Rewrite completo de la primera hoja desde el CSV. Costoso —
        úsalo solo para sync inicial o para forzar consistencia."""
        file_path = file_path or getattr(self, "csv_file", None)
        if not file_path:
            return
        csv = pd.read_csv(file_path).fillna("")
        rows = [csv.columns.tolist()] + csv.astype(str).values.tolist()

        def _upload_rows():
            ws = self.sheet[0]
            self._ensure_capacity(ws, len(rows), len(csv.columns))
            ws.updateRows(rows)

        self._run_with_retries("Subida completa a Google Sheets", _upload_rows)

    def append_rows(self, rows, start_row):
        """Escribe `rows` (lista 2D de str) empezando en la fila 1-based
        `start_row`. Usado para agregar solo las filas nuevas sin reescribir
        el sheet entero."""
        if not rows:
            return

        def _append_rows():
            ws = self.sheet[0]
            self._ensure_capacity(ws, start_row + len(rows) - 1, len(rows[0]))
            ws.updateRows(rows, startRow=start_row)

        self._run_with_retries("Append de filas en Google Sheets", _append_rows)

    @staticmethod
    def _ensure_capacity(ws, needed_rows, needed_cols):
        """ezsheets no auto-redimensiona al escribir fuera del rango asignado."""
        new_rows = max(ws.rowCount, needed_rows)
        new_cols = max(ws.columnCount, needed_cols)
        if new_rows != ws.rowCount or new_cols != ws.columnCount:
            ws.resize(rowCount=new_rows, columnCount=new_cols)
