from bs4 import BeautifulSoup
from dre_scraper.config.urls import BASE_URL_PREFIX
from dre_scraper.model.scrapable import Scrapable


class Book(Scrapable):
    def __init__(self, name, url, session):
        self.name = name
        self.url = url
        self.session = session
        self.sections = []

    def __parse_row(self, row):
        # type, name, url, depth

        # Parsing depth
        inner_div = row.select_one("td > div")

        margin_left = 0 if inner_div is None or inner_div['style'] is None else int(
            inner_div['style'].split(":")[1].split("px")[0])

        depth = margin_left // 20

        # Parsing type
        a = row.select_one(
            "a.blacklink", href=True)
        type = "article" if a is not None and "Artigo" in a.text else "section"

        # Parsing name
        name_spans = row.select("a.blacklink span")
        name_spans_text = list(map(lambda span: span.text, name_spans))
        name = " ".join(name_spans_text)

        url = None if type == "section" else a["href"]

        return {
            "name": name,
            "type": type,
            "url": url,
            "depth": depth
        }

    def __parse(self, html):
        soup = BeautifulSoup(html, "html.parser")

        rows_raw = soup.find_all("tr")

        print(self.url, len(rows_raw))

        rows = list(map(self.__parse_row, rows_raw))

        print(rows)

        return None

    async def scrap(self):
        html = await self.session.get(BASE_URL_PREFIX.format(self.url))

        sections = self.__parse(html)

        self.sections = sections

    def __repr__(self):
        return f"<Book {self.name}, {self.url}, {len(self.sections)} sections>"
