from sqlmodel import Field, Relationship, SQLModel


class Topic(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    completed: bool = Field(default=False)

    sub_topics: list["SubTopic"] = Relationship(back_populates="topic")


class SubTopic(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    page: int = Field(default=0)
    completed: bool = Field(default=False)

    topic_id: int = Field(foreign_key="topic.id")

    topic: Topic = Relationship(back_populates="sub_topics")