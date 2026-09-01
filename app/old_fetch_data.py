from datetime import date

from twikit import Tweet
from twikit.utils import Result

from config import COUNTRY
from scrapper import Scrapper



async def prepare_topic(topic: str, date_init: date | None = None, date_end: date | None = None, last_id: str | None = None) -> str:
    query = f"{topic} place_country:{COUNTRY} lang:es -filter:retweets"

    if date_init:
        query += f" since:{date_init:%Y-%m-%d}"
    if date_end:
        query += f" until:{date_end:%Y-%m-%d}"
    if last_id:
        query += f" max_id:{int(last_id)}"

    return query


async def fetch_data(scraper: Scrapper,topic: str,date_init: date | None = None,date_end: date | None = None, last_id: str | None = None, pagination_token: str | None = None, limit: int = 20) -> dict[str, object]:
    # pagination_token es solo de xdk; twikit pagina por max_id (last_id) y lo ignora.
    tweets = await scraper.get_batch(await prepare_topic(topic, date_init, date_end, last_id))

    items = get_tweets_text(tweets)

    last_id = items[len(items) - 1]["identifier"] if items else None

    return {
        "items": items,
        "last_id": last_id,
        "pagination_token": None,
    }

def get_tweets_text(tweets: Result[Tweet]) -> dict[int, dict[str, str]]:
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
