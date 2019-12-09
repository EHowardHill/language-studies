import sqlite3, csv, pprint

conn = sqlite3.connect('sentences.db')
c = conn.cursor()

batch = []

print("Loading batch...")

with open('sentences.csv', newline='', encoding="utf8") as csvfile:
    s = csv.reader(csvfile, delimiter='\t', quotechar='"')
    for row in s:
        batch.append(row)

print("Done with batching...")

for row in batch:
    try:
        c.execute("insert or ignore into master values (\"" + row[2] + "\",\"" + row[0] + "\",\"" + row[1] + "\");")
    except:
        pass

conn.commit()
conn.close()

"""
decomp = []

c.execute(r"select distinct radical from radical;")
data = [d[0] for d in c.fetchall()]
pprint.pprint(data)

def getBool(b):
    return '1' if b else '0'

with open('kangxiradical.csv', newline='', encoding="utf8") as csvfile:
    s = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in s:
        decomp.append([
            row[1][1],
            '1' if row[2] == 'V' else '0',
            '1' if 'T' in row[3] else '0',
            '1' if 'C' in row[3] else '0',
            '1' if 'J' in row[3] else '0',
            '1' if 'K' in row[3] else '0',
            '1' if 'V' in row[3] else '0'
        ])

for d in decomp:
    com = ("insert into radical values (\"" +
        d[0] + "\"," +
        d[1] + "," +
        d[2] + "," +
        d[3] + "," +
        d[4] + "," +
        d[5] + "," +
        d[6] +
        ");")
    print(com)
    c.execute(com)
"""

#for d in decomp:
    #com = "update kanji set decomp = '" + d[1] + "' where kanji = '" + d[0] + "';"
    #c.execute(com)

"""
with open('freq-kanji.txt','r', encoding='utf-8') as f:
    all_kan = f.readlines()
    all_kan = [[t.replace('\n',''),all_kan.index(t)] for t in all_kan]

for kan in all_kan:
    pass
    #com = "update kanji set pop = " + str(kan[1]) + " where kanji = '" + kan[0] + "';"
    #c.execute(com)

for d in data:
    c.execute("update dictionary set romanji = '" + romkan.to_roma(d).replace('/',' ').replace('\'',' ') + "' where kana = '" + d + "';")
"""

#conn.commit()
#conn.close()