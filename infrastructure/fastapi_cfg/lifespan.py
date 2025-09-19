from contextlib import asynccontextmanager

from fastapi import FastAPI

from infrastructure.constants import LOGGING_CONFIG
from infrastructure.environment import env
from infrastructure.logging_cfg import setup_logging
from infrastructure.mongo_db.connector import conn
from infrastructure.mongo_db.quotes_index import create_unique_index


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging(LOGGING_CONFIG)
    cn = await conn.get_async_connection()
    await create_unique_index(cn, env.mongodb.quotes_collection, ['author', 'text'])
    yield
