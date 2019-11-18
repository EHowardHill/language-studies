import os, sqlite3, pprint, random, subprocess
from google.cloud import texttospeech

conn = sqlite3.connect('master_dict.db')
c = conn.cursor()
c.execute("select distinct english, kana, kanji, romanji from dictionary where jlpt >= 4;")
data = c.fetchall()
path = 'C:/Users/ehill/Documents/GitHub/language-studies/audio/ja/'

client = texttospeech.TextToSpeechClient()
voice = texttospeech.types.VoiceSelectionParams(
    language_code='ja-JP',
    name="ja-JP-Wavenet-C",
    ssml_gender=texttospeech.enums.SsmlVoiceGender.NEUTRAL)
audio_config = texttospeech.types.AudioConfig(
    audio_encoding=texttospeech.enums.AudioEncoding.MP3)

data = [[d[0].split(','), d[1].split('/'), d[2].split('/'), d[3]] for d in data]

while True:
    pop = random.choice(data)

    my_path = str(path + pop[3] + '.mp3')

    synthesis_input = texttospeech.types.SynthesisInput(text=pop[1][0])
    response = client.synthesize_speech(synthesis_input, voice, audio_config)
    with open('output.mp3', 'wb') as out:
        out.write(response.audio_content)

    print("英語で単語を書きます。")
    y = input()
    yy = ("...\n")
    pprint.pprint(pop)
    print('\n\n')
c.close()