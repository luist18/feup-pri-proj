import requests

from dre_scraper.parser import parse_books
from dre_scraper.model.legislation import Legislation


def scrap_dre():
    parse_books()
    pass
