from cleanup import cleaner

def main():
    cleaner.books("data/scraper/book.csv")
    cleaner.sections("data/scraper/section.csv")
    cleaner.articles("data/scraper/article.csv")

if __name__ == '__main__':
    main()