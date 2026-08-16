from sqlmodel import select, col
from sqlmodel.ext.asyncio.session import AsyncSession
from typing_extensions import List


from database.models import Post, SubTopic
from schemas import PostSchema

from .advance_subtopic import advance_subtopic, should_exhaust


async def upload_tweets(sub_topic_id: int, items: List[PostSchema], session: AsyncSession):
    sub_topic : SubTopic | None = (await  session.exec(select(SubTopic).where(SubTopic.id == sub_topic_id))).first()

    if not sub_topic:
        return {"error": "SubTopic not found"}

    assert sub_topic.id is not None

    # Cuales de estos no teniamos ya guardados.
    nuevos = items
    if nuevos:
        existentes = set(
            (await session.exec(
                select(col(Post.identifier)).where(
                    col(Post.identifier).in_([i.identifier for i in nuevos])
                )
            )).all()
        )
        nuevos = [i for i in nuevos if i.identifier not in existentes]

    advance_subtopic(
        sub_topic,
        len(items),
        len(nuevos),
        items[-1].identifier if items else None,
    )
    session.add(sub_topic)

    for item in nuevos:
        post: Post = Post(
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
        )
        session.add(post)
        
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
