import sqlite3, csv

conn = sqlite3.connect('master_dict.db')
c = conn.cursor()

with open('kanji.csv', newline='', encoding="utf8") as csvfile:
    s = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in s:
        print("insert into kanji (kanji, onyomi, kunyomi, english) values (\"" + row[0] + "\",\"" + row[1] + "\",\"" + row[2] + "\",\"" + row[3] + "\");")
        #c.execute("insert into dictionary (jlpt, kanji, kana, english) values (1, \"" + row[0] + "\",\"" + row[1] + "\",\"" + row[2] + "\");")
        c.execute("insert into kanji (kanji, onyomi, kunyomi, english) values (\"" + row[0] + "\",\"" + row[1] + "\",\"" + row[2] + "\",\"" + row[3] + "\");")
        conn.commit()

conn.close()

"""
c.execute('select * from dictionary limit 200')
print(c.fetchall())
"""