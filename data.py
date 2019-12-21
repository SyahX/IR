from elasticsearch import Elasticsearch
from elasticsearch import helpers
import gc
import os

es = Elasticsearch()

data_path = "../data"
index = "foo"

files = os.listdir(data_path)
action = []
idx = 0
for file in files:
    if not file.endswith(".txt"):
        continue
    f = open(os.path.join(data_path, file), "r")
    for line in f:
        items = line.strip().split()
        words = []
        tags = []
        for item in items:
            try:
                word, tag = item.split("/")
                words.append(word)
                tags.append(tag)
            except ValueError:
                words.append(item[0])
                tags.append(item[-1])
        # print (words)
        # print (tags)
        action.append({
            "_id": idx,
            "_index": index,
            "_source": {
                "words": words,
                "tags": tags
            }
        })
        idx += 1
        if idx % 100000 == 0:
            print ("load %d ..." % idx)
            helpers.bulk(es, action, index="foo", raise_on_error=True)
            del action
            gc.collect()
            action = []
print ("total data: %d" % idx)

# 使用bulk批量导入数据

