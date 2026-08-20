from datetime import date

from twikit import Tweet
from twikit.utils import Result

from config import COUNTRY
from scrapper import Scrapper



async def prepare_topic(topic: str, date_init: date, date_end: date, last_id: str | None = None) -> str:
    date_init_format = date_init.strftime("%Y-%m-%d")
    date_end_format = date_end.strftime("%Y-%m-%d")

    query = f"{topic} place_country:{COUNTRY} lang:es"

    if date_init_format:
        query += f" since:{date_init_format}"
    if date_end_format:
        query += f" until:{date_end_format}"
    if last_id:
        query += f" max_id:{int(last_id)}"

    return query


async def fetch_data(scraper: Scrapper,topic: str,date_init: date,date_end: date, last_id: str | None = None, limit: int = 20) -> dict[str, object]:
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
