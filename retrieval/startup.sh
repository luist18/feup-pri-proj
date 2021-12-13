#!/bin/bash

precreate-core articles

# Start Solr in background mode so we can use the API to upload the schema
solr start

sleep 10

if [[ ! -v SCHEMA_TYPE ]]; then
    echo "SCHEMA_TYPE is not set";
elif [[ -z "$SCHEMA_TYPE" ]]; then
    echo "SCHEMA_TYPE is not set";
elif [[  "$SCHEMA_TYPE" == "SCHEMALESS" ]]; then
    echo "Running SOLR in SCHEMALESS mode"
elif [[ "$SCHEMA_TYPE" == "SCHEMA" ]]; then
    echo "Running SOLR in SCHEMA mode"
    # Schema definition via API
    curl -X POST -H 'Content-type:application/json' \
        --data-binary @/schemas/schema_article.json \
        http://localhost:8983/solr/articles/schema
elif [[ "$SCHEMA_TYPE" == "SCHEMA_WITH_WEIGHTS" ]]; then
    echo "Running SOLR in SCHEMA mode"
    # Schema definition via API
    curl -X POST -H 'Content-type:application/json' \
        --data-binary @/schemas/schema_article_with_weights.json \
        http://localhost:8983/solr/articles/schema
else
    echo "SCHEMA_TYPE is not valid"; exit 1
fi

# Populate collection
bin/post -c articles /data/article.json

# Restart in foreground mode so we can access the interface
solr restart -f
