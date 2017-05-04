import numpy as np 

def vad_order(mfcc_file, vad_file):
	#vad and mfcc should have the same order so x_train and y_train can match 	
	#return the stored vad key 
	with open(mfcc_file) as f:			
		mfcc_content = f.readlines()

	with open(vad_file) as f: 
		vad_content = f.readlines()

	mfcc_key = []
	for count, element in enumerate(mfcc_content):
		if element[-2] is "[":
			mfcc_key.append(element.split("  ")[0])

	vad_key = []
	for count, element in enumerate(vad_content):
		vad_key.append(element.split("  ")[0])

	#sort vad according to mfcc order 
	sorted_vad_key = []
	for i in mfcc_key: 
		# print(i)
		sorted_vad_key.append(i)

	return sorted_vad_key

def check_order(vadFile,mfccFile): 
	#vad and mfcc should have the same order so input and output can match 	
	with open(vadFile) as f: 
		vad_content = f.readlines()
	vad_content = [x.strip() for x in vad_content]

	with open(mfccFile) as f: 
		mfcc_content = f.readlines()

	mfcc_key = []
	for count, element in enumerate(mfcc_content):
		if element[-2] is "[":
			# print(element.split("  ")[0])
			mfcc_key.append(element.split("  ")[0])

	vad_key = []
	for count, element in enumerate(vad_content):
		# print(element.split("  ")[0])
		vad_key.append(element.split("  ")[0])

	sorted_vad_key = vad_order(mfccFile, vadFile)
	print(sorted_vad_key)
	assert mfcc_key == sorted_vad_key, "Keys are not in the same order"

	# assert mfcc_key == vad_key, "Keys are not in the same order"


if __name__ == '__main__':
	check_order('final_vad.txt','final_mfcc.txt')