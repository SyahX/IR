from elasticsearch import Elasticsearch
from elasticsearch import helpers
import json
import sys
from copy import copy
import numpy as np
from gensim.models import KeyedVectors

from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

es = Elasticsearch()

tags2name = {
    "n": "名词", "np": "人名", "ns": "地名", "ni": "机构名", "nz": "其它专名",
    "m": "数词", "q": "量词", "mq": "数量词", "t": "时间词", "f": "方位词", "s": "处所词",
    "v": "动词", "a": "形容词", "d": "副词", "h": "前接成分", "k": "后接成分", "i": "习语",
    "j": "简称", "r": "代词", "c": "连词", "p": "介词", "u": "助词", "y": "语气助词",
    "e": "叹词", "o": "拟声词", "g": "语素", "w": "标点", "x": "其它"
}

idx2tags = [key for key in tags2name]
tags2show = {
    "tags2name": tags2name,
    "idx2tags": idx2tags,
    "flag": [True for i in range(28)]
}

with open("./word2tag.txt", "r") as f:
    word2tag = json.load(f)
wv = KeyedVectors.load_word2vec_format('got_word2vec.txt', binary=False)

def NewScore(score, i, j):
    if j < i:
        return score
    else:
        return score # / abs(i - j)

def sim(keyword):
    print (wv.most_similar(['man']))

def search(keywords, size=5, tag=None):
    query = {
        "query": {
            "bool": {
                "must": []
            }
        },
    }
    keywords = keywords.split()
    for keyword in keywords:
        query['query']['bool']['must'].append({'match': {'words' : keyword}})
    results = es.search(index="foo", body=query, size=10000)
    word_results = {}
    pos_table = {}
    for hit in results["hits"]["hits"]:
        # print (hit)
        score = hit["_score"]
        words = hit["_source"]["words"]
        tags = hit["_source"]["tags"]
        lens = len(words)

        sim = []
        for word in words:
            cnt = 0
            for keyword in keywords:
                cnt += wv.similarity(word, keyword)
            sim.append(cnt)
        total_sim = np.sum(sim) + 1e-8

        for i, word in enumerate(words):
            if word in keywords:
                for j in range(max(i - size, 0),
                               min(i + size + 1, lens)):
                    if words[j] in keywords:
                        continue
                    elif tag != None and tags[j] not in tag:
                        continue
                    elif words[j] in word_results:
                        word_results[words[j]].append(score * sim[j] / total_sim)
                    else:
                        word_results[words[j]] = [score * sim[j] / total_sim]
                        pos_table[words[j]] = tags[j]
    for key in word_results:
        word_results[key] = np.mean(word_results[key])
    word_results = sorted(word_results.items(), key=lambda x: x[1], reverse=True)
    results = []
    for word, score in word_results:
        results.append({"word": word, "score": score, "tag": tags2name[pos_table[word]]})
    return results

@app.route('/', methods=['POST', 'GET'])
@app.route('/search', methods=['POST', 'GET'])
def foo():
    if request.method =='POST':
        keywords = request.form['keyword']
        size = int(request.form['window'])
        tag_idxs = request.form.getlist('tags')
        info = {'query': keywords}
        tags2show["flag"] = [False for i in range(28)]
        tags = []
        for idx in tag_idxs:
            idx = int(idx)
            tags2show["flag"][idx] = True
            tags.append(tags2show["idx2tags"][idx])
        results = search(keywords, size=size, tag=tags)
        return render_template('foo.html', keywords=keywords, window=size, results=results, tags2show=tags2show)
    return render_template('foo.html', tags2show=tags2show)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='6006', debug=True)
    # sim("Y")
