from __future__ import print_function
# from sklearn.preprocessing import StandardScaler

from keras.models import Sequential
from keras.layers import Dense, LSTM, TimeDistributed

import numpy as np 
np.seterr(divide='ignore', invalid='ignore')

def concatenate(mfcc1, mfcc2, vad1, vad2):
	#Concatenate two mfcc text files and two vad text files 
	filenames = [mfcc1, mfcc2]
	with open('/Users/jefflai108/clsp/spoken/noise/final_mfcc.txt', 'w') as outfile:
	    for fname in filenames:
	        with open(fname) as infile:
	            for line in infile:
	                outfile.write(line)

	filenames = [vad1, vad2]
	with open('/Users/jefflai108/clsp/spoken/noise/final_vad.txt', 'w') as outfile:
	    for fname in filenames:
	        with open(fname) as infile:
	            for line in infile:
	                outfile.write(line)

def lstm():

	batch_size = 32

	print('Loading data...') 
	X_train, X_validation, X_test, Train_mask, Val_mask, Test_mask = open_mfcc_file('final_mfcc.txt',1001,143,286)
	Y_train, Y_validation, Y_test = open_vad_file('final_mfcc.txt','final_vad.txt',1001,143,286)
	# X_test, X_train, X_validation, Test_mask, Train_mask, Val_mask = open_mfcc_file('final_mfcc.txt',286,1001,143)
	# Y_test , Y_train, Y_validation = open_vad_file('final_mfcc.txt','final_vad.txt',286,1001,143)

	print('Build model...')
	model = Sequential()
	model.add(TimeDistributed(Dense(128, activation='relu'), input_shape=(None,20)))
	model.add(LSTM(128, dropout=0.5, recurrent_dropout=0.5, input_shape=(None,20), return_sequences=True))
	model.add(LSTM(128, dropout=0.5, recurrent_dropout=0.5, input_shape=(None,20), return_sequences=True))
	# model.add(LSTM(128, dropout=0.2, recurrent_dropout=0.2, input_shape=(None,20), return_sequences=True))
	# model.add(LSTM(128, dropout=0.2, recurrent_dropout=0.2, input_shape=(None,20), return_sequences=True))
	model.add(TimeDistributed(Dense(1, activation='sigmoid')))

	# try using different optimizers and different optimizer configs
	model.compile(loss='binary_crossentropy',
	              optimizer='adam',
	              metrics=['accuracy'],
	              sample_weight_mode="temporal")

	print('Train...')
	model.fit(X_train, Y_train,
	          batch_size=batch_size,
	          epochs=15,
	          sample_weight=Train_mask,
	          validation_data=(X_validation, Y_validation, Val_mask))
	# model.fit_generator()
	score, acc = model.evaluate(X_test, Y_test,
								sample_weight=Test_mask,
	                            batch_size=batch_size)
	print('Test score:', score)
	print('Test accuracy:', acc)

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


def open_mfcc_file(file, train_size, validation_size, test_size):

	with open(file) as f:
		content = f.readlines()

	train_max_frame = 0 
	validation_max_frame = 0
	test_max_frame = 0 
	recordings = 0
	for count, element in enumerate(content):
		if recordings < train_size:
			if element[-2] is "[":
				i = 0
				recordings += 1
			else: 
				i += 1
				if element[-2] is "]" and i > train_max_frame: 
					train_max_frame = i
		elif recordings < (train_size + validation_size):
			if element[-2] is "[":
				i = 0
				recordings += 1
			else: 
				i += 1
				if element[-2] is "]" and i > validation_max_frame: 
					validation_max_frame = i
		elif recordings < (train_size + validation_size + test_size):
			if element[-2] is "[":
				i = 0
				recordings += 1
			else: 
				i += 1
				if element[-2] is "]" and i > test_max_frame: 
					test_max_frame = i

	assert recordings == (train_size + validation_size + test_size), 'recordings number not equivalent'
	print(train_max_frame) #1709
	print(validation_max_frame) #1710
	print(test_max_frame) #1724

	x_train = np.zeros((train_size, train_max_frame, 20), dtype='float32')
	x_validation = np.zeros((validation_size, validation_max_frame, 20), dtype='float32')
	x_test = np.zeros((test_size, test_max_frame, 20), dtype='float32')

	train_mask = np.zeros((train_size, train_max_frame), dtype='int')
	val_mask = np.zeros((validation_size, validation_max_frame), dtype='int')
	test_mask = np.zeros((test_size, test_max_frame), dtype='int')

	recordings = 0
	i,j,m,l = 0,0,0,0
	for count, element in enumerate(content):
		if recordings < train_size: 
			if element[-2] is "[":
				recordings += 1
				continue
			else:
				x_train[i,j,:] = np.asarray([float(x) for x in element.split(" ")[2:-1]])
				train_mask[i,j] = 1
				j += 1
				if element[-2] is "]":
					j=0
					i += 1
		elif recordings < (train_size + validation_size):
			if element[-2] is "[":
				recordings += 1
				continue
			else:
				x_validation[m,j,:] = np.asarray([float(x) for x in element.split(" ")[2:-1]])
				val_mask[m,j] = 1
				j += 1
				if element[-2] is "]":
					j=0
					m += 1
		elif recordings < (train_size + validation_size + test_size):
			if element[-2] is "[":
				recordings += 1
				continue
			else:
				x_test[l,j,:] = np.asarray([float(x) for x in element.split(" ")[2:-1]])
				test_mask[l,j] = 1
				j += 1
				if element[-2] is "]":
					j=0
					l += 1			

	#Normalization for each recording

	# print(d.shape) (1709, 20)
	# print(train_mask.shape) (431, 1709) 
	count = 0
	for d in x_train: 
		mean = np.mean(d[train_mask[count],:], axis=0)
		std = np.std(d[train_mask[count],:], axis=0)
		# print("mean is", mean)
		# print("std is", std)
		for i in d:
			i = (i-mean)/std
		count += 1

	count = 0
	for d in x_validation: 
		mean = np.mean(d[val_mask[count],:], axis=0)
		std = np.std(d[val_mask[count],:], axis=0)
		for i in d:
			i = (i-mean)/std
		count += 1

	count = 0
	for d in x_test: 
		mean = np.mean(d[test_mask[count],:], axis=0)
		std = np.std(d[test_mask[count],:], axis=0)
		for i in d:
			i = (i-mean)/std
		count += 1

	# scaler = StandardScaler()

	# for d in x_train: 
	# 	d = scaler.partial_fit(d).transform(d)

	# for d in x_validation: 
	# 	d = scaler.partial_fit(d).transform(d)

	# for d in x_test: 
	# 	d = scaler.partial_fit(d).transform(d)

	return x_train, x_validation, x_test, train_mask, val_mask, test_mask

