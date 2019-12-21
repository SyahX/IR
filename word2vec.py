import gc
import os
import gensim
import time

data_path = "../data"
BLOCK = 10000
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
        if idx % BLOCK == 0:
            print ("")
print ("total data: %d, %d" % (idx, idx // BLOCK))

print ("--- build model ---")
ptr_time = time.time()
model = gensim.models.Word2Vec(size=128, window=5, min_count=5, workers=40, iter=40)
model.build_vocab(sentences)
total = time.time() - ptr_time
print ("Total time: %.4f" % (total / 60.0))

print ("--- train model ---")
ptr_time = time.time()
length = len(sentences)
for i in range(length // BLOCK):
    model.train(sentences[i * BLOCK, (i + 1) * BLOCK])
    total = time.time() - ptr_time
    print ("Total time[%d]: %.4f" % ((i + 1) * BLOCK, total / 60.0))

print ("--- save model ---")
ptr_time = time.time()
model.wv.save_word2vec_format("got_word2vec.txt", binary=False)
total = time.time() - ptr_time
print ("Total time: %.4f" % (total / 60.0))



