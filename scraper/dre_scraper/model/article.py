from dre_scraper.model.scrapable import Scrapable


class Article(Scrapable):
    
    def __init__(self, title, url, session):
        self.title = title
        self.url = url
        self.session = session

    def __parse(self, html=None):
        pass

    def scrap(self):
        pass
