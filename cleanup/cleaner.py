# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import math
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
    df.name = df.name.str.strip()
    df.parent_id = df.parent_id.fillna(-1)  # root section has parent -1
    df.parent_id = df.parent_id.astype(int)
    df.to_csv("data/cleanup/section.csv")


def articles(path):
    """
    Cleanup article.csv
    """
    df = pd.read_csv(path, index_col='id')

    groups = df['title'].str.extract(
        r'Artigo\s+(?P<key>\d+)\.º(?:\s+|-(?P<extra>\w)\s+)\(?(?P<title>.*?)\)?$', expand=True)
    groups['key'] = np.where(groups.extra.notna(
    ), groups.key + " " + groups.extra, groups.key)
    groups = groups.drop(['extra'], axis=1)

    df = df.drop(['title'], axis=1)
    df = df.join(groups)

    df['text'] = df["text"].apply(lambda text: "Revogado" if re.search(
        r'^\s*\(?Revogado\.?\)?\.?\s*(?:\\n)?$', text.strip(), re.IGNORECASE) is not None else text)

    df['state'].mask(df['text'] == 'Revogado', 'Revogado', inplace=True)
    print(df.state.describe())

    # separate into points
    points = _create_points(df)
    points.to_csv("data/cleanup/article_point.csv")
    df.to_csv("data/cleanup/article.csv")


def article_versions(path):
    """
    Cleanup article_version.csv
    """
    df = pd.read_csv(path, index_col='id')

    points = _create_points(df)
    points.to_csv("data/cleanup/article_version_point.csv")

    df.to_csv("data/cleanup/article_version.csv")


def _get_date(details):
    results = re.search(r'^.* (.+)$', details)
    if not results:
        return ''
    return results.group(1)


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
