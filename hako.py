from functools import total_ordering
import os, pprint, fugashi
from googletrans import Translator
translator = Translator()

tango = {}

with open("hakosan no me-seji rekishi.txt", "r", encoding="utf-8") as f:
    for l in f.readlines():
        tagger = fugashi.Tagger()
        words = [word.surface for word in tagger(l)]
        for w in words:
            if w in tango.keys():
                tango[w] += 1
            else:
                tango[w] = 1

with open("hako no kotae.txt", "w", encoding="utf-8") as w:
    for k in tango.keys():
        t = k + "\n"
        print(t)
        w.write(t)