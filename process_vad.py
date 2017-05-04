import numpy as np 

def process_vad(fileID):

	with open(fileID) as f: 
		content = f.readlines()
	content = [x.strip() for x in content]

	for count, element in enumerate(content):
		y = []		
		y = y + [int(x) for x in element.split("  ")[1][2:-2].split(' ')]	
		i = element.split("  ")[0]
		f = open('/Users/jefflai108/clsp/spoken/noise/vad_data_2/'+str(i)+'.txt', 'w')
		for item in y:
	  		f.write("%d\n" % item)
		f.close() 

if __name__ == '__main__':
	process_vad('real_vad_2.txt')