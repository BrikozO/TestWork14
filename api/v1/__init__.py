from fastapi import APIRouter

from api.v1 import quotes

basic_router = APIRouter(prefix="/api/v1", tags=["v1"])

basic_router.include_router(quotes.router)
