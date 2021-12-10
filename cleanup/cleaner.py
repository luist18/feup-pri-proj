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
    print("### ARTICLES ###")
    print("Reading csv...")
    articles = pd.read_csv(articles_path, index_col='id')

    print("Extracting key and title...")
    # creates a new dataframe with the clear title and the key
    groups = articles['title'].str.extract(
        r'Artigo\s+(?P<key>\d+)\.º(?:\s+|-(?P<extra>\w)\s+)\(?(?P<title>.*?)\)?$', expand=True)
    groups['key'] = np.where(groups.extra.notna(
    ), groups.key + " " + groups.extra, groups.key)
    groups = groups.drop(['extra'], axis=1)

    # updates the title and key on the main dataframe
    articles = articles.drop(['title'], axis=1)
    articles = articles.join(groups)

    print("Updating revogados...")
    # sets the revogado state where it applies
    articles['text'] = articles["text"].apply(lambda text: "Revogado" if re.search(
        r'^\s*\(?Revogado\.?\)?\.?\s*(?:\\n)?$', text.strip(), re.IGNORECASE) is not None else text)

    articles['state'].mask(articles['text'] == 'Revogado',
                           'Revogado', inplace=True)

    print("Appending versions...")
    # appends the versions
    article_versions = pd.read_csv(article_versions_path, index_col='id')
    article_versions['title'] = article_versions['title'].apply(
        lambda title: re.search(r'^\(?(.+?)\)?(?:\\n)?$', title).group(1))
    article_versions = article_versions.drop_duplicates(
        subset=['article_id', 'text', 'title'], keep='last')
    articles = _join_article_versions(articles, article_versions)

    print("Creating dates...")
    # creates the date field
    articles['date'] = None
    articles = articles.apply(_get_date, 1)

    print("Creating article versions dataframe...")
    # creates the article versions dataframe
    articles, article_versions = _create_article_versions(articles)

    # finally fixes the index column
    articles.index.name = 'id'
    articles = articles.drop(['id'], axis=1)

    print("Creating points...")
    # separates into points
    points = _create_points(articles)

    # cleans the \n
    articles.text = articles.text.str.strip()
    articles.text = articles.text.str.replace(r'\\n$', '')
    points.text = points.text.str.strip()
    points.text = points.text.str.replace(r'\\n$', '')

    print("Saving...")
    # saves all new dataframes
    points.to_csv("data/cleanup/article_point.csv")
    articles.to_csv("data/cleanup/article.csv")
    article_versions.to_csv("data/cleanup/article_version.csv", index=False)

    print("Done!\n")


def _get_date(row):
    if str(row.details) != 'nan':
        # gets the date from the end of the details
        # yyyy-mm-dd
        results = re.search(r'^.* (\d\d\d\d-\d\d-\d\d)$', row.details)
        row.date = results.group(1)
    elif str(row.header) != 'nan':
        # gets the date from the end of the header
        # yyyy-mm-dd
        results = re.search(r'^.* (\d\d\d\d-\d\d-\d\d)$', row.header)
        row.date = results.group(1)

    return row


def _create_article_versions(articles):
    # creates the dataframes
    article_versions = pd.DataFrame(columns=['original', 'version'])
    articles = articles.copy()

    # goes through the dataframe
    idx = 1
    while idx <= len(articles):
        # goes through all articles that have the same article_id
        article_id = articles.iloc[idx - 1].article_id
        articles_for_id = []

        # gets the articles that have the same article_id
        while idx <= len(articles) and articles.iloc[idx - 1].article_id == article_id:
            articles_for_id.append(articles.iloc[idx - 1])
            idx += 1

        # gets the IDs of the currents
        current_ids = [
            article.id for article in articles_for_id if article.current]
        assert len(
            current_ids) == 1, "There should be only one current article for each article_id"
        current_id = current_ids[0]

        # sets the current article as current
        articles.iloc[current_id - 1,
                      articles.columns.get_loc('current')] = True

        # creates all entries
        # creates auxiliary list with IDs
        ids = [article.id for article in articles_for_id]
        # drops the current article
        ids.remove(current_id)
        # creates the entries
        for article in ids:
            article_versions = article_versions.append(
                {'original': current_id, 'version': article}, ignore_index=True)

    return articles, article_versions


def _join_article_versions(articles, article_versions):
    res = articles.copy()
    res['article_id'] = res.index

    # appends the versions to the original dataframe
    # ignore_index so that the indexes of the new (old) articles' index comes after the original ones
    article_versions.index += res.index.max() + 1
    res = res.append(article_versions)

    # creates the current table
    # this one is False for all old articles and True for the current one (one per article_id)
    res['current'] = False

    # updates section_id, header, key, and title according to article_id
    # also updates the state to 'Alterado'
    res['id'] = res.index
    res = res.apply(lambda row: _update_article_id(row, res), axis=1)

    # removes the original articles that originally appeared in the versions
    # if the article_id is the same, it means that the article_id and the text are the same
    # if they are the same, given the parse in the last operation, the one with more information is the article_version
    #     this is, the 'last'
    global remove
    res = res[~res.id.isin(remove)]

    # in order to restore the original order, we need to sort by article_id
    res = res.sort_values(by=['article_id'], ignore_index=True)

    # fixes wrong types
    # section_id and article_id should be ints instead of floats
    res.section_id = res.section_id.astype(int)
    res.article_id = res.article_id.astype(int)

    # sets ID as index
    res.index += 1
    res['id'] = res.index

    return res


global remove
remove = []


def _update_article_id(row, articles):
    # if that's an original article then it does not need to do this operation
    if str(row.initial) == 'nan':
        row.initial = True
        row.current = True
        return row

    original = articles[articles.index == row.article_id].iloc[0]

    # updates section_id, header, and key according to article_id
    row.section_id = original.section_id
    row.header = original.header
    row.key = original.key

    # the state of old articles is 'Alterado'

    if row.text == original.text and row.title == original.title:
        row.state = original.state
        row.current = True

        global remove
        remove.append(original.id)
    else:
        row.state = 'Alterado'
        row.current = False

    return row


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
