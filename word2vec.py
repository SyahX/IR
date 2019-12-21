import gc
import os
import gensim

data_path = "../data"

files = os.listdir(data_path)
sentences = []
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
        sentences.append(words)
        if idx % 100000 == 0:
            break
print ("total data: %d" % idx)

print ("--- train model ---")
model = gensim.models.Word2Vec(sentences, size=128, window=3, min_count=5, workers=40, iter=40)
model.wv.save_word2vec_format("got_word2vec.txt", binary=False)

