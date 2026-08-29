from datetime import date, datetime
from typing import Literal

from sqlmodel import Field, SQLModel

from database.models.Post import Lang
from scrapper.TweetTypeEnum import TweetTypeEnum


class TopicSchema(SQLModel):
    name: str


class SubTopicSchema(SQLModel):
    name: str
    page: int = Field(default=0)
    topic_id: int


class PostCreateSchema(SQLModel):
    identifier: str
    created_at: str
    text: str
    sentiment_llm: Literal["POS", "NEG", "NEU"]
    llm_model: str
    llm_prompt_version: str
    llm_classified_at: datetime

    lang: Lang | None = None
    has_irony: bool = False
    mixed: bool = False

    discarded: bool = False
    discard_reason: str | None = None
    llm_reason: str | None = None

    source_type: str | None = None


class PostSchema(PostCreateSchema):
    id: int


class TestSchema(SQLModel):
    type: TweetTypeEnum
    topic: str
    last_id: str | None = None


class ScrapperSchema(SQLModel):
    date_init: date
    date_end: date
    name: str
    type: TweetTypeEnum
    last_id: str | None = None
