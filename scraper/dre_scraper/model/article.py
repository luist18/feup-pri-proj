from bs4 import BeautifulSoup
from dre_scraper.config.urls import BASE_URL_PREFIX
from dre_scraper.model.article_version import ArticleVersion
from dre_scraper.model.scrapable import Scrapable


class Article(Scrapable):

    id = 1

    def __init__(self, title, url, session):
        self.title = title
        self.url = url
        self.session = session

        self.header = None
        self.state = None
        self.text = None
        self.versions = []

        # Set id and increment it
        self.id = Article.id
        Article.id += 1

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
            ".Fragmento_Texto > div > div").text.replace("\n", "\\n")

        initial_version = ArticleVersion(
            text=initial_version_text, initial=True)

        # Add initial version to the versions array
        versions.append(initial_version)

        # Parse versions
        version_divs = soup.select("#b10-b1-VersoesSeguintes > div > div")

        for div in version_divs:
            # Get article text
            text = div.select_one(
                ".Fragmento_Texto > div > div").text.replace("\n", "\\n")

            # Get article details
            details = div.select_one(
                ".ThemeGrid_Margin1First span").text.replace("\n", "\\n")

            # Create version
            version = ArticleVersion(text=text, details=details)

            # Add version to the versions array
            versions.append(version)

        return versions

    def __parse(self, html=None):
        soup = BeautifulSoup(html, "html.parser")

        # Get the article header
        header = soup.select_one(
            "#Modificado > div.ThemeGrid_Width10 > span").text.replace("\n", "\\n")

        # Get the article state
        state = soup.select_one("#ConsolidadoOrRevogado > span").text

        # Get the article text
        text_element = soup.select_one(
            "#b10-b2-b2-InjectHTMLWrapper")

        if text_element is None:
            text_element = soup.select_one(
                "#b10-b2-Texto")

        text = text_element.text.replace("\n", "\\n")

        versions_count = len(soup.select(
            "div.list.list-group.OSFillParent > div"))

        return (header, state, text, versions_count)

    async def scrap(self):
        # TODO: fix this spaghetti code
        versions_html = None

        try:
            (html, versions_html) = await self.session.get_and_click(BASE_URL_PREFIX.format(self.url),
                                                                     "#b10-b2-b4-Alteracoes_Titulo > a", ["#b10-b1-b3-b3-InjectHTMLWrapper", ".Fragmento_Texto"])
        except:
            html = await self.session.get(BASE_URL_PREFIX.format(self.url))

        # Parse header, state and text
        header, state, text, versions_count = self.__parse(html)

        self.header = header
        self.state = state
        self.text = text

        # Parse versions
        if versions_html is None:
            versions = []
        else:
            versions = self.__parse_versions(versions_html)

        self.versions = versions

        print(self)

    def __repr__(self):
        return f"<Article {self.title}, {self.header}, {self.state}, {len(self.versions)} versions>"
