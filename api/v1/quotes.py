from typing import Annotated

from fastapi import APIRouter, Request
from fastapi.params import Query

from application.controllers.quotes import QuotesController, parse_task
from application.dto.request import GetQuotesQueryDTO
from application.dto.response import QuotesFromDBResponseDTO
from infrastructure.constants import QUOTES_PARSING_REQUEST_LIMIT
from infrastructure.fastapi_cfg import limiter

router = APIRouter(prefix="")


@router.get('/quotes')
async def get_quotes_from_db(filter_params: Annotated[GetQuotesQueryDTO, Query()]) -> QuotesFromDBResponseDTO:
    """Get parsed quotes from database by filter parameters.

    Args:
        filter_params: Filter parameters containing author and tags.
            If both author and tags are empty, returns all quotes.
            - author: Author name to filter by
            - tags: List of tags to filter by

    Returns:
        List of Quote objects matching the filter criteria.
    """
    return await QuotesController.get_quotes_from_db(filter_params)


@router.post('/parse-quotes-task')
@limiter.limit(QUOTES_PARSING_REQUEST_LIMIT)
async def start_parse_quotes_task(request: Request):
    """Parse quotes from site: https://quotes.toscrape.com/

    Parsing start's async in celery worker
    """
    task = parse_task.delay()
    return {'task_id': task.id}
