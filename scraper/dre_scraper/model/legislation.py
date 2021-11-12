from bs4 import BeautifulSoup
from dre_scraper.config.urls import DRE_URL
from dre_scraper.model.book import Book
from dre_scraper.model.scrapable import Scrapable


class Legislation(Scrapable):
    
    def __init__(self, session, verbose=False):
        self.session = session
        self.books = []
        self.verbose = verbose

    def __parse(self, html=None):
        soup = BeautifulSoup(html, "html.parser")

        # Get the juridic legislation
        books_raw = soup.select("#RegimeJuridicos > div a", href=True)

        books = map(lambda book: Book(book.span.text,
                                      book["href"], self.session), books_raw)

        return list(books)

    async def scrap(self):
        print("Getting legislation")

        html = await self.session.get(DRE_URL)

        print("Parsing legislation")

        books = self.__parse(html)

        # todo: tmp
        books = books[:1]

        for book in books:
            await book.scrap()

        print("Parsed legislation")

        self.books = books

    def __repr__(self):
        return f"<Legislation {len(self.books)} books>"
