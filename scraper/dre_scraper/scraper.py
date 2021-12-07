import asyncio

from dre_scraper.model.legislation import Legislation
from dre_scraper.session import create_pyppeteer_session as create_session


async def __scrap_legislation():
    session = await create_session()

    legislation = Legislation(session)

    await legislation.scrap()

    return legislation


def scrap():
    legislation = asyncio.get_event_loop().run_until_complete(__scrap_legislation())

    return legislation
