from elasticsearch import Elasticsearch
es = Elasticsearch()
index = 'foo'
query = {
    "query": {
        "match_all": {
        }
    }
}
es.delete_by_query(index=index, body=query)