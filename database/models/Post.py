from datetime import datetime

from sqlalchemy import Column, DateTime
from sqlmodel import Field, Relationship, SQLModel

from .Topic import SubTopic, Topic


class Post(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    identifier: str = Field(unique=True, index=True)
    created_at: str
    text: str

    sentiment_llm: str | None = Field(default=None)
    llm_model: str | None = Field(default=None)
    llm_prompt_version: str | None = Field(default=None)
    llm_classified_at: datetime | None = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), nullable=True),
    )

    topic_id: int = Field(foreign_key="topic.id")
    subtopic_id: int = Field(foreign_key="subtopic.id")

    topic: Topic = Relationship(back_populates="posts")
    subtopic: SubTopic = Relationship(back_populates="posts")
