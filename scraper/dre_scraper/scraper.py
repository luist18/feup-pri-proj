import asyncio

from dre_scraper.model.legislation import Legislation
from dre_scraper.session import create_session


async def __scrap_legislation():
    session = await create_session()

    legislation = Legislation(session)
    pass


def scrap():
    asyncio.get_event_loop().run_until_complete(__scrap_legislation())
