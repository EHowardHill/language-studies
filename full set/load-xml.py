import os, sqlite3, pprint, xmltodict, json
from tinydb import TinyDB, Query

conn = sqlite3.connect('dict.db')
c = conn.cursor()

# Build a basic dictionary
with open('JMdict_e.xml', encoding='utf-8') as of:
    data = of.readlines()

tags = []
full_data = []
cache = {}
rele = []
kele = []
reno = []
sense = []
key = 0
keyname = ""

for d in data:

    d = d[:-1]
    if d == '<entry>':
        cache = {}
        key = 0
    elif d == '</entry>':
        full_data.append(cache)
    
    elif d == '<sense>':
        key = 1
        t = 0
        while 'sense_' + str(t) in cache: t += 1
        keyname = 'sense_' + str(t)
        cache[keyname] = []
    elif d == '</sense>':
        key = 0
        sense = []

    elif d == '<r_ele>':
        key = 2
        t = 0
        while 'r_ele_' + str(t) in cache: t += 1
        keyname = 'r_ele_' + str(t)
        cache[keyname] = []
    elif d == '</r_ele>':
        key = 0
        rele = []

    elif d == '<k_ele>':
        key = 3
        t = 0
        while 'k_ele_' + str(t) in cache: t += 1
        keyname = 'k_ele_' + str(t)
        cache[keyname] = []
    elif d == '</k_ele>':
        key = 0
        kele = []

    elif d == '<re_nokanji>':
        key = 4
        t = 0
        while 're_nokanji_' + str(t) in cache: t += 1
        keyname = 're_nokanji_' + str(t)
        cache[keyname] = []
    elif d == '</re_nokanji>':
        key = 0
        reno = []

    else:
        if key > 0:
            bit = d.replace('</','>').split('>')
            if (len(bit)) == 4:
                if 'lsource' not in bit[0]:
                    cache[keyname].append([bit[0][1:],bit[1]])

def retbit(t,bit):
    if bit in t:
        return json.dumps(t['r_ele_0'],ensure_ascii=False)
    else:
        return None

def pretty(x):
    if len(x) == 1:
        return '"' + x[0][1].replace('"','\'') + '"'
    elif len(x) == 0:
        return 'NULL'
    else:
        return '"' + json.dumps([y[1] for y in x],ensure_ascii=False).replace("\"","'") + '"'

perc = 0
size = len(full_data)
for bit in range(size):
    for o in range(0,5):
        if 'sense_' + str(o) in full_data[bit]:

            # Watch progress
            if int((bit / size) * 100) > perc:
                perc = int((bit / size) * 100)
                print(str(perc) + "%")

            t = [tt for tt in full_data[bit]['sense_' + str(o)] if tt != []]
            query = (
                'insert or ignore into sense (word_id, pos, expl, gloss, xref, misc, s_inf, dial, lit, field, stagr, ant, stagk, fig) values (' +
                str(bit) + ', ' +
                pretty([tt for tt in t if tt[0] == 'pos']) + ", " +
                pretty([tt for tt in t if tt[0] == 'gloss g_type="expl"']) + ", " +
                pretty([tt for tt in t if tt[0] == 'gloss']) + ", " +
                pretty([tt for tt in t if tt[0] == 'xref']) + ", " +
                pretty([tt for tt in t if tt[0] == 'misc']) + ", " +
                pretty([tt for tt in t if tt[0] == 's_inf']) + ", " +
                pretty([tt for tt in t if tt[0] == 'dial']) + ", " +
                pretty([tt for tt in t if tt[0] == 'gloss g_type="lit"']) + ", " +
                pretty([tt for tt in t if tt[0] == 'field']) + ", " +
                pretty([tt for tt in t if tt[0] == 'stagr']) + ", " +
                pretty([tt for tt in t if tt[0] == 'ant']) + ", " +
                pretty([tt for tt in t if tt[0] == 'stagk']) + ", " +
                pretty([tt for tt in t if tt[0] == 'gloss g_type="fig"']) +
                ');'
            )
            c.execute(query)
            conn.commit()

"""
size = len(full_data)
for bit in range(size):
    for o in range(0,1):
        if 'k_ele_' + str(o) in full_data[bit]:
            print (str(bit) + " / " + str(size))
            t = [tt for tt in full_data[bit]['k_ele_' + str(o)] if tt != []]
            query = (
                'insert or ignore into k_ele (word_id, keb, ke_pri, ke_inf) values (' +
                str(bit) + ', ' +
                pretty([tt for tt in t if tt[0] == 'keb']) + ", " +
                pretty([tt for tt in t if tt[0] == 'ke_pri']) + ", " +
                pretty([tt for tt in t if tt[0] == 'ke_inf']) +
                ');'
            )
            c.execute(query)
            conn.commit()
            """

"""
size = len(full_data)
for bit in range(size):
    for o in range(0,1):
        if 'r_ele_' + str(o) in full_data[bit]:
            print (str(bit) + " / " + str(size))
            t = [tt for tt in full_data[bit]['r_ele_0'] if tt != []]
            query = (
                'insert or ignore into r_ele (word_id, reb, re_pri, re_restr, re_inf) values (' +
                str(bit) + ', ' +
                pretty([tt for tt in t if tt[0] == 'reb']) + ", " +
                pretty([tt for tt in t if tt[0] == 're_pri']) + ", " +
                pretty([tt for tt in t if tt[0] == 're_restr']) + ", " +
                pretty([tt for tt in t if tt[0] == 're_inf']) +
                ');'
            )
            c.execute(query)
            conn.commit()
"""

"""
size = len(full_data)
for bit in range(size):
    print(str(bit) + " / " + str(size))
    t = full_data[bit]
    query = "insert or ignore into dict1 values (?,?,?,?,?,?,?,?,?,?,?);"
    c.execute(
        query,(
            str(bit),
            retbit(t,'r_ele_0'),
            retbit(t,'r_ele_1'),
            retbit(t,'sense_0'),
            retbit(t,'sense_1'),
            retbit(t,'sense_2'),
            retbit(t,'sense_3'),
            retbit(t,'sense_4'),
            retbit(t,'k_ele_0'),
            retbit(t,'k_ele_1'),
            retbit(t,'k_ele_2'))
        )
    conn.commit()
"""

conn.close()