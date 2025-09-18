from typing import Annotated

from fastapi import APIRouter, Request
from fastapi.params import Query

from application.controllers.quotes import QuotesController, parse_task
from application.dto.request import GetQuotesQueryDTO
from infrastructure.constants import QUOTES_PARSING_REQUEST_LIMIT
from infrastructure.fastapi_cfg import limiter

router = APIRouter(prefix="")


@router.get('/quotes')
async def get_quotes_from_db(filter_params: Annotated[GetQuotesQueryDTO, Query()]):
    return await QuotesController.get_quotes_from_db(filter_params)


@router.post('/parse-quotes-task')
@limiter.limit(QUOTES_PARSING_REQUEST_LIMIT)
async def start_parse_quotes_task(request: Request):
    task = parse_task.delay()
    return {'task_id': task.id}
