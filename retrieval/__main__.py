from datetime import datetime

import pandas as pd

articles_read = 0


def main():
    """
    Main function.
    """
    # reads the data CSVs
    article = pd.read_csv('data/cleanup/article.csv', index_col='id')
    book = pd.read_csv('data/cleanup/book.csv', index_col='id')
    section = pd.read_csv('data/cleanup/section.csv', index_col='id')

    article_final = create_article_documents(article, book, section)

    article_final = article_final.drop(['id'], axis=1)

    with open('data/retrieval/article.json', 'w', encoding='utf-8') as file:
        article_final.to_json(file, orient='records',
                              force_ascii=False, indent=4)


def create_article_documents(article, book, section):
    print("Articles")
    df = article.copy()

    # drops unnecessary columns
    df = df.drop(['header', 'initial', 'current'], axis=1)

    # creates paths
    # TODO shit algorithm this one
    df = df.apply(lambda row: _create_path(row, book, section, df), axis=1)
    print(f'\r100%        ')

    df = df.drop(['section_id', 'article_id'], axis=1)

    return df


def _create_path(row, book, section, articles):
    global articles_read
    articles_read = articles_read + 1
    if articles_read % 100 == 0:
        print(f'\r{round(articles_read / len(articles) * 100, 2)}%', end='')

    path = []

    # creates a column named id with the section id
    section['id'] = section.index

    # gets the section
    section_id = row['section_id']

    # gets the section row with the section id
    section_row = section[section.id == section_id].iloc[0]
    path = [section_row['name']] + path

    while section_row.parent_id != -1:
        section_row = section[section.id == section_row.parent_id].iloc[0]
        path = [section_row['name']] + path

    # get the book row according to the root_section_id
    book_row = book[book.root_section_id == section_row.id].iloc[0]

    row['id'] = row.name
    row['path'] = path
    row['book'] = book_row['name']
    row['book_url'] = book_row['url']

    return row


if __name__ == '__main__':
    main()
