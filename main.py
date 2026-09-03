from datetime import date, timedelta

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy import update
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app import fetch_data, get_scraper, get_sheet_csv_handler, get_sentiment_analyzer, lifespan
from app.get_available_subtopic import get_available_subtopic
from app.save_tweets import save_tweets
from database import get_session
from database.models import Post, Topic, SubTopic
from handlers import SheetCsvHandler
from schemas import PostCreateSchema, PostSchema, PostUpdateSchema, ScrapperSchema, SubTopicSchema, TestSchema, TopicSchema, \
    PostResponseSchema
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


@app.get("/posts/{page}", response_model=list[PostResponseSchema])
async def get_posts(
    page: int,
    per_page: int = Query(default=20, ge=1, le=100),
    session: AsyncSession = Depends(get_session),
):
    offset = (page - 1) * per_page
    result = await session.exec(select(Post).order_by(Post.id).offset(offset).limit(per_page))
    return result.all()


@app.post("/upload-data/{subtopic_id}")
async def upload_data(
    subtopic_id: int,
    items: list[PostCreateSchema],
    pagination_token: str | None = None,
    session: AsyncSession = Depends(get_session),
    sheet_csv_handler: SheetCsvHandler = Depends(get_sheet_csv_handler),
):
    return await save_tweets(subtopic_id, items, session, sheet_csv_handler, pagination_token)


@app.put("/posts")
async def update_posts(
    items: list[PostUpdateSchema],
    session: AsyncSession = Depends(get_session),
    sheet_csv_handler: SheetCsvHandler = Depends(get_sheet_csv_handler),
):
    if not items:
        return {"updated": 0}

    await session.execute(update(Post), [item.model_dump() for item in items])
    await session.commit()

    ids = [item.id for item in items]
    posts = (await session.exec(select(Post).where(Post.id.in_(ids)))).all()
    topics = {t.id: t.name for t in (await session.exec(select(Topic))).all()}
    subtopics = {s.id: s.name for s in (await session.exec(select(SubTopic))).all()}
    meta = {p.id: {"categoria": topics.get(p.topic_id), "sub_categoria": subtopics.get(p.subtopic_id)} for p in posts}

    sheet_csv_handler.update_tweets(items, meta=meta)
    return {"updated": len(items)}


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
    return await fetch_data(scraper, topic.name, topic.date_init, topic.date_end, topic.last_id, topic.pagination_token)

@app.post("/sentiment", response_model=PostCreateSchema)
async def sentiment(data: PostSchema, analyzer = Depends(get_sentiment_analyzer)):
    result = analyzer(data.text)
    data.robertuito_sentiment = result.output
    return data

@app.post("/sentiment/batch", response_model=list[PostCreateSchema])
async def sentiment_batch(data: list[PostSchema], analyzer = Depends(get_sentiment_analyzer)):
    for post in data:
        result = analyzer(post.text)
        post.robertuito_sentiment = result.output
    return data

@app.post("/test")
async def test(topic: TestSchema, scraper: Scrapper = Depends(get_scraper)):
    date_init = date.today() - timedelta(days=90)
    date_end = date.today() + timedelta(days=0)

    name = topic.topic
    last_id = topic.last_id

    return await fetch_data(scraper, name, date_init, date_end, last_id=last_id, pagination_token=topic.pagination_token)
