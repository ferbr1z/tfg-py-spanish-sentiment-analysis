from enum import Enum
from typing import Literal


TweetProduct = Literal["Top", "Latest", "Media"]


class TweetTypeEnum(str, Enum):
    LATEST = "Latest"
    TOP = "Top"
    MEDIA = "Media"

    @property
    def product(self) -> TweetProduct:
        match self:
            case TweetTypeEnum.TOP:
                return "Top"
            case TweetTypeEnum.MEDIA:
                return "Media"
            case TweetTypeEnum.LATEST:
                return "Latest"
