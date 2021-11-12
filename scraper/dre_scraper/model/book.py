from dre_scraper.model.scrapable import Scrapable


class Book(Scrapable):
    def __init__(self, name, url, session):
        self.name = name
        self.url = url
        self.session = session

    def __parse(self, html):
        """todo: documentation"""
        pass

    async def scrap(self):
        """todo: documentation"""
        pass

    def __repr__(self):
        return f"<Book {self.name}, {self.url}>"
