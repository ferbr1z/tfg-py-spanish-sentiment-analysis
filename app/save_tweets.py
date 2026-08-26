from typing import Any

from sqlmodel import col, select
from sqlmodel.ext.asyncio.session import AsyncSession

from database.models import Post, SubTopic, Topic
from handlers import SheetCsvHandler
from schemas import PostCreateSchema, PostSchema

from .advance_subtopic import should_exhaust


async def save_tweets(
    sub_topic_id: int,
    items: list[PostCreateSchema],
    session: AsyncSession,
    sheet_csv_handler: SheetCsvHandler,
) -> dict[str, Any]:
    sub_topic: SubTopic | None = await session.get(SubTopic, sub_topic_id)

    if not sub_topic:
        return {"error": "SubTopic not found"}

    # Filtramos los que ya teniamos guardados para no duplicar.
    identifiers = [item.identifier for item in items]
    existentes = (
        set(
            (
                await session.exec(
                    select(col(Post.identifier)).where(
                        col(Post.identifier).in_(identifiers)
                    )
                )
            ).all()
        )
        if identifiers
        else set()
    )

    # Conservamos la primera aparición de cada ID dentro del lote. Así, un
    # reintento o un lote mal agregado no viola el índice único de Post.
    identifiers_seen = set(existentes)
    nuevos: list[PostCreateSchema] = []
    for item in items:
        if item.identifier not in identifiers_seen:
            nuevos.append(item)
            identifiers_seen.add(item.identifier)

    if items:
        sub_topic.last_id = items[-1].identifier

    posts: list[Post] = []
    if nuevos:
        sub_topic.page += 1
        sub_topic.count += len(nuevos)
        sub_topic.empty_streak = 0

        for item in nuevos:
            post = Post(
                identifier=item.identifier,
                created_at=item.created_at,
                text=item.text,
                sentiment_llm=item.sentiment_llm,
                llm_model=item.llm_model,
                llm_prompt_version=item.llm_prompt_version,
                llm_classified_at=item.llm_classified_at,
                topic_id=sub_topic.topic_id,
                subtopic_id=sub_topic.id,
                subtopic=sub_topic,
            )
            session.add(post)
            posts.append(post)
    else:
        sub_topic.empty_streak += 1

    sub_topic.exhausted = should_exhaust(sub_topic)

    session.add(sub_topic)
    await session.flush()

    topic = await session.get(Topic, sub_topic.topic_id)
    topic_name = topic.name if topic else None

    if nuevos:
        guardados = [
            PostSchema(**item.model_dump(), id=post.id)
            for item, post in zip(nuevos, posts)
        ]
        sheet_csv_handler.add_tweets(guardados, categoria=topic_name, sub_categoria=sub_topic.name)

    return {
        "topic": topic_name,
        "subtopic": sub_topic.name,
        "recibidos": len(items),
        "guardados": len(nuevos),
        "page": sub_topic.page,
        "last_id": sub_topic.last_id,
        "empty_streak": sub_topic.empty_streak,
        "should_exhaust": sub_topic.exhausted,
    }
