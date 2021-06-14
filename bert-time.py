from scipy import spatial
from sent2vec.vectorizer import Vectorizer
import pprint
import numpy as np
import math

data = [
    "Y'all get off your ass and work",
    "Everyone here is a hobo, you see"
    ]

def pea_pick(proto):
    sentences = []
    for t in range(len(proto)):
        p = list(proto)
        del p[t]
        sentences.append(p)
    return sentences

def group(input, n):
    return [input[i:i+n] for i in range(0, len(input), n)] 

def chunky(d):
    stat = group(d.split(' '),4)
    f = []
    for s in stat:
        f.extend(pea_pick(s))
    f = [ff for ff in f if len(ff) > 0]
    pairs = group(f, 2)
    pairs = [[' '.join(pp) for pp in p] for p in pairs]
    return pairs

for sent in data:

    sentences = chunky(sent)

    dist = []
    for p in sentences:
        print(p)
        if len(p) > 1:
            vectorizer = Vectorizer()
            vectorizer.bert(p)
            vectors_bert = vectorizer.vectors

            dist.append(spatial.distance.cosine(vectors_bert[0], vectors_bert[1]))
            print(dist[-1])

    avg = int(np.average(dist) * 1000000)

    print("Sentence: " + sent)
    print(avg)
    print()