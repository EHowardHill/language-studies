import sqlite3, csv, pprint

conn = sqlite3.connect('master_dict.db')
ci = conn.cursor()
ci.execute(r"select distinct kanji, decomp, english from kanji;")
kan = {d[0]:str(d[1]).replace('[','').replace(']','').replace('\'','') for d in ci.fetchall()}

phoneme = "ㄚㄧㆲロユ56789フブプㆠㄆㄇㄉㄌㄑㄫンシ1"
phon = {}

convert = {
    "ㄚ":"a",
    "ㄧ":"i",
    "ㆲ":"e",
    "ロ":"o",
    "ユ":"u",
    "5":"ya",
    "6":"yi",
    "7":"ye",
    "8":"yo",
    "9":"yu",
    "フ":"h",
    "ブ":"b",
    "プ":"p",
    "ㆠ":"s",
    "ㄆ":"ch",
    "ㄇ":"m",
    "ㄉ":"d",
    "ㄌ":"zh",
    "ㄑ":"k",
    "ㄫ":"r",
    "ン":"ts",
    "シ":"j",
    "1":"t"
}

minus = 0
t = 0
while (t-minus) < 461:
    o = t
    out = ""
    while o >= len(phoneme):
        div = int(o / len(phoneme))
        rem = o % len(phoneme)
        out = out + phoneme[rem]
        o = div
    out = out + phoneme[o]
    if (len([o for o in out if phoneme.index(o) < 11]) < 5) and (len([o for o in out if phoneme.index(o) >= 11]) < 5) and (len(out) > 1 and out[0] != out[1]):
        phon[t-minus] = out
        #print(str(t-minus) + '\t' + str([convert[o] for o in out]))
    else:
        minus += 1
    t += 1

"""
minus = 0
for t in range(0,461):
    o = t
    out = ""
    while o >= len(phoneme):
        out += phoneme[int(o / len(phoneme)) % len(phoneme)]
        o = o / len(phoneme)
    out += phoneme[t%len(phoneme)]
    if (len([o for o in out if phoneme.index(o) < 6]) < 3):
        phon[t - minus] = out
        print(str(t) + '\t' + str([convert[o] for o in out]))
    else:
        minus += 1
"""

freq = {}

def process(c,f='-'):
    res = []
    if str(c) in kan.keys():
        if kan[c] != "None":
            for k in kan[c]:
                res += process(k,('\t' + f))
        else:
            res += c
    else:
        res += c
    return res

all_res = []
for k in kan.keys():
    res = []
    for c in k:
        res += process(c,'\t-')

    if 'N' not in res:
        all_res.append([k,res])

print(" === ")
#pprint.pprint(phon)

for res in all_res:
    for r in res[1]:
        if r in freq.keys():
            freq[r] += 1
        else:
            freq[r] = 1

freq = sorted(freq.items(), key=lambda x: x[1])
#pprint.pprint(freq)
#print(len(freq))

chitotz = {}

for han in all_res:
    ci.execute("select english from kanji where kanji = '" + han[0] + "';")
    eng = ci.fetchone()[0]

    new_str = ""
    for y in han[1]:
        new_str += phon[[len(freq) - freq.index(x) for x in freq if x[0] == y][0]]
    #print(han[0] + '\t' + new_str)

    roman = "".join([convert[t] for t in new_str])
    roman = roman.replace('ii','sh').replace('eiy','g').replace('iuiu','\'').replace('iu','ng').replace('ioio','f')

    if len(roman) > 16:
        roman = (roman[:12] + " (" + roman[12:] + ")")
    else:
        roman = (roman)

    com = ("insert or ignore into chitotzish values (\"" + eng + "\", \"" + han[0].replace(' ','') + "\", \"" + roman + "\");")
    #print(com)
    conn.execute(com)
    conn.commit()

conn.close()