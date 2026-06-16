from datetime import date

from twikit import Tweet
from twikit.utils import Result

from config import COUNTRY
from scrapper import Scrapper



async def prepare_topic(topic: str, date_init: date, date_end: date, last_id: str | None = None) -> str:
    query = f"{topic} place_country:{COUNTRY} lang:es"
    if last_id:
        query += f" max_id:{int(last_id)}"
    return query


async def fetch_data(scraper: Scrapper,topic: str,date_init: date,date_end: date,limit: int = 20, last_id: str | None = None) -> dict[str, object]:
    tweets = await scraper.get_batch(await prepare_topic(topic, date_init, date_end, last_id))

    items = get_tweets_text(tweets)

    last_id = items[len(items) - 1]["id"] if items else None

    return {
        "items": items,
        "last_id": last_id,
    }

def get_tweets_text(tweets: Result[Tweet]) -> dict[int, dict[str, str]]:
    result = {}
    for idx, tweet in enumerate(tweets):
        result.setdefault(idx, {"id": tweet.id, "text": tweet.text})
    return result
