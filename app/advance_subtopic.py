from config import EMPTY_STREAK_LIMIT, PAGE_DEPTH
from database.models import SubTopic


def should_exhaust(sub_topic: SubTopic) -> bool:
    """Si el subtema ya no aporta nada nuevo. Marcarlo lo decide quien llama."""
    return (
        sub_topic.empty_streak >= EMPTY_STREAK_LIMIT
        or sub_topic.page >= PAGE_DEPTH
    )
