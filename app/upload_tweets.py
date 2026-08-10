from sqlmodel import select, col
from sqlmodel.ext.asyncio.session import AsyncSession
from typing_extensions import List


from database.models import Post, SubTopic
from schemas import PostSchema


async def upload_tweets(sub_topic_id: int, items: List[PostSchema], session: AsyncSession):
    sub_topic : SubTopic | None = (await  session.exec(select(SubTopic).where(SubTopic.id == sub_topic_id))).first()

    if not sub_topic:
        return {"error": "SubTopic not found"}

    assert sub_topic.id is not None

    sub_topic.count += len(items)

    for item in items:
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
    
    