from bs4 import BeautifulSoup
from dre_scraper.config.urls import DRE_URL
from dre_scraper.model.scrapable import Scrapable


class Legislation(Scrapable):
    def __init__(self, session):
        self.session = session
        pass

    def __parse(self, html):
        soup = BeautifulSoup(html, 'html.parser')

        # Get the juridic legislation
        books = soup.select('#RegimeJuridicos > div a', href=True)

        return books

    async def scrap(self):
        html = await self.session.get(DRE_URL)

        books = self.__parse(html)

        pass

    def __repr__(self):
        return f"<Legislation {len(self.books)} books>"
