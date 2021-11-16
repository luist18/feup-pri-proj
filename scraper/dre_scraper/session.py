import asyncio

from bs4 import BeautifulSoup
from pyppeteer import launch


async def create_session():
    browser = await launch(headless=True)

    session = Session(browser)

    return session


class Session():
    def __init__(self, browser):
        self.browser = browser

    async def get(self, url):
        # Open a new page
        page = await self.browser.newPage()

        # Navigate to url
        await page.goto(url, options={"waitUntil": "networkidle0"})
        # Get the page content
        content = await page.content()

        # Close the page
        await page.close()

        return content

    async def get_and_click(self, url, selector, wait_until):
        # Open a new page
        page = await self.browser.newPage()

        # Navigate to url
        await page.goto(url, options={"waitUntil": "networkidle0"})
        # Get the page content
        content = await page.content()

        # Check if the selector exists
        soup = BeautifulSoup(content, "html.parser")

        wait_until = list(
            map(lambda selector: page.waitForSelector(selector), wait_until))

        # If element exists, click it
        if soup.select_one(selector) is not None:
            # Click the element
            await asyncio.gather(
                page.click(selector),
                *wait_until,
            )

        # Get the page content
        content_after_click = await page.content()

        # Close the page
        await page.close()

        return (content, content_after_click)

    async def close(self):
        await self.browser.close()
