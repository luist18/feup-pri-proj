#!/bin/bash

precreate-core articles
precreate-core article_points

# Start Solr in background mode so we can use the API to upload the schema
solr start

# Schema definition via API
curl -X POST -H 'Content-type:application/json' \
    --data-binary @/data/simple_schema.json \
    http://localhost:8983/solr/articles/schema

# Populate collection
bin/post -c articles /data/article.json
bin/post -c article_points /data/article_point.json

# Restart in foreground mode so we can access the interface
solr restart -f
