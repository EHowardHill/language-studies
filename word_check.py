import os, sqlite3, pprint, random

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

from pygame import mixer
from gtts import gTTS

conn = sqlite3.connect('master_dict.db')
c = conn.cursor()
c.execute("select distinct english, kana, kanji from dictionary where jlpt = 5;")
data = c.fetchall()

mixer.init()

data = [[d[0].split(','), d[1].split('/'), d[2].split('/')] for d in data]

while True:
    pop = random.choice(data)
    path = r'C:\Users\ethan\Documents\GitHub\language-studies\audio\ja\おとこ.mp3'

    #if not os.path.exists(path):
    #    tts = gTTS(text=pop[1][0], lang='ja')
    #    tts.save(path)

    # C:\Users\ethan\Documents\GitHub\language-studies\audio\ja\おとこ.mp3
    # C:/Users/ehill/Documents/GitHub/language-studies/audio/ja/おとこ.mp3

    mixer.music.load(path)
    mixer.music.play()

    print("英語で単語を書きます。")
    y = input()
    yy = ("...\n" + pop[0])
c.close()