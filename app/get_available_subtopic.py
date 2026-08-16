from sqlmodel import select, col
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
            col(SubTopic.exhausted).is_(False),
            col(SubTopic.page) < PAGE_DEPTH,
        )
        .order_by(col(SubTopic.page).asc(), col(SubTopic.id).asc())
    )
    result = await session.exec(statement)

    return result.first()
