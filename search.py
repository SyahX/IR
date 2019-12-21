from elasticsearch import Elasticsearch
from elasticsearch import helpers
import json
import sys
import numpy as np

es = Elasticsearch()

def search(keyword, size=5, tag=None):
    query = {
        # "size": 100,
        "query": {
            "match": {
                "words": keyword
            }
        },
    }
    results = es.search(index="foo", body=query, size=10)
    word_results = {}
    pos_table = {}
    for hit in results["hits"]["hits"]:
        # print (hit)
        score = hit["_score"]
        words = hit["_source"]["words"]
        tags = hit["_source"]["tags"]
        lens = len(words)
        for i, word in enumerate(words):
            if word == keyword:
                for j in range(max(i - size, 0),
                               min(i + size + 1, lens)):
                    if words[j] == keyword:
                        continue
                    elif tag != None and tags[j] not in tag:
                        continue
                    elif words[j] in word_results:
                        word_results[words[j]].append(score)
                    else:
                        word_results[words[j]] = [score]
                        pos_table[words[j]] = tags[j]
    for key in word_results:
        word_results[key] = np.mean(word_results[key])
    word_results = sorted(word_results.items(), key=lambda x: x[1])
    return word_results, pos_table

def main():
    word = "故事"
    results, pos_table = search(word)
    print (results)

if __name__ == "__main__":
    main()