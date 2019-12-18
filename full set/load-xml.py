import os, sqlite3, pprint, xmltodict, json
from tinydb import TinyDB, Query

conn = sqlite3.connect('jisho.db')
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

c.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(c.fetchall())

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

conn.close()