import numpy as np 
import os
from glob import glob


def vad_check():
	with open('new_vad_1.txt') as f: 
		content = f.readlines()
	content = [x.strip() for x in content]


	fileList = [y for x in os.walk('/Users/jefflai108/clsp/spoken/noise/new_flac_data/') for y in glob(os.path.join(x[0], '*.flac'))]
	match = []
	for file in fileList: 
		match.append(file.split('/')[9].split('.')[0])

	test = []
	for count, element in enumerate(content):
		if element.split("  ")[0] not in match: 
			print(count) # 0,1,202,207
		test.append(element.split("  ")[0])

	assert len(match) == len(test)


if __name__ == '__main__':
	vad_check()