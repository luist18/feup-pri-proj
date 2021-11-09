import asyncio

from dre_scraper.model.legislation import Legislation
from dre_scraper.parser import parse_legislation
from dre_scraper.session import create_session


async def __scrap_dre():
    session = await create_session()

    await parse_legislation(session)
    pass


def scrap():
    asyncio.get_event_loop().run_until_complete(__scrap_dre())
