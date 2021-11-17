import pandas as pd
import re


def books(path):
    """
    Cleanup book.csv
    """
    df = pd.read_csv(path, index_col='id')
    df.to_csv("data/cleanup/book.csv")


def sections(path):
    """
    Cleanup section.csv
    """
    df = pd.read_csv(path, index_col='id')
    df['name'] = df['name'].apply(lambda str: '"{}"'.format(str.strip()))
    df.to_csv("data/cleanup/section.csv")


def _create_points(articles):
    df = pd.DataFrame(columns=['article_id', 'key', 'text'])

    for article_id, row in articles.iterrows():
        # sees if the text in the article has points
        if re.search(r'1\.', row.text):
            # if it has points, split it into points
            points = re.findall(
                r'(?:^|"|\\n)(\d+)(?:\.| -) (.+?)(?=\s*(?:\\n(?:\\n|\d+)|"|$))', row.text)

            for point in points:
                df = df.append({
                    'article_id': article_id,
                    'key': point[0],
                    'text': point[1]
                }, ignore_index=True)

            articles.at[article_id, 'text'] = re.sub('(\\n|\s)*(^|"|\\n)\d+(\.| -).*', '', row.text)
    df.to_csv("data/cleanup/point.csv")


def articles(path):
    """
    Cleanup article.csv
    """
    df = pd.read_csv(path, index_col='id')
    df['key'] = df.apply(lambda row: re.search(
        r' (\d+).º', row.title).group(1), axis=1)
    df['title'] = df.apply(lambda row: re.search(
        r'\(.*\)', row.title).group().replace('(', '"').replace(')', '"'), axis=1)

    # separate into points
    points = _create_points(df)

    print(df)
    df.to_csv("data/cleanup/article.csv")
