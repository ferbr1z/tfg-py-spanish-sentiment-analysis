from contextlib import asynccontextmanager

from fastapi import FastAPI, Request

from scrapper import Scrapper


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.scraper = Scrapper()
    try:
        yield
    finally:
        await app.state.scraper.client.http.aclose()


def get_scraper(request: Request) -> Scrapper:
    return request.app.state.scraper
