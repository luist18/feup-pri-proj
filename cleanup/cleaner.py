# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import math
import re

pd.set_option('display.max_columns', None)


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
    df.name = df.name.str.strip()
    df.parent_id = df.parent_id.fillna(-1)  # root section has parent -1
    df.parent_id = df.parent_id.astype(int)
    df.to_csv("data/cleanup/section.csv")


def articles(articles_path, article_versions_path):
    """
    Cleanup article.csv and article_version.csv
    """
    articles = pd.read_csv(articles_path, index_col='id')

    # creates a new dataframe with the clear title and the key
    groups = articles['title'].str.extract(
        r'Artigo\s+(?P<key>\d+)\.º(?:\s+|-(?P<extra>\w)\s+)\(?(?P<title>.*?)\)?$', expand=True)
    groups['key'] = np.where(groups.extra.notna(
    ), groups.key + " " + groups.extra, groups.key)
    groups = groups.drop(['extra'], axis=1)

    # updates the title and key on the main dataframe
    articles = articles.drop(['title'], axis=1)
    articles = articles.join(groups)

    # sets the revogado state where it applies
    articles['text'] = articles["text"].apply(lambda text: "Revogado" if re.search(
        r'^\s*\(?Revogado\.?\)?\.?\s*(?:\\n)?$', text.strip(), re.IGNORECASE) is not None else text)

    articles['state'].mask(articles['text'] == 'Revogado',
                           'Revogado', inplace=True)

    # appends the versions
    article_versions = pd.read_csv(article_versions_path, index_col='id')
    articles = _join_article_versions(articles, article_versions)

    # creates the date field
    articles['date'] = None
    articles = articles.apply(_get_date, 1)

    # creates the article versions dataframe
    articles, article_versions = _create_article_versions(articles)

    # separates into points
    points = _create_points(articles)

    # saves all new dataframes
    points.to_csv("data/cleanup/article_point.csv")
    articles.to_csv("data/cleanup/article.csv")
    article_versions.to_csv("data/cleanup/article_version.csv", index=False)


def _get_date(row):
    if str(row.details) != 'nan':
        # gets the date from the end of the details
        # yyyy-mm-dd
        results = re.search(r'^.* (\d\d\d\d-\d\d-\d\d)$', row.details)
        row.date = results.group(1)
    
    return row


def _create_article_versions(articles):
    # creates the dataframes
    article_versions = pd.DataFrame(columns=['original', 'version'])
    articles = articles.copy()

    # creates the current column
    articles['current'] = False

    # goes through the dataframe in reverse order
    idx = len(articles)
    while idx > 0:
        # goes through all articles that have the same article_id
        article_id = articles.iloc[idx - 1].article_id

        current_idx = idx

        # sets the current article as current
        articles.iloc[current_idx - 1,
                      articles.columns.get_loc('current')] = True

        idx -= 1
        while idx > 0 and articles.iloc[idx - 1].article_id == article_id:
            # if the article id is the same, create a new entry
            article_versions = article_versions.append(
                {'original': current_idx, 'version': idx}, ignore_index=True)

            # updates the state
            articles.iloc[idx - 1,
                          articles.columns.get_loc('state')] = 'Alterado'

            idx -= 1

    # reverses the dataset
    article_versions = article_versions[::-1].reset_index(drop=True)

    # drops the no longer needed article_id
    articles = articles.drop(['article_id'], axis=1)

    return articles, article_versions


def _join_article_versions(articles, article_versions):
    res = articles.copy()

    # joins the version to the original dataframe
    # article_versions.article_id are joined with articles.id
    # drops the text because it already exists in the article_versions
    res = res.drop(['text'], axis=1)
    res = article_versions.join(res, on='article_id')

    return res


def _create_points(articles):
    df = pd.DataFrame(columns=['id', 'article_id', 'key', 'text'])

    id = 1

    # TODO cleanup revogado points

    for article_id, row in articles.iterrows():
        # sees if the text in the article has points
        # TODO is instance temporary (nan)
        if not isinstance(row.text, float) and re.search(r'1\.', row.text):
            # if it has points, split it into points
            points = _create_points_text(row.text)

            for point in points:
                df = df.append({
                    'id': id,
                    'article_id': article_id,
                    'key': point[0],
                    'text': point[1]
                }, ignore_index=True)

                id += 1
            articles.at[article_id, 'text'] = re.sub(
                '(\\n|\s)*(^|"|\\n)\d+(\.| -).*', '', row.text)

    df = df.set_index('id')

    return df


def _create_points_text(text):
    return re.findall(
        r'(?:^|"|\\n)(\d+)(?:\.| -) (.+?)(?=\s*(?:\\n(?:\\n|\d+)|"|$))', text)
