import os, sqlite3, pprint, xmltodict, json

conn = sqlite3.connect('jisho.db')
c = conn.cursor()

data = ""

print('step 1')
fr = []

json_data=open("jmdict_2.json")
data = json.load(json_data)

for key, value in data.items():
    pprint.pprint("Key:")
    pprint.pprint(key)

"""
char = []

with open('kradfile','r', encoding="euc_jp") as file:
    data = file.readlines()
    for ch in data:
        ch1 = ch.replace(' ','').split(':')
        if len(ch1) == 2 and '#' not in ch1[0]:
            char.append([ch1[0],ch1[1].replace('\n','')])

for r in char:
    c.execute("insert or ignore into decomp values ('" + r[0] + "','" + r[1] + "');")
"""

conn.commit()
conn.close()