import asyncio
from urllib.parse import urljoin

import httpx
from bs4 import BeautifulSoup

from constants import QUOTAS_SITE_URL
from domain.models.quote import Quote
from domain.services.quotes_parser import QuotesParserService

http_client: httpx.AsyncClient = httpx.AsyncClient(follow_redirects=True, verify=False, timeout=10)


async def main():
    next_page = ''
    result: list[Quote] = []
    while next_page is not None:
        response = await http_client.get(urljoin(QUOTAS_SITE_URL, next_page))
        soup = BeautifulSoup(response.text, 'lxml')
        curr_page_quotes = await QuotesParserService().parse(soup)
        result += curr_page_quotes
        next_page = try_to_get_next_page_link(soup)

    print(f'Found {len(result)} quotes')


def try_to_get_next_page_link(soup: BeautifulSoup) -> str | None:
    next_element = soup.find('ul', class_='pager').find('li', class_='next')
    if next_element:
        return next_element.find('a').get('href')
    return None


if __name__ == '__main__':
    asyncio.run(main())
