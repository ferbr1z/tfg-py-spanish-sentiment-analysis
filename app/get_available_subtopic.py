from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from config import PAGE_DEPTH
from database.models import SubTopic


async def get_available_subtopic(session: AsyncSession) -> SubTopic | None:

    # Sale el menos avanzado (menor page); a igual page, el que menos veces
    # vino vacio (menor empty_streak); a igual todo, por id para que el
    # recorrido sea siempre el mismo. Los agotados quedan fuera.
    statement = (
        select(SubTopic)
        .where(
            SubTopic.exhausted == False,
            SubTopic.page < PAGE_DEPTH
        )
        .order_by(SubTopic.page, SubTopic.empty_streak, SubTopic.id)
        .limit(1)
    )
    result = await session.exec(statement)

    return result.first()
