from datetime import date

from config import COUNTRY_GEOCODE
from scrapper import Scrapper, TweetTypeEnum

scraper = Scrapper()

async def prepare_topic(topic: str, date_init: date, date_end: date):
    return f"{topic} since:{date_init} until:{date_end} {COUNTRY_GEOCODE}"

async def fetch_data(topic: str, date_init: date, date_end: date, limit: int = 20):
    return await scraper.get_batch(await prepare_topic(topic, date_init, date_end))
