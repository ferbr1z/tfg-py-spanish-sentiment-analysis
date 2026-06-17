import logging

from twikit import Client, Tweet
from twikit.utils import Result

from scrapper.TweetTypeEnum import TweetTypeEnum
from .compat import CompatibleClientTransaction
from .cookies import get_cookies

class Scrapper:
    def __init__(self):
        self.client = Client('en-US')
        self.client.client_transaction = CompatibleClientTransaction()
        self.client.set_cookies(get_cookies())

    async def get_by_id(self, id: str):
        try:
            return await self.client.get_tweet_by_id(id)
        except Exception as e:
            logging.error(e)

    async def get_batch(self, query: str, count: int = 20, tweet_type: TweetTypeEnum = TweetTypeEnum.LATEST) -> Result[Tweet]:
        return await self.client.search_tweet(
            query=query,
            product=tweet_type.product,
            count=count,
        )
