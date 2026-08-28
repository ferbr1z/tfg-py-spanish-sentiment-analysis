"""
Smoke test del scrapper nuevo (xdk / X API v2): busca un tema en un rango de ~3 años
en Paraguay vía search_all y muestra los tweets.

Uso:
    python -m scrapper.test
"""
import asyncio
import sys
from datetime import date, timedelta
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scrapper.client import Scrapper


TOPIC = "santi"
COUNTRY = "PY"
COUNT = 20


async def main():
    scraper = Scrapper()
    date_init = date.today() - timedelta(days=365 * 3)
    date_end = date.today()
    query = f"{TOPIC} place_country:{COUNTRY} lang:es"
    result = await scraper.get_batch(
        query,
        count=COUNT,
        start_time=f"{date_init:%Y-%m-%d}T00:00:00Z",
        end_time=f"{date_end:%Y-%m-%d}T00:00:00Z",
    )

    print(f"Query: {query!r}")
    print(f"Tweets encontrados: {len(result)}")
    for i, tweet in enumerate(result, 1):
        print(f"{i}. {tweet.text}")

    await scraper.close()


if __name__ == "__main__":
    asyncio.run(main())
