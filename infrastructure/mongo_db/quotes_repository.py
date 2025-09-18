import logging
from dataclasses import asdict

from pymongo.asynchronous.collection import AsyncCollection
from pymongo.asynchronous.database import AsyncDatabase
from pymongo.errors import BulkWriteError
from pymongo.synchronous.collection import Collection
from pymongo.synchronous.database import Database

from domain.models.quote import Quote
from infrastructure.mongo_db.connector import quotes_db_client_async, quotes_db_client


class AsyncQuotesRepository:
    _DUPLICATE_ERROR_CODE: int = 11000
    def __init__(self, client: AsyncDatabase, collection_name: str):
        self._conn: AsyncCollection = client[collection_name]

    async def insert_batch(self, quotes: list[Quote]):
        try:
            await self._conn.insert_many([asdict(quote) for quote in quotes], ordered=False)
            logging.info(f"Inserted {len(quotes)} quotes")
        except BulkWriteError as e:
            inserted_count = e.details.get('nInserted', 0)
            duplicate_errors = [
                error for error in e.details.get('writeErrors', [])
                if error.get('code') == self._DUPLICATE_ERROR_CODE
            ]
            logging.info(f"inserted {inserted_count} quotes and ignored {len(duplicate_errors)} duplicates")

    async def all(self) -> list[Quote]:
        result: list[Quote] = []
        async for quote in self._conn.find({}, {'_id': False}):
            result.append(Quote(**quote))
        return result

    async def get_by_author_and_tags(self, author: str, tags: list[str]) -> list[Quote]:
        result: list[Quote] = []
        query_filter: dict = self._build_author_and_tags_query_filter(author, tags)
        async for quote in self._conn.find(query_filter, {'_id': False}):
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


class SyncQuotesRepository:
    _DUPLICATE_ERROR_CODE: int = 11000

    def __init__(self, client: Database, collection_name: str):
        self._conn: Collection = client[collection_name]

    def insert_batch(self, quotes: list[Quote]):
        try:
            self._conn.insert_many([asdict(quote) for quote in quotes], ordered=False)
            logging.info(f"Inserted {len(quotes)} quotes")
        except BulkWriteError as e:
            inserted_count = e.details.get('nInserted', 0)
            duplicate_errors = [
                error for error in e.details.get('writeErrors', [])
                if error.get('code') == self._DUPLICATE_ERROR_CODE
            ]
            logging.info(f"inserted {inserted_count} quotes and ignored {len(duplicate_errors)} duplicates")


quotes_repo_async: AsyncQuotesRepository = AsyncQuotesRepository(quotes_db_client_async, "quotes")
quotes_repo = SyncQuotesRepository(quotes_db_client, "quotes")
