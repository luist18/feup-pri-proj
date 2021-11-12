from bs4 import BeautifulSoup

from dre_scraper.model.article import Article
from dre_scraper.model.book_entry import BookEntryType
from dre_scraper.config.urls import BASE_URL_PREFIX
from dre_scraper.model.scrapable import Scrapable


class Section(Scrapable):
    
    def __init__(self, name, entries, depth, session):
        self.name = name
        self.entries = entries
        self.depth = depth
        self.session = session
        self.sections = []
        self.articles = []

    def __parse(self, html=None):
        # Enumerate entries

        current_section = None

        for entry in entries:
            if entry.depth == self.depth + 1:
                if entry.type == BookEntryType.SECTION:
                    current_section = Section(entry.name, [], entry.depth, self.session)
                else:
                    # create article
                    article = Article(entry.name, entry.url, self.session)
                    
                    self.articles.append(article)
            elif entry.depth >= self.depth:
                current_section.entries.append(entry)

        return (sections, articles)

    async def scrap(self):
        # There is no section parsing
        self.__parse()
        print(f"Scraping section {self.name}")

    def __repr__(self):
        return f"<Section {self.name}, {len(self.sections)} sections, {len(self.articles)} articles>"
