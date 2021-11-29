# -*- coding: utf-8 -*-

from cleanup import cleaner


def main():
    cleaner.books("data/scraper/book.csv")
    cleaner.sections("data/scraper/section.csv")
    cleaner.articles("data/scraper/article.csv")
    cleaner.article_versions("data/scraper/article_version.csv")


if __name__ == '__main__':
    main()
