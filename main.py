from datetime import date, timedelta

from fastapi import Depends, FastAPI, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from app import fetch_data, get_scraper, lifespan
from app.get_available_subtopic import get_available_subtopic
from database import get_session
from database.models import Topic, SubTopic
from schemas import TopicSchema, SubTopicSchema, TestSchema, ScrapperSchema
from scrapper import Scrapper

app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/register/topic", response_model=Topic)
async def register_topic(topic_data: TopicSchema, session: AsyncSession = Depends(get_session)):
    topic = Topic(name=topic_data.name)
    session.add(topic)
    await session.refresh(topic)
    return topic


@app.post("/register/subtopic", response_model=SubTopic)
async def register_subtopic(
    subtopic_data: SubTopicSchema,
    session: AsyncSession = Depends(get_session),
):
    subtopic = SubTopic(name=subtopic_data.name, topic_id=subtopic_data.topic_id)
    session.add(subtopic)
    await session.refresh(subtopic)
    return subtopic


@app.get("/available")
async def available_topics(session: AsyncSession = Depends(get_session)):
    return await get_available_subtopic(session)

@app.post("/upload-data")
async def upload_data(session: AsyncSession = Depends(get_session)):
    return {};

@app.post("/subtopic/{subtopic_id}/exhaust")
async def exhaust_subtopic(
    subtopic_id: int,
    exhausted: bool = True,
    session: AsyncSession = Depends(get_session),
):
    """Saca (o devuelve) un subtema de la cola."""
    subtopic = await session.get(SubTopic, subtopic_id)
    if subtopic is None:
        raise HTTPException(status_code=404, detail="SubTopic not found")

    subtopic.exhausted = exhausted
    session.add(subtopic)
    await session.commit()
    await session.refresh(subtopic)
    return subtopic

@app.post("/scrapper")
async def scrapper(topic: ScrapperSchema, scraper = Depends(get_scraper)):
    return await fetch_data(scraper, topic.name, topic.date_init, topic.date_end, topic.last_id)

@app.post("/test")
async def test(topic: TestSchema, scraper: Scrapper = Depends(get_scraper)):
    date_init = date.today() - timedelta(days=90)
    date_end = date.today() + timedelta(days=0)

    name = topic.topic
    last_id = topic.last_id

    return await fetch_data(scraper, name, date_init, date_end, last_id=last_id)
