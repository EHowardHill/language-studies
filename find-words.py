import os, pprint, sqlite3
import numpy as np
from collections import OrderedDict

con = sqlite3.connect('./full set/decomp.db')
c = con.cursor()

c.execute('select character, decomposition from decomp;')
data = c.fetchall()
data = {t[0]: t[1] for t in data}
words = []

def mood(t):
    s = ''
    if t in data.keys():
        tt = [y for y in data[t] if y != t]
        if len(tt) == 0:
            s += t
        else:
            for x in tt:
                s += mood(x)
    else:
        s += t
    return s

for t in data:
    words.append([t,mood(t)])

#pprint.pprint(words)

freqd = {}

def process(a,n=1):
    for t in range(len(a) - n + 1):
        bit = a[t:t+n]
        if bit not in freqd: freqd[bit] = 0
        freqd[bit] += 1
    if (n <= len(a)):
        process(a,n+1)

for all in words:
    process(all[1])

freq = [t for t in sorted(freqd, key=lambda k: (-freqd[k],-len(k))) if len(t) < freqd[t]]

frel = [t for t in sorted(freqd, key=lambda k: (-len(k),-freqd[k])) if len(t) < freqd[t]]

val = {}

for t in range(len(freq)):
    val[freq[t]] = str(np.base_repr(t,base=32))

#pprint.pprint(frel)

def conv(t):
    s = t
    for y in frel:
        if y in s:
            s = s.replace(y,val[y])
    return s

chi = sqlite3.connect('chitotz.db')
cho = chi.cursor()

for word in words:
    cho.execute(
        "insert or ignore into base (kanji, kana) values ('" + word[0] + "', '" + str(conv(word[1])) + "');")
    chi.commit()

chi.close()
con.close()