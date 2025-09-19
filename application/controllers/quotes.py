from logging import getLogger
from urllib.parse import urljoin

import httpx
from bs4 import BeautifulSoup

from application.dto.request import GetQuotesQueryDTO
from application.dto.response import QuotesFromDBResponseDTO
from domain.models.quote import Quote
from domain.services.quotes_parser import QuotesParserService
from infrastructure.celery_cfg import celery_app
from infrastructure.constants import QUOTES_SITE_URL
from infrastructure.environment import env
from infrastructure.http_client import http_client
from infrastructure.mongo_db.connector import conn
from infrastructure.mongo_db.quotes_repository import AsyncQuotesRepository, SyncQuotesRepository

logger = getLogger(__name__)


class QuotesController:
    @staticmethod
    async def get_quotes_from_db(filter_: GetQuotesQueryDTO) -> QuotesFromDBResponseDTO:
        mongo_client = await conn.get_async_connection()
        repo: AsyncQuotesRepository = AsyncQuotesRepository(
            client=mongo_client, collection=env.mongodb.quotes_collection
        )
        if filter_.empty:
            logger.info('Get all quotes from db (empty filter)')
            quotes: list[Quote] = await repo.all()
        else:
            logger.info(f'Get quotes by filter: {filter_.author} | {filter_.tags}')
            quotes: list[Quote] = await repo.get_by_author_and_tags(filter_.author, filter_.tags)
        return QuotesFromDBResponseDTO(quotes=quotes, filter=filter_)

    @staticmethod
    def parse():
        next_page = ''
        result: list[Quote] = []
        while next_page is not None:
            try:
                response = http_client.get(urljoin(QUOTES_SITE_URL, next_page))
            except (httpx.HTTPError, httpx.TimeoutException) as e:
                logger.error(f'Failed to get next page: {e}')
                break

            soup = BeautifulSoup(response.text, 'lxml')
            curr_page_quotes = QuotesParserService().parse(soup)
            result += curr_page_quotes
            logger.info(f'Parsed {len(curr_page_quotes)} quotes from current page. Total: {len(result)}')

            next_page = QuotesController._try_to_get_next_page_link(soup)
        if result:
            SyncQuotesRepository(
                client=conn.get_sync_connection(), collection=env.mongodb.quotes_collection
            ).insert_batch(result)

    @staticmethod
    def _try_to_get_next_page_link(soup: BeautifulSoup) -> str | None:
        next_element = soup.find('ul', class_='pager').find('li', class_='next')
        if next_element:
            next_page_link = next_element.find('a').get('href')
            logger.info(f'Found link to next quotes page: {next_page_link}')
            return next_page_link
        return None


@celery_app.task
def parse_task():
    QuotesController.parse()
