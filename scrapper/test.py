"""
Smoke test del scrapper: busca un tema en los últimos 30 días en Paraguay
con product=Latest y muestra los tweets.

Uso:
    python -m scrapper.test
"""
import asyncio
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scrapper import Scrapper, TweetTypeEnum


TOPIC = "santi"
COUNTRY = "PY"
COUNT = 20


async def main():
    scraper = Scrapper()
    query = f"{TOPIC} place_country:{COUNTRY} lang:es"
    result = await scraper.get_batch(query, count=COUNT, tweet_type=TweetTypeEnum.LATEST)

    print(f"Query: {query!r}")
    print(f"Tweets encontrados: {len(result)}")
    for i, tweet in enumerate(result, 1):
        print(f"{i}. {tweet.text}")


if __name__ == "__main__":
    asyncio.run(main())
