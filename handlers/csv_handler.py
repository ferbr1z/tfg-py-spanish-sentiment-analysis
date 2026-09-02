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
            return pd.read_csv(self.file_path)
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

    def save_csv(self):
        if self.csv is None:
            return
        self.csv.to_csv(self.file_path, index=False)

    def get_rows(self):
        if self.csv is not None:
            return self.csv.values.tolist()
        return []
