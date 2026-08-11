from contextlib import asynccontextmanager

from fastapi import FastAPI, Request

from database import create_db_and_tables
from scrapper import Scrapper


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    app.state.scraper = Scrapper()
    try:
        yield
    finally:
        await app.state.scraper.client.http.aclose()


def get_scraper(request: Request) -> Scrapper:
    return request.app.state.scraper
