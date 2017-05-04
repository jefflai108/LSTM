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

indir = '/Users/jefflai108/clsp/spoken/'
for root, dirs, filenames in os.walk(indir):
	for filename in filenames:
		if filename == '103-1240-0000.wav': 
			samplerate, data = wavfile.read('/Users/jefflai108/clsp/spoken/'+filename)
		# if filename == '103-1240-0001.wav': 
		# 	samplerate, data0 = wavfile.read('/Users/jefflai108/clsp/spoken/'+filename)
		# 	data = np.concatenate((data, data0))
		# if filename == '1040-133433-0004.wav': 
		# 	samplerate, data1 = wavfile.read('/Users/jefflai108/clsp/spoken/'+filename)
		# 	data = np.concatenate((data, data1))
		# if filename == '1040-133433-0009.wav': 
		# 	samplerate, data2 = wavfile.read('/Users/jefflai108/clsp/spoken/'+filename)
		# 	data = np.concatenate((data, data2))

t1 = np.linspace(0, len(data)/samplerate, len(data))

plt.plot(t1, data)
###################################
plt.subplot(2, 1, 2)

with open('new_new_vad_1.txt') as f: 
	content = f.readlines()
content = [x.strip() for x in content]

y = []
for count, element in enumerate(content):
	if element.split("  ")[0] == '103-1240-0000':
		y = y + [int(x) for x in element.split("  ")[1][2:-2].split(' ')]
	# if element.split("  ")[0] == '103-1240-0001':
	# 	y = y + [int(x) for x in element.split("  ")[1][2:-2].split(' ')] 
	# if element.split("  ")[0] == '1040-133433-0004':
	# 	y = y + [int(x) for x in element.split("  ")[1][2:-2].split(' ')]
	# if element.split("  ")[0] == '1040-133433-0009':
	# 	y = y + [int(x) for x in element.split("  ")[1][2:-2].split(' ')]

t2 = np.linspace(0, len(y)*10/1000, len(y))

plt.plot(t2, y)
####################################

fig.savefig('vad_temp8.png')

