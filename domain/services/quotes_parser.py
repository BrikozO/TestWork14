import logging

from bs4 import BeautifulSoup, Tag
from bs4.element import PageElement, NavigableString

from domain.models.quote import Quote

logger = logging.getLogger(__name__)


class QuotesParserService:
    """Service for parsing quotes from site: https://quotes.toscrape.com/"""

    def parse(self, soup: BeautifulSoup) -> list[Quote]:
        """Main parsing method

        Find all quotes on page, and parse them to list. If Quote attribute is unknow, it will be ignored

        Attributes:
             soup (BeautifulSoup): BeautifulSoup object of HTML page

        Returns:
            list[Quote]: list of Quote objects
        """
        quotes: list = soup.find_all(class_='quote')
        result: list[Quote] = []
        for quote in quotes:
            parsed_quote: Quote = self._parse_quote(quote)
            result.append(parsed_quote)
        return result

    def _parse_quote(self, quote_html: BeautifulSoup) -> Quote:
        author = self._get_text_safe(quote_html.find(class_='author'))
        text = self._get_text_safe(quote_html.find(class_='text'))
        tags = [self._get_text_safe(tag) for tag in quote_html.find_all('a', class_='tag')]
        return Quote(author, text, tags)

    @staticmethod
    def _get_text_safe[T: PageElement | Tag | NavigableString | None](element: T) -> str | None:
        try:
            return element.text
        except AttributeError:
            logger.warning('Part of quote can\'t be parsed!')
