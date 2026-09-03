import logging

from .csv_handler import CSVHandler, COLUMNS


logger = logging.getLogger(__name__)


class SheetCsvHandler:
    def __init__(self, sheet_id, csv_file="corpus.csv"):
        self.csv_handler = CSVHandler(csv_file)
        self.sheet_client = self._create_sheet_client(sheet_id)
        self.sheets_enabled = self.sheet_client is not None

        # Cuántas filas de datos están ya en el sheet remoto.
        # Se actualiza en sync_sheet_to_csv y en add_tweets.
        self._synced_rows = len(self.csv_handler.csv)

    @staticmethod
    def _create_sheet_client(sheet_id):
        try:
            from .google_sheets import GoogleSheetsClient

            return GoogleSheetsClient(sheet_id)
        except Exception as e:
            logger.warning(
                "Google Sheets deshabilitado (modo solo CSV local): %s",
                e,
            )
            return None

    def _has_sheet_client(self):
        return self.sheets_enabled and self.sheet_client is not None

    def sync_sheet_to_csv(self):
        """Baja la hoja completa al CSV local. Costoso — ejecutar solo al
        iniciar el proceso o cuando se sospecha drift."""
        if not self._has_sheet_client():
            return
        self.sheet_client.download_sheet_as_csv(self.csv_handler.file_path)
        self.csv_handler.csv = self.csv_handler.read_csv()
        self._synced_rows = len(self.csv_handler.csv)

    def sync_csv_to_sheet(self):
        """Sube el CSV local completo (rewrite). Solo para usos puntuales."""
        self.csv_handler.save_csv()
        if not self._has_sheet_client():
            return
        self.sheet_client.upload_csv_to_sheet(self.csv_handler.file_path)
        self._synced_rows = len(self.csv_handler.csv)

    def update_tweet(self, tweet, **extra_fields):
        return self.update_tweets([tweet], **extra_fields)

    def update_tweets(self, tweets, meta=None, **extra_fields):
        """Update in place (por id) del CSV local + push de esas mismas filas
        al sheet. `tweets` son PostSchema/PostUpdateSchema (deben traer id).
        `meta` (dict id -> {categoria, sub_categoria}) solo se usa para rellenar
        las filas nuevas; las existentes conservan su categoria."""
        rows = [{**tweet.model_dump(mode="json"), **extra_fields} for tweet in tweets]
        updated = self.csv_handler.update_rows(rows, meta=meta)
        if updated:
            self.csv_handler.save_csv()

        if not self._has_sheet_client() or not updated:
            return updated

        for pos in updated:
            record = (
                self.csv_handler.csv.iloc[[pos]]
                .reindex(columns=COLUMNS, fill_value="")
                .fillna("")
                .to_dict("records")[0]
            )
            row = [str(record.get(col, "")) for col in COLUMNS]
            self.sheet_client.append_rows([row], pos + 2)  # +1 header, +1 1-based
        return updated

    def add_tweet(self, tweet, **extra_fields):
        return self.add_tweets([tweet], **extra_fields)

    def add_tweets(self, tweets, **extra_fields):
        """Dedupe + persistir local + append solo de las filas nuevas al sheet.

        `tweets` son PostSchema. `extra_fields` (p. ej. categoria/sub_categoria)
        se agregan igual a cada fila del lote.
        """
        rows = [{**tweet.model_dump(mode="json"), **extra_fields} for tweet in tweets]
        added = self.csv_handler.add_rows(rows)
        if added:
            self.csv_handler.save_csv()

        if not self._has_sheet_client():
            return added

        csv_len = len(self.csv_handler.csv)
        if self._synced_rows > csv_len:
            self._synced_rows = csv_len

        pending_df = self.csv_handler.csv.iloc[self._synced_rows :]
        if pending_df.empty:
            return added

        pending_records = (
            pending_df
            .reindex(columns=COLUMNS, fill_value="")
            .fillna("")
            .to_dict("records")
        )
        rows = [[str(row.get(col, "")) for col in COLUMNS] for row in pending_records]
        if self._synced_rows == 0:
            # Sheet vacío: escribimos el header (COLUMNS) en la fila 1 antes de los datos.
            rows = [list(COLUMNS)] + rows
            start_row = 1
        else:
            start_row = self._synced_rows + 2  # +1 por header, +1 por 1-based
        self.sheet_client.append_rows(rows, start_row)
        self._synced_rows += len(pending_records)
        return added
