from contextlib import asynccontextmanager

from fastapi import FastAPI, Request

from config import SHEET_ID
from handlers import SheetCsvHandler
from scrapper import Scrapper


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.scraper = Scrapper()
    app.state.sheet_csv_handler = SheetCsvHandler(SHEET_ID)
    app.state.sheet_csv_handler.sync_sheet_to_csv()
    try:
        yield
    finally:
        await app.state.scraper.close()


def get_scraper(request: Request) -> Scrapper:
    return request.app.state.scraper


def get_sheet_csv_handler(request: Request) -> SheetCsvHandler:
    return request.app.state.sheet_csv_handler
