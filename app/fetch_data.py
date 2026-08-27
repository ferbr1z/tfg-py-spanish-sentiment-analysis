from datetime import date

from config import COUNTRY
from scrapper import Scrapper



async def prepare_topic(topic: str) -> str:
    return f"{topic} place_country:{COUNTRY} lang:es"


async def fetch_data(scraper: Scrapper,topic: str,date_init: date,date_end: date, last_id: str | None = None, limit: int = 50) -> dict[str, object]:
    tweets = await scraper.get_batch(
        await prepare_topic(topic),
        count=limit,
        start_time=f"{date_init:%Y-%m-%d}T00:00:00Z",
        end_time=f"{date_end:%Y-%m-%d}T00:00:00Z",
        until_id=str(int(last_id)) if last_id else None,
    )

    items = get_tweets_text(tweets)

    last_id = items[len(items) - 1]["identifier"] if items else None

    return {
        "items": items,
        "last_id": last_id,
    }

def get_tweets_text(tweets) -> dict[int, dict[str, str]]:
    result = {}
    for idx, tweet in enumerate(tweets):
        result.setdefault(
            idx,
            {
                "id": tweet.id,
                "identifier": tweet.id,
                "created_at": tweet.created_at,
                "text": tweet.text,
            },
        )
    return result
