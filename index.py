from elasticsearch import Elasticsearch

es = Elasticsearch()
index = 'foo'

# 自定义建立映射结构文件，很重要
mappings = {
    "settings" : {
        "index" : {
            "number_of_shards" : 5,
            "number_of_replicas" : 0
        },
    },
    "mappings":{
        "properties":{
            "words" : {
                "type" : "keyword",
            },
            "tags" : {
                "type" : "keyword",
            }
        }
    }
}

es.indices.create(index=index, ignore=[400, 404], body=mappings)