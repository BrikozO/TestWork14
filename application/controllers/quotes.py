from urllib.parse import urljoin

from bs4 import BeautifulSoup

from application.dto.request import GetQuotesQueryDTO
from domain.models.quote import Quote
from domain.services.quotes_parser import QuotesParserService
from infrastructure.constants import QUOTES_SITE_URL
from infrastructure.http_client import http_client
from infrastructure.mongo_db.quotes_repository import quotes_repo


class QuotesController:

    @staticmethod
    async def get_quotes_from_db(filter_: GetQuotesQueryDTO) -> list[Quote]:
        if filter_.empty:
            return await quotes_repo.all()
        return await quotes_repo.get_by_author_and_tags(filter_.author, filter_.tags)

    @staticmethod
    async def parse():
        next_page = ''
        result: list[Quote] = []
        while next_page is not None:
            response = await http_client.get(urljoin(QUOTES_SITE_URL, next_page))
            soup = BeautifulSoup(response.text, 'lxml')
            curr_page_quotes = await QuotesParserService().parse(soup)
            result += curr_page_quotes
            next_page = try_to_get_next_page_link(soup)

        await quotes_repo.insert_batch(result)


def try_to_get_next_page_link(soup: BeautifulSoup) -> str | None:
    next_element = soup.find('ul', class_='pager').find('li', class_='next')
    if next_element:
        return next_element.find('a').get('href')
    return None
