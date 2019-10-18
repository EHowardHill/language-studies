import os, sqlite3, csv
from gtts import gTTS

print()

conn = sqlite3.connect('master_dict.db')
c = conn.cursor()
c.execute("select distinct english, id from dictionary;")

for word in c.fetchall():
    my_path = str('./audio/en/' + str(word[1]) + '.mp3')
    if not os.path.exists(my_path):
        try:
            tts = gTTS(text=word[0], lang='en')
            tts.save(my_path)
        except: pass

c.close()