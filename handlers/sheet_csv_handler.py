from csv_handler import CSVHandler, COLUMNS
from google_sheets import GoogleSheetsClient


class SheetCsvHandler:
    def __init__(self, sheet_id, csv_file="corpus.csv"):
        self.sheet_client = None
        self.csv_handler = CSVHandler(csv_file)
        self.sheets_enabled = True

        try:
            self.sheet_client = GoogleSheetsClient(sheet_id)
        except Exception as e:
            self.sheets_enabled = False
            print(
                "⚠️ Google Sheets deshabilitado (modo solo CSV local): "
                f"{e}"
            )

        # Cuántas filas de datos están ya en el sheet remoto.
        # Se actualiza en sync_sheet_to_csv y en add_tweets.
        self._synced_rows = len(self.csv_handler.csv)

    def sync_sheet_to_csv(self):
        """Baja la hoja completa al CSV local. Costoso — ejecutar solo al
        iniciar el proceso o cuando se sospecha drift."""
        if not self.sheets_enabled or self.sheet_client is None:
            return
        self.sheet_client.download_sheet_as_csv(self.csv_handler.file_path)
        self.csv_handler.csv = self.csv_handler.read_csv(self.csv_handler.file_path)
        self._synced_rows = len(self.csv_handler.csv)

    def sync_csv_to_sheet(self):
        """Sube el CSV local completo (rewrite). Solo para usos puntuales."""
        self.csv_handler.save_csv(self.csv_handler.file_path)
        if not self.sheets_enabled or self.sheet_client is None:
            return
        self.sheet_client.upload_csv_to_sheet(self.csv_handler.file_path)
        self._synced_rows = len(self.csv_handler.csv)

    def add_tweet(self, tweet_data):
        return self.add_tweets([tweet_data])

    def add_tweets(self, tweets_data):
        """Dedupe + persistir local + append solo de las filas nuevas al sheet."""
        added = self.csv_handler.add_rows(tweets_data)
        if added:
            self.csv_handler.save_csv(self.csv_handler.file_path)

        if not self.sheets_enabled or self.sheet_client is None:
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
        start_row = self._synced_rows + 2  # +1 por header, +1 por 1-based
        self.sheet_client.append_rows(rows, start_row)
        self._synced_rows += len(rows)
        return added
