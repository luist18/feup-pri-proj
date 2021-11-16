from bs4 import BeautifulSoup
from dre_scraper.config.urls import BASE_URL_PREFIX
from dre_scraper.model.article_version import ArticleVersion
from dre_scraper.model.scrapable import Scrapable


class Article(Scrapable):

    def __init__(self, title, url, session):
        self.title = title
        self.url = url
        self.session = session

    def __parse_versions(self, html):
        soup = BeautifulSoup(html, "html.parser")

        # Create versions array
        versions = []

        # Parse initial version
        initial_version_div = soup.select_one("#b10-b1-VersaoInicial")

        # Check if there are any versions
        if initial_version_div is None:
            return versions

        initial_version_text = initial_version_div.select_one(
            ".Fragmento_Texto > div > div").text

        initial_version = ArticleVersion(
            text=initial_version_text, initial=True)

        # Add initial version to the versions array
        versions.append(initial_version)

        # Parse versions
        version_divs = soup.select("#b10-b1-VersoesSeguintes > div > div")

        for div in version_divs:
            # Get article text
            text = div.select_one(".Fragmento_Texto > div > div").text

            # Get article details
            details = div.select_one(".ThemeGrid_Margin1First span").text

            # Create version
            version = ArticleVersion(text=text, details=details)

            # Add version to the versions array
            versions.append(version)

        return versions

    def __parse(self, html=None):
        soup = BeautifulSoup(html, "html.parser")

        # Get the article header
        header = soup.select_one(
            "#Modificado > div.ThemeGrid_Width10 > span").text

        # Get the article state
        state = soup.select_one("#ConsolidadoOrRevogado > span").text

        # Get the article text
        text = soup.select_one("#b10-b2-b2-InjectHTMLWrapper").text

        versions_count = len(soup.select(
            "div.list.list-group.OSFillParent > div"))

        return (header, state, text, versions_count)

    async def scrap(self):
        (html, versions_html) = await self.session.get_and_click(BASE_URL_PREFIX.format(self.url),
                                                                 "#b10-b2-b4-Alteracoes_Titulo > a", ["#b10-b1-b3-b3-InjectHTMLWrapper", ".Fragmento_Texto"])

        # Parse header, state and text
        header, state, text, versions_count = self.__parse(html)

        self.header = header
        self.state = state
        self.text = text

        # Parse versions
        versions = self.__parse_versions(versions_html)

        self.versions = versions

        print(self)

        if versions_count > 0 and len(self.versions) != versions_count + 1:
            print(
                f"Error in article ({len(self.versions)}/{versions_count + 1})", self)

    def __repr__(self):
        return f"<Article {self.title}, {self.header}, {self.state}, {len(self.versions)} versions>"
