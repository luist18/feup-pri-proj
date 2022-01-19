import requests

def query(query):
    x = requests.get(
        url="http://localhost:5002/solr/articles/select",
        params={
            "defType": "edismax",
            "qf": "key^10 title_raw^1.5 title^1 text_raw^1.5 text^1 path^1 book^3",
            "pf": "title_raw^1.5 title^1 text_raw^1.5 text^1 path^1 book^3",
            "bq": "state:Consolidado^4",
            "tie": "1.0",
            "q": query,
            "start": 0,
            "rows": 20
        }
    )

    return _parse_articles(x.json()['response']['docs'])


def _parse_articles(articles):
    # gets the last element of a list
    return [build_article(article['book'], article['key'], article['path'][-1], article['date']) for article in articles]

def build_article(book, key, last_path, date):
    return "{}/{}/{}/{}".format(book, key, last_path, date)
