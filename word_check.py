import os, sqlite3, pprint, random, playsound

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
    path = ("C:/Users/ehill/Documents/GitHub/language-studies/audio/ja/" + pop[1][0] + ".mp3")

    if not os.path.exists(path):
        tts = gTTS(text=pop[1][0], lang='ja')
        tts.save(path)

    mixer.music.load(path)
    mixer.music.play()
    y = input(pop)
c.close()