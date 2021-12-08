# Solr Server

## Building

```sh
docker build . -t pri_solr
```

## Running

```sh
docker run -p 5001:8983 -d -e SCHEMA_TYPE=<type> pri_solr
```
