#!/usr/bin/env python 
import numpy as np 
import matplotlib as mpl
mpl.use('Agg')
from matplotlib import pyplot as plt 
import numpy as np 

with open("vad_1.txt") as f:
    content = f.readlines()
content = [x.strip() for x in content]

#for count, element in enumerate(content): 
#	y.append(element.split("  ")[1])  

y = [int(x) for x in content[0].split("  ")[1][2:-2].split(' ')]

print(y)
fig = plt.figure()
bins = np.linspace(0, 100000, 200000)
plt.hist(y, bins, alpha=0.65, label='vad_1')
fig.show()
fig.savefig('vad_temp.png')
