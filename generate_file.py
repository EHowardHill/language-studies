import os, pprint
from scipy.io import wavfile
import numpy as np

en = []
audio = []

for file in os.listdir('hopper'):
    if 'en' in file:
        en.append(file[3:-4])

pprint.pprint(en)

def append_silence(duration_milliseconds=500):
    """
    Adding silence is easy - we add zeros to the end of our array
    """
    num_samples = duration_milliseconds * (sample_rate / 1000.0)

    for x in range(int(num_samples)): 
        audio.append(0.0)

    return

def append_bit(file):
    fs, data = wavfile.read(file)

    audio.append(data)

append_bit('./hopper/en ' + en[0] + '.wav')

for i in audio:
    wavfile.write('sleeping_rec.wav',44100,np.asarray(audio))