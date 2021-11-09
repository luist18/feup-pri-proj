import dre_scraper.config.urls as request_urls
from dre_scraper.model import Article, Book


async def parse_legislation(session):
    print(await session.get(request_urls.LEGISLATION_URL))
    pass
