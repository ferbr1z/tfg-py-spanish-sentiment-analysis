import asyncio
import logging

from xdk import Client

from config import X_BEARER_TOKEN

POST_FIELDS = ["created_at", "text"]


class Scrapper:
    def __init__(self):
        self.client = Client(bearer_token=X_BEARER_TOKEN)

    async def get_by_id(self, id: str):
        try:
            response = await asyncio.to_thread(self.client.posts.get_by_id, id, post_fields=POST_FIELDS)
            return response.data
        except Exception as e:
            logging.error(e)

    async def get_batch(self, query: str, count: int = 50, start_time: str | None = None, end_time: str | None = None, until_id: str | None = None):
        def _first_page():
            pages = self.client.posts.search_all(
                query=query,
                max_results=count,
                start_time=start_time,
                end_time=end_time,
                until_id=until_id,
                post_fields=POST_FIELDS,
                sort_order="recency",
            )
            return next(iter(pages), None)

        response = await asyncio.to_thread(_first_page)
        return response.data if response and response.data else []

    async def close(self):
        self.client.session.close()
