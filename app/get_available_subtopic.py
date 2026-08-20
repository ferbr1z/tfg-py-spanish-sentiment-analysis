from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from config import PAGE_DEPTH
from database.models import SubTopic


async def get_available_subtopic(session: AsyncSession) -> SubTopic | None:

    # Sale el menos avanzado. Los agotados quedan fuera: si no, se quedan
    # con el page mas bajo y bloquean la cola. Desempata por id para que
    # el recorrido sea siempre el mismo.
    statement = (
        select(SubTopic)
        .where(
            SubTopic.exhausted == False,
            SubTopic.page < PAGE_DEPTH
        )
        .order_by(SubTopic.page, SubTopic.id)
        .limit(1)
    )
    result = await session.exec(statement)

    return result.first()
