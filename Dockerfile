FROM solr:8.11.0

COPY ./data/retrieval/article.json /data/article.json
COPY ./data/retrieval/article_point.json /data/article_point.json

COPY ./retrieval/simple_schema.json /data/simple_schema.json

COPY ./retrieval/startup.sh /scripts/startup.sh

ENTRYPOINT ["/scripts/startup.sh"]
