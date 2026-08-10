from datetime import date, timedelta

from fastapi import Depends, FastAPI
from sqlmodel.ext.asyncio.session import AsyncSession

from app import fetch_data, get_scraper, lifespan
from app.get_available_subtopic import get_available_subtopic
from database import get_session
from database.models import Topic, SubTopic
from schemas import TopicSchema, SubTopicSchema, TestSchema
from scrapper import Scrapper

app = FastAPI(lifespan=lifespan)


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

@app.post("/upload-data")
async def upload_data(session: AsyncSession = Depends(get_session)):
    return {};

@app.post("/test")
async def test(topic: TestSchema, scraper: Scrapper = Depends(get_scraper)):
    date_init = date.today() - timedelta(days=30)
    date_end = date.today() + timedelta(days=0)

    name = topic.topic
    last_id = topic.last_id

    return await fetch_data(scraper, name, date_init, date_end, last_id=last_id)
