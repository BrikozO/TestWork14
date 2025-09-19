from contextlib import asynccontextmanager

from fastapi import FastAPI

from infrastructure.constants import LOGGING_CONFIG
from infrastructure.logging_cfg import setup_logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging(LOGGING_CONFIG)
    yield
    print('Done')
