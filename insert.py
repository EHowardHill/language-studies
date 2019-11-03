import sqlite3, csv, pprint, romkan

conn = sqlite3.connect('master_dict.db')
c = conn.cursor()

"""
with open('kanji.csv', newline='', encoding="utf8") as csvfile:
    s = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in s:
        print("insert into kanji (kanji, onyomi, kunyomi, english) values (\"" + row[0] + "\",\"" + row[1] + "\",\"" + row[2] + "\",\"" + row[3] + "\");")
        #c.execute("insert into dictionary (jlpt, kanji, kana, english) values (1, \"" + row[0] + "\",\"" + row[1] + "\",\"" + row[2] + "\");")
        c.execute("insert into kanji (kanji, onyomi, kunyomi, english) values (\"" + row[0] + "\",\"" + row[1] + "\",\"" + row[2] + "\",\"" + row[3] + "\");")
        conn.commit()

conn.close()
"""

c.execute(r"select distinct kana, id from dictionary;")
data = [d[0] for d in c.fetchall()]

for d in data:
    c.execute("update dictionary set romanji = '" + romkan.to_roma(d).replace('/',' ').replace('\'',' ') + "' where kana = '" + d + "';")

conn.commit()
conn.close()