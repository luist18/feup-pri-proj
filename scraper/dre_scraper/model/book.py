from bs4 import BeautifulSoup
from dre_scraper.config.urls import BASE_URL_PREFIX
from dre_scraper.model.book_entry import BookEntry, BookEntryType
from dre_scraper.model.scrapable import Scrapable


class Book(Scrapable):
    def __init__(self, name, url, session):
        self.name = name
        self.url = url
        self.session = session
        self.root_section = None

    def __parse_row(self, row):
        # type, name, url, depth

        # Parsing depth
        inner_div = row.select_one("td > div")
        margin_left = 0 if inner_div is None or inner_div['style'] is None else int(
            inner_div['style'].split(":")[1].split("px")[0])

        # 20px per depth
        depth = margin_left // 20

        # Parsing type
        a = row.select_one(
            "a.blacklink", href=True)
        type = BookEntryType.ARTICLE if a is not None and "Artigo" in a.text else BookEntryType.SECTION

        # Parsing url
        url = None if type == BookEntryType.SECTION else a["href"]

        # Parsing name
        name_spans = row.select("span")
        name_spans_text = list(map(lambda span: span.text, name_spans))
        name = " ".join(name_spans_text)

        return BookEntry(name, type, depth, url)

    def __parse(self, html):
        soup = BeautifulSoup(html, "html.parser")

        rows_raw = soup.find_all("tr")
        # Remove empty rows, websites from the government are always good and have empty rows :)
        rows_raw = list(filter(lambda row: len(
            row.select("span")) > 0, rows_raw))

        entries = list(map(self.__parse_row, rows_raw))

        # parse entries into sections and articles

        return None

    async def scrap(self):
        html = await self.session.get(BASE_URL_PREFIX.format(self.url))

        entries = self.__parse(html)

    def __repr__(self):
        return f"<Book {self.name}, {self.url}, {len(self.sections)} sections>"