def open_vad_file(mfcc_file, vad_file, train_size, validation_size, test_size):

	sorted_vad_key = vad_order(mfcc_file, vad_file)

	with open(vad_file) as f: 
		content = f.readlines()
	content = [x.strip() for x in content]

	train_max_frame = 0 
	validation_max_frame = 0
	test_max_frame = 0
	counter = 0 
	for key in sorted_vad_key:
		for count, element in enumerate(content):
			if element.split("  ")[0] == key and counter < train_size:
				counter += 1
				dummy = 0
				for _ in [int(x) for x in element.split("  ")[1][2:-2].split(' ')]:
					dummy += 1
				if dummy > train_max_frame: train_max_frame = dummy 
			elif element.split("  ")[0] == key and counter < (train_size + validation_size):
				counter += 1
				dummy = 0
				for _ in [int(x) for x in element.split("  ")[1][2:-2].split(' ')]:
					dummy += 1
				if dummy > validation_max_frame: validation_max_frame = dummy 
			elif element.split("  ")[0] == key and counter < (train_size + validation_size + test_size):
				counter += 1
				dummy = 0
				for _ in [int(x) for x in element.split("  ")[1][2:-2].split(' ')]:
					dummy += 1
				if dummy > test_max_frame: test_max_frame = dummy 

	print(train_max_frame) #1709
	print(validation_max_frame) #1710
	print(test_max_frame) #1724

	y_train = np.zeros((train_size, train_max_frame, 1), dtype='int')
	y_validation = np.zeros((validation_size, validation_max_frame, 1), dtype='int')
	y_test = np.zeros((test_size, test_max_frame, 1), dtype='int')

	counter = 0 
	for key in sorted_vad_key: 
		for count, element in enumerate(content):
			if element.split("  ")[0] == key and counter < train_size:
				A = [int(x) for x in element.split("  ")[1][2:-2].split(' ')]
				for j, x in enumerate(A):
					y_train[counter, j] = x
				counter += 1
			elif element.split("  ")[0] == key and counter < (train_size + validation_size):
				A = [int(x) for x in element.split("  ")[1][2:-2].split(' ')]
				for j, x in enumerate(A):
					y_validation[counter-train_size, j] = x
				counter += 1
			elif element.split("  ")[0] == key and counter < (train_size + validation_size + test_size):
				A = [int(x) for x in element.split("  ")[1][2:-2].split(' ')]
				for j, x in enumerate(A):
					y_test[counter-train_size-validation_size, j] = x					
				counter += 1

	return y_train, y_validation, y_test 

if __name__ == '__main__':
	# vad_order('final_mfcc.txt','final_vad.txt')
	# open_mfcc_file('noisy_mfcc_1.txt',431,145,145)
	# open_vad_file('noisy_mfcc_1.txt','vad_1.txt',431,145,145)
	# concatenate('mfcc_1.txt', 'mfcc_2.txt', 'real_vad_1.txt', 'real_vad_2.txt')
	lstm()