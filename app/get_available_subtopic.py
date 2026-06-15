from sqlmodel import select, col
from sqlmodel.ext.asyncio.session import AsyncSession

from config import PAGE_DEPTH
from database.models import SubTopic


async def get_available_subtopic(session: AsyncSession) -> SubTopic | None:

    # si se alcanzo el limite de paginacion

    statement = (
        select(SubTopic)
        .order_by(col(SubTopic.page).asc())
        .where(SubTopic.page < PAGE_DEPTH)
    )
    result = await session.exec(statement)

    return result.first()
