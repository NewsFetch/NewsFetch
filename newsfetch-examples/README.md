# What can be built with NewsFetch?

## News Search Engine

### OpenSearch

A search engine for News content can be built with [OpenSearch](https://opensearch.org).

#### Installation

```
docker pull opensearchproject/opensearch:2.3.0

docker run -p 9200:9200 -p 9600:9600 -e "discovery.type=single-node" opensearchproject/opensearch:2.3.0
```

More information can be found [here](https://opensearch.org/downloads.html).

### Traditional Keyword Search

A prototype keyword search engine, built with [Elasticsearch](https://www.elastic.co/),
using the data enriched by the [newsfetch-enrichers](../newsfetch-enrichers) project,
is described below.

Follow along with the documentation in the [opensearch-news-search](./opensearch-news-search) directory.

### Vector Search

A vector search engine, again built with [Elasticsearch](https://www.elastic.co/), 
from the data enriched by the [newsfetch-enrichers](../newsfetch-enrichers) project,
is described below.

Follow along with the documentation in the [opensearch-news-vector-search](./opensearch-news-vector-search) directory.
