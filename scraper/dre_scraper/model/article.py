from bs4 import BeautifulSoup
from dre_scraper.config.urls import BASE_URL_PREFIX
from dre_scraper.model.scrapable import Scrapable


class Article(Scrapable):

    def __init__(self, title, url, session):
        self.title = title
        self.url = url
        self.session = session

    def __parse(self, html=None):
        soup = BeautifulSoup(html, "html.parser")

        # Get the article header
        header = soup.select_one(
            "#Modificado > div.ThemeGrid_Width10 > span").text

        # Get the article state
        state = soup.select_one("#ConsolidadoOrRevogado > span").text

        # Get the article text
        text = soup.select_one("#b10-b2-b2-InjectHTMLWrapper").text

        # Get the article changes
        # TODO: Implement changes
        changes = []

        return (header, state, text, changes)

    async def scrap(self):
        html = await self.session.get(BASE_URL_PREFIX.format(self.url))

        # Parse header, state, text and changes

        header, state, text, changes = self.__parse(html)

        self.header = header
        self.state = state
        self.text = text
        self.changes = changes

        print(self)

    def __repr__(self) -> str:
        return f"<Article {self.title}, {self.header}, {self.state}, {len(self.changes)} changes>"
