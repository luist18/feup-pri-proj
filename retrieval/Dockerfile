FROM solr:8.11.0

ARG SCHEMA_TYPE
ENV SCHEMA_TYPE $SCHEMA_TYPE

COPY data/ /data

COPY schemas/ /schemas

COPY startup.sh /scripts/startup.sh

ENTRYPOINT ["/scripts/startup.sh"]
