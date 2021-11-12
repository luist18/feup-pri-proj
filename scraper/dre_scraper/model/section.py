from bs4 import BeautifulSoup
from dre_scraper.config.urls import BASE_URL_PREFIX
from dre_scraper.model.scrapable import Scrapable


class Section(Scrapable):
    def __init__(self, name, sections_left):
        self.name = name
        self.sections_left = sections_left
        self.sections = []
        self.articles = []

    def __parse(self, html):
        """todo: documentation"""
        return None

    async def scrap(self):
        pass

    def __repr__(self):
        return f"<Section {self.name}, {len(self.sections)} sections, {len(self.articles)} articles>"
