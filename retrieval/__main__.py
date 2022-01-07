from datetime import datetime
import json

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


def _get_presidents():
    with open("data/presidents/presidents.json", "r") as file:
        presidents = json.load(file)

    for president in presidents:
        president['date_start'] = datetime.strptime(
            president['date_start'], '%B %d, %Y')

        if 'Incumbent' in president['date_end']:
            president['date_end'] = None
        else:
            president['date_end'] = datetime.strptime(
                president['date_end'], '%B %d, %Y')

    return presidents

def _binary_search(presidents, date):
    # binary search on the presidents list
    left = 0
    right = len(presidents) - 1

    while left <= right:
        middle = (left + right) // 2
        president = presidents[middle]

        if ((president['date_start'] <= date and president['date_end'] is None) or president['date_start'] <= date <= president['date_end']):
            return presidents[middle]
        elif president['date_start'] > date:
            right = middle - 1
        else:
            left = middle + 1

    return None


def _add_president(row, presidents):
    # transforms the date to a datetime object
    article_date = row['date']
    article_date = datetime.strptime(article_date, '%Y-%m-%d')

    # binary search on the presidents list
    president = _binary_search(presidents, article_date)

    # adds the president to the row
    if president is not None:
        row['president_name'] = president['name']
        row['president_party'] = president['political_party']

    return row

def create_article_documents(article, book, section):
    print("Articles")
    df = article.copy()

    # reads the presidents json
    presidents = _get_presidents()

    # drops unnecessary columns
    df = df.drop(['header', 'initial', 'current'], axis=1)

    # creates paths
    # TODO shit algorithm this one
    df = df.apply(lambda row: _create_path(row, book, section, df), axis=1)
    df = df.apply(lambda row: _add_president(row, presidents), axis=1)
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
