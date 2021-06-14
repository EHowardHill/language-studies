import os, pprint, pickle, time, math, sys, glob
import tensorflow as tf
import numpy as np

def pad(x, l):
    return x + [0 for _ in range(l - len(x))]

token = {0:''}
setup = []
l = 0
with open("cmudict-0.7b.txt", "r") as o:
    for oo in o.readlines():
        if oo[0].isalpha():
            ks = []
            vs = []
            for k in oo.split(" ")[0]:
                if k not in token.keys(): token[k] = len(token)
                ks.append(token[k])
            for v in oo.split(" ")[1:]:
                if v not in token.keys(): token[v] = len(token)
                vs.append(token[v])
            if len(ks) > l: l = len(ks)
            if len(vs) > l: l = len(vs)
            setup.append([ks,vs])

nekot = dict((v,k) for k,v in token.items())

def func(arg):
    return tf.convert_to_tensor(arg, dtype=tf.int32)  

tensors = []

for t in setup:
    tt = tf.convert_to_tensor([pad(t[0],l),pad(t[1],l)], dtype=tf.int32)
    tensors.append(tt)

dataset = tf.data.Dataset.from_tensors(tensors)

pprint.pprint(len(dataset))