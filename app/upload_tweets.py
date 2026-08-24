from sqlmodel import select, col
from sqlmodel.ext.asyncio.session import AsyncSession
from typing_extensions import List


from database.models import Post, SubTopic
from schemas import PostSchema

from .advance_subtopic import should_exhaust


async def upload_tweets(sub_topic_id: int, items: List[PostSchema], session: AsyncSession):
    sub_topic: SubTopic | None = await session.get(SubTopic, sub_topic_id)

    if not sub_topic:
        return {"error": "SubTopic not found"}

    # Filtramos los que ya teniamos guardados para no duplicar.
    existentes = set(
        (await session.exec(
            select(col(Post.identifier)).where(
                col(Post.identifier).in_([i.identifier for i in items])
            )
        )).all()
    ) if items else set()
    nuevos = [i for i in items if i.identifier not in existentes]

    if nuevos:
        sub_topic.last_id = items[-1].identifier
        sub_topic.page += 1
        sub_topic.count += len(nuevos)
        sub_topic.empty_streak = 0

        for item in nuevos:
            session.add(Post(
                type=item.type,
                identifier=item.identifier,
                created_at=item.created_at,
                text=item.text,
                favorite_count=item.favorite_count,
                retweet_count=item.retweet_count,
                reply_count=item.reply_count,
                topic_id=sub_topic.topic_id,
                subtopic_id=sub_topic.id,
                subtopic=sub_topic,
            ))
    else:
        sub_topic.empty_streak += 1

    session.add(sub_topic)
    await session.flush()

    return {
        "subtopic": sub_topic.name,
        "recibidos": len(items),
        "guardados": len(nuevos),
        "page": sub_topic.page,
        "last_id": sub_topic.last_id,
        "empty_streak": sub_topic.empty_streak,
        "should_exhaust": should_exhaust(sub_topic),
    }
