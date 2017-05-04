import numpy as np 

def concatenate(vad1, vad2):
	#Concatenate two vad text files 
	filenames = [vad1, vad2]
	with open('/Users/jefflai108/clsp/spoken/noise/final_baseline_vad.txt', 'w') as outfile:
	    for fname in filenames:
	        with open(fname) as infile:
	            for line in infile:
	                outfile.write(line)

def compare(ground_truth_vad, baseline_vad):
	#compare two vad file and output error rate 
	with open(ground_truth_vad) as f:
		ground_truth_content = f.readlines()
	ground_truth_content = [x.strip() for x in ground_truth_content]	

	with open(baseline_vad) as f:
		baseline_vad_content = f.readlines()
	baseline_vad_content = [x.strip() for x in baseline_vad_content]

	ground_truth_array = []
	for key, element in enumerate(ground_truth_content):
		A = [int(x) for x in element.split("  ")[1][2:-2].split(' ')]
		ground_truth_array = ground_truth_array + A

	baseline_array = []
	for key, element in enumerate(baseline_vad_content):
		A = [int(x) for x in element.split("  ")[1][2:-2].split(' ')]
		baseline_array = baseline_array + A

	error_rate = np.mean([ x!=y for (x,y) in zip(ground_truth_array, baseline_array)])
	print(error_rate)

	return error_rate 

if __name__ == '__main__':
	# concatenate('baseline_vad_1.txt','baseline_vad_2.txt')
	compare('final_vad.txt','final_baseline_vad.txt')