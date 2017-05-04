import numpy as np 

def open_vad_file(file):

	with open(file) as f: 
		content = f.readlines()
	content = [x.strip() for x in content]

	y = []
	for count, element in enumerate(content):
		if count == 1:
			break
		y = y + [int(x) for x in element.split("  ")[1][2:-2].split(' ')]				

	f = open('vad_matlab.txt', 'w')
	for item in y:
  		f.write("%d\n" % item)
	f.close() 

	return y

if __name__ == '__main__':
	open_vad_file('vad_1.txt')