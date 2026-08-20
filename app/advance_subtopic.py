from config import EMPTY_STREAK_LIMIT, PAGE_DEPTH
from database.models import SubTopic


def advance_subtopic(
    sub_topic: SubTopic,
    fetched: int,
    saved: int,
    last_id: str | None = None,
) -> SubTopic:
    """Actualiza el estado del subtema despues de procesar un lote."""
    if fetched:
        sub_topic.page += 1
        if last_id:
            sub_topic.last_id = last_id

    # Contamos los posts nuevos, no los recibidos: max_id es inclusivo, asi
    # que una busqueda agotada igual devuelve el post del borde.
    if saved:
        sub_topic.count += saved
        sub_topic.empty_streak = 0
    else:
        sub_topic.empty_streak += 1

    return sub_topic


def should_exhaust(sub_topic: SubTopic) -> bool:
    """Si el subtema ya no aporta nada nuevo. Marcarlo lo decide quien llama."""
    return (
        sub_topic.empty_streak >= EMPTY_STREAK_LIMIT
        or sub_topic.page >= PAGE_DEPTH
    )
