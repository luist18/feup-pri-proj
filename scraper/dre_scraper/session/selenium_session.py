from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup


async def create_session():
    browser = webdriver.Chrome()

    return Session(browser)


class Session():
    def __init__(self, browser):
        self.browser = browser
        self.browser.implicitly_wait(2)

    async def get(self, url, wait_until=[], delay=3):
        if len(wait_until) > 0:
            self.browser.get(url)
        else:
            for element in wait_until:
                self.browser.find_element_by_css_selector(element)

        content = self.browser.page_source

        return content

    async def get_and_click(self, url, selector, wait_until=[], wait_for_function=[]):
        content = await self.get(url)

        try:
            # Check if the selector exists
            soup = BeautifulSoup(content, "html.parser")

            if soup.select_one(selector) is not None:
                # Click the element
                for element in wait_until:
                    self.browser.find_element_by_css_selector(element)

            # Get the page content
            content_after_click = self.browser.page_source

            return (content, content_after_click)
        except:
            return (content, None)

    async def close(self):
        self.browser.quit()
