from sqlmodel import Field, Relationship, SQLModel
from scrapper.TweetTypeEnum import TweetTypeEnum

from .Topic import SubTopic, Topic


class Post(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    type: TweetTypeEnum = Field(nullable=False)

    identifier: str = Field(unique=True, index=True)
    created_at: str
    text: str

    favorite_count: int
    retweet_count: int
    reply_count: int

    topic_id: int = Field(foreign_key="topic.id")
    subtopic_id: int = Field(foreign_key="subtopic.id")

    topic: Topic = Relationship(back_populates="posts")
    subtopic: SubTopic = Relationship(back_populates="posts")

    # uploaded: bool = Field(default=False)