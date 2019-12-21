import os, sqlite3, pprint

jlpt = sqlite3.connect('master_dict.db')
jlpc = jlpt.cursor()

jlpc.execute("select jlpt, kanji from dictionary where kanji is not null and kanji is not '';")
base_data = jlpc.fetchall()

bdic = sqlite3.connect('./full set/dict.db')
dcur = bdic.cursor()

spot = 0
size = len(base_data)
for t in range(size):
    if int((t / size) * 100) > spot:
        spot = int((t / size) * 100)
        print(spot)
    dcur.execute("update k_ele set jlpt = " + str(base_data[t][0]) + " where keb = '" + base_data[t][1] + "';")
    bdic.commit()

jlpt.close()