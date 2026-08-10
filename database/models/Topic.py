from sqlmodel import Field, Relationship, SQLModel


class Topic(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str

    sub_topics: list["SubTopic"] = Relationship(back_populates="topic")
    posts: list["Post"] = Relationship(back_populates="topic")

class SubTopic(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str

    page: int = Field(default=0)
    count: int = Field(default=0)

    topic_id: int = Field(foreign_key="topic.id")

    topic: Topic = Relationship(back_populates="sub_topics")
    posts: list["Post"] = Relationship(back_populates="subtopic")


