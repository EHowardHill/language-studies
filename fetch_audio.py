import os, sqlite3, csv, romkan
from gtts import gTTS

conn = sqlite3.connect('master_dict.db')
c = conn.cursor()
c.execute("select distinct kana, id from dictionary;")

for word in c.fetchall():
    my_path = str('./audio/ja/' + romkan.to_roma(word[0]).replace('/', ' ') + '.wav')
    if (not os.path.exists(my_path)):
        tts = gTTS(text=word[0], lang='ja')
        tts.save(my_path)
        print(romkan.to_roma(word[0]).replace('/', ' '))

c.close()