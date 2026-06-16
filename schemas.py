from sqlmodel import Field, SQLModel

from scrapper.TweetTypeEnum import TweetTypeEnum


class TopicSchema(SQLModel):
    name: str


class SubTopicSchema(SQLModel):
    name: str
    page: int = Field(default=0)
    topic_id: int


class PostSchema(SQLModel):
    type: TweetTypeEnum
    identifier: str
    created_at: str
    text: str
    favorite_count: int
    retweet_count: int
    reply_count: int
    topic_id: int
    subtopic_id: int
    uploaded: bool = Field(default=False)

class TestSchema(SQLModel):
    type: TweetTypeEnum
    topic: str
    last_id: str | None = None