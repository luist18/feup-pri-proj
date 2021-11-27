from cleanup import cleaner


def main():
    cleaner.books("data/book.csv")
    cleaner.sections("data/section.csv")
    cleaner.articles("data/article.csv")
    cleaner.article_versions("data/article_version.csv")


if __name__ == '__main__':
    main()
