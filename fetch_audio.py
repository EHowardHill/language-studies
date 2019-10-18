import os, sqlite3, csv
from gtts import gTTS

conn = sqlite3.connect('master_dict.db')
c = conn.cursor()
c.execute("select distinct kana from dictionary;")

for word in c.fetchall():
    my_path = str('./audio/ja/' + word[0].replace('\n','') + '.mp3')
    if not os.path.exists(my_path):
        try:
            tts = gTTS(text=word[0], lang='ja')
            tts.save(my_path)
        except: pass

c.close()