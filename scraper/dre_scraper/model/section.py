from dre_scraper.model.article import Article
from dre_scraper.model.book_entry import BookEntryType
from dre_scraper.model.scrapable import Scrapable


class Section(Scrapable):

    def __init__(self, name, entries, depth, session):
        self.name = name
        self.entries = entries
        self.depth = depth
        self.session = session
        self.sections = []
        self.articles = []

    def __parse(self, html=None):
        # Enumerate entries

        current_section = None

        sections = []
        articles = []

        for entry in self.entries:
            if entry.depth == self.depth + 1:
                # New section or article
                if entry.type == BookEntryType.SECTION:
                    # Create new section and append to the list
                    current_section = Section(
                        entry.name, [], entry.depth, self.session)

                    sections.append(current_section)
                else:
                    # Create article new article and append to the list
                    article = Article(entry.name, entry.url, self.session)

                    articles.append(article)
            elif entry.depth >= self.depth:
                # Entries inside a section
                current_section.entries.append(entry)

        return (sections, articles)

    async def scrap(self):
        # Parse section and articles with the entries
        sections, articles = self.__parse()

        self.sections = sections
        self.articles = articles

        # Scrap all sections
        for section in self.sections:
            await section.scrap()

        # Scrap all articles
        for article in self.articles:
            await article.scrap()

    def __repr__(self):
        return f"<Section {self.name}, {len(self.sections)} sections, {len(self.articles)} articles>"
