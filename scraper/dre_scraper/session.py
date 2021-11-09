from pyppeteer import launch


async def create_session():
    browser = await launch(headless=True)
    page = await browser.newPage()

    session = Session(browser, page)

    return session


class Session():
    def __init__(self, browser, page):
        self.browser = browser
        self.page = page

    async def get(self, url):
        await self.page.goto(url, options={'waitUntil': 'networkidle2'})
        content = await self.page.content()

        return content

    async def close(self):
        await self.browser.close()
