from datetime import date, timedelta

from fastapi import Depends, FastAPI
from sqlmodel.ext.asyncio.session import AsyncSession

from app import fetch_data
from app.get_available_subtopic import get_available_subtopic
from database import get_session
from database.models import Topic, SubTopic
from schemas import TopicSchema, SubTopicSchema

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/register/topic", response_model=Topic)
async def register_topic(topic_data: TopicSchema, session: AsyncSession = Depends(get_session)):
    topic = Topic(name=topic_data.name)
    session.add(topic)
    await session.commit()
    await session.refresh(topic)
    return topic


@app.post("/register/subtopic", response_model=SubTopic)
async def register_subtopic(
    subtopic_data: SubTopicSchema,
    session: AsyncSession = Depends(get_session),
):
    subtopic = SubTopic(name=subtopic_data.name, topic_id=subtopic_data.topic_id)
    session.add(subtopic)
    await session.commit()
    await session.refresh(subtopic)
    return subtopic


@app.get("/available")
async def available_topics(session: AsyncSession = Depends(get_session)):
    return await get_available_subtopic(session)

@app.post("/test/{topic}")
async def test(topic: str):
    date_init = date.today() - timedelta(days=1)
    date_end = date.today() + timedelta(days=1)

    return await fetch_data(topic, date_init, date_end)
