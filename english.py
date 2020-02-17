import os, pprint, string, json, sqlite3

data = []
inds = {}
defs = {}
part = {}
deff = {}
index = 0

radicals = {}

print("Preparing data...")

with open('english.txt', 'r') as english:
    for eng in english.readlines():
        if eng != '\n':
            eng = eng.lower().split('@')
            data.append(eng)

print("Creating indexes...")

for d in data:
    if d[0] not in inds.keys():
        inds[d[0]] = index
        part[index] = d[1]
        try:
            deff[index] = d[2].translate(str.maketrans('', '', string.punctuation))
        except:
            deff[index] = ''
        index += 1

all_keys = inds.keys()

for d in data:
    key = inds[d[0]]
    try:
        this = [inds[t] for t in d[2].translate(str.maketrans('', '', string.punctuation)).split(' ') if t in all_keys]
        if key not in defs: defs[key] = {}
        for t in this:
            if t not in defs[key]:
                defs[key][t] = 1
            else:
                defs[key][t] += 1
    except:
        pass

with open('english_r.json', 'w', encoding='utf-8') as f:
    json.dump(defs, f, ensure_ascii=False, indent=4)

backw = {v: k for k, v in inds.items()}

for t in defs.keys():

    temp = {}
    for n in defs[t]:
        temp[n] = defs[t][n]

    for n in temp.keys():
        if not n in radicals:
            radicals[n] = temp[n]
        else:
            radicals[n] += temp[n]

rad = sqlite3.connect('english-radicals.db')
rcu = rad.cursor()

for t in radicals.keys():
    rcu.execute('insert or replace into word_count values (' + str(t) + ', "' + backw[t] + '", ' + str(radicals[t]) + ', "' + part[t] + '");')

for t in inds.keys():
    try:
        rcu.execute('insert or replace into word_index values (' + str(inds[t]) + ',"' + t + '", "' + part[inds[t]] + '", "' + deff[inds[t]] + '");')
    except:
        print('insert or replace into word_index values (' + str(inds[t]) + ',"' + t + '", "' + part[inds[t]] + '", "' + deff[inds[t]] + '");')
        yyy = input()

rad.commit()
rad.close()