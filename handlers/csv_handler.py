import logging
import os
import pandas as pd

COLUMNS = [
    "id",
    "categoria",
    "sub_categoria",
    "identifier",
    "created_at",
    "text",
    "sentiment_llm",
    "llm_reason",
    "llm_model",
    "llm_prompt_version",
    "llm_classified_at",
    "lang",
    "has_irony",
    "mixed",
    "discarded",
    "discard_reason",
    "source_type",
    "robertuito_sentiment",
]


class CSVHandler:
    def __init__(self, file_path):
        self.file_path = file_path
        self.csv = self.read_csv()

    def read_csv(self):
        if not os.path.exists(self.file_path):
            return pd.DataFrame(columns=COLUMNS)
        try:
            df = pd.read_csv(self.file_path, dtype=object)
            return df.reindex(columns=[*df.columns, *[c for c in COLUMNS if c not in df.columns]], fill_value="")
        except Exception as e:
            logging.exception("Error al leer el CSV: %s", self.file_path)
            return pd.DataFrame(columns=COLUMNS)

    def get_header(self):
        if self.csv is not None:
            return self.csv.columns.tolist()
        return []

    def add_row(self, row_data):
        added = self.add_rows([row_data])
        return added[0] if added else None

    def add_rows(self, rows_data):
        """Dedupe y append batch. Devuelve las filas efectivamente agregadas."""
        if not rows_data:
            return []

        existing = set(self.csv["id"].astype(str)) if "id" in self.csv.columns else set()
        added = []
        for row in rows_data:
            rid = str(row["id"])
            if rid in existing:
                continue
            existing.add(rid)
            added.append(row)

        if added:
            self.csv = pd.concat(
                [self.csv, pd.DataFrame(added, columns=COLUMNS)],
                ignore_index=True,
            )
        return added

    def update_rows(self, rows_data, meta=None):
        """Upsert por id. Si el id existe, pisa solo las columnas presentes en el
        dict; si no existe, agrega la fila al final. categoria/sub_categoria se
        rellenan desde `meta` (dict id -> {categoria, sub_categoria}) SOLO cuando
        la celda esta vacia (nunca pisa una categoria existente). Devuelve las
        posiciones afectadas."""
        if not rows_data or "id" not in self.csv.columns:
            return []

        meta = meta or {}
        ids = self.csv["id"].astype(str)
        updated = []
        for row in rows_data:
            matches = self.csv.index[ids == str(row["id"])]
            if len(matches) == 0:
                new_row = {col: row.get(col, "") for col in self.csv.columns}
                self.csv = pd.concat(
                    [self.csv, pd.DataFrame([new_row], columns=self.csv.columns)],
                    ignore_index=True,
                )
                ids = self.csv["id"].astype(str)
                idx = self.csv.index[-1]
            else:
                idx = matches[0]
                for col, value in row.items():
                    if col in self.csv.columns:
                        self.csv.at[idx, col] = value
            info = meta.get(row["id"]) or meta.get(str(row["id"])) or {}
            for col, value in info.items():
                if value is not None and col in self.csv.columns:
                    current = self.csv.at[idx, col]
                    if pd.isna(current) or current == "":
                        self.csv.at[idx, col] = value
            updated.append(self.csv.index.get_loc(idx))
        return updated

    def save_csv(self):
        if self.csv is None:
            return
        self.csv.to_csv(self.file_path, index=False)

    def get_rows(self):
        if self.csv is not None:
            return self.csv.values.tolist()
        return []
