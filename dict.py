import gc
import os
import gensim
import time
import json

data_path = "../data"
BLOCK = 10000000
files = os.listdir(data_path)
word2tag = {}
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

        idx += 1
        for i, word in enumerate(words):
            if word not in word2tag:
                word2tag[word] = tags[i]
        if idx % BLOCK == 0:
            print ("load %d" % idx)

# print (word2tag)
with open("./word2tag.txt", "w") as f:
    json.dump(word2tag, f)

# with open("./word2tag.txt", "r") as f:
#     word2tag = json.load(f)
# print (word2tag)

print ("total data: %d, %d" % (idx, len(word2tag)))
