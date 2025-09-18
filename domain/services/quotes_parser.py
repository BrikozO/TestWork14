from bs4 import BeautifulSoup, Tag
from bs4.element import PageElement, NavigableString

from domain.models.quote import Quote


class QuotesParserService:

    def parse(self, soup: BeautifulSoup) -> list[Quote]:
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
            print(f'Спарсить часть цитаты не получилось!')
