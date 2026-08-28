from config import USE_OLD
from .TweetTypeEnum import TweetTypeEnum

if USE_OLD:
    from .old import Scrapper
else:
    from .client import Scrapper

__all__ = ['Scrapper', 'TweetTypeEnum']
