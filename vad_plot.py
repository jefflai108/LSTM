#!/usr/bin/env python
import numpy as np
np.seterr(divide='ignore', invalid='ignore')
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt 
from scipy.io import wavfile
import os 

fig = plt.figure()
###################################
plt.subplot(2, 1, 1)

indir = '/Users/jefflai108/clsp/spoken/flac_to_wav'
for root, dirs, filenames in os.walk(indir):
	for filename in filenames:
		if filename == 'flac_to_wav_0.wav': 
			samplerate, data = wavfile.read('/Users/jefflai108/clsp/spoken/flac_to_wav/'+filename)
		else: 
			samplerate, data0 = wavfile.read('/Users/jefflai108/clsp/spoken/flac_to_wav/'+filename)
			data = np.concatenate((data, data0))

t1 = np.linspace(0, len(data)/samplerate, len(data))

plt.plot(t1, data)
###################################
plt.subplot(2, 1, 2)

with open('vad_1.txt') as f: 
	content = f.readlines()
content = [x.strip() for x in content]

y = []
for count, element in enumerate(content):
	y = y + [int(x) for x in element.split("  ")[1][2:-2].split(' ')]


t2 = np.linspace(0, len(y)*10/1000, len(y))

plt.plot(t2, y)
####################################

fig.savefig('vad_temp3.png')

