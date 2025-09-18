from dataclasses import asdict

from pymongo.asynchronous.collection import AsyncCollection
from pymongo.asynchronous.database import AsyncDatabase

from domain.models.quote import Quote
from infrastructure.mongo_db.connector import quotes_db_client


class QuotesRepository:
    def __init__(self, client: AsyncDatabase, collection_name: str):
        self._conn: AsyncCollection = client[collection_name]

    async def insert_batch(self, quotes: list[Quote]):
        await self._conn.insert_many([asdict(quote) for quote in quotes])

    async def all(self) -> list[Quote]:
        result: list[Quote] = []
        async for quote in self._conn.find({}, {'_id': False}).skip(10).limit(10):
            result.append(Quote(**quote))
        return result

    async def get_by_author_and_tags(self, author: str, tags: list[str]) -> list[Quote]:
        result: list[Quote] = []
        query_filter: dict = self._build_author_and_tags_query_filter(author, tags)
        async for quote in self._conn.find(query_filter, {'_id': False}).skip(10).limit(10):
            result.append(Quote(**quote))
        return result

    @staticmethod
    def _build_author_and_tags_query_filter(author: str, tags: list[str]):
        query_filter: dict = {}
        if author:
            query_filter['author'] = author
        if tags:
            query_filter['tags'] = {'$in': tags}
        return query_filter


quotes_repo: QuotesRepository = QuotesRepository(quotes_db_client, "quotes")
