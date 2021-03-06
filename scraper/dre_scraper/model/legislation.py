import logging
import datetime
from bs4 import BeautifulSoup
from dre_scraper.config.urls import DRE_URL
from dre_scraper.model.book import Book
from dre_scraper.model.scrapable import Scrapable


class Legislation(Scrapable):

    def __init__(self, session):
        self.session = session
        self.books = []

        self.__config_logger()

    def __config_logger(self):
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            handlers=[
                logging.FileHandler(
                    "run-{}.log".format(datetime.datetime.now()).replace(":", ".")),
                logging.StreamHandler()
            ]
        )

        logging.getLogger().propagate = False

    def __parse(self, html=None):
        soup = BeautifulSoup(html, "html.parser")

        # Get the juridic legislation
        books_raw = soup.select("#RegimeJuridicos > div a", href=True)

        books = map(lambda book: Book(book.span.text,
                                      book["href"], self.session), books_raw)

        return list(books)

    async def scrap(self):
        html = await self.session.get(DRE_URL)

        books = self.__parse(html)

        tmp = 1

        for book in books:
            logging.info(f"Parsing {tmp}/{len(books)}")
            await book.scrap()
            logging.info(f"Parsed {tmp}/{len(books)} {book.name}")
            tmp += 1

        self.books = books

    def __repr__(self):
        return f"<Legislation {len(self.books)} books>"
