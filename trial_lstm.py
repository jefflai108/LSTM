from __future__ import print_function

from keras.models import Sequential
from keras.layers import Dense, LSTM, TimeDistributed
import pickle 
import numpy as np 

def data_to_file():

	X_train = open_mfcc_file('mfcc_1.txt') #718 #1724
	Y_train = open_vad_file('vad_1.txt') 
	X_validation = open_mfcc_file('mfcc_2.txt') #711 #1698
	Y_validation= open_vad_file('vad_2.txt') 
	X_test = open_mfcc_file('mfcc_3.txt') #714 #1712
	Y_test = open_vad_file('vad_3.txt') 
	
	#Store X, Y in a seperate file
	file_Name = "X_Ys"
	f = open(file_Name, "wb")
	pickle.dump(X_train, f)
	pickle.dump(Y_train, f)
	pickle.dump(X_validation, f)
	pickle.dump(Y_validation, f)
	pickle.dump(X_test, f)
	pickle.dump(Y_test, f)
	f.close()

def lstm():

	batch_size = 32

	print('Loading data...') 
	X_train = open_mfcc_file('mfcc_1.txt') #718, 1724
	X_validation = open_mfcc_file('mfcc_2.txt') #711, 1698
	X_test = open_mfcc_file('mfcc_3.txt') #714, 1712
	Y_train, Y_validation, Y_test = open_vad_file('vad_all.txt', 718, 711, 714)

	print('Build model...')
	model = Sequential()
	model.add(LSTM(128, dropout=0.2, recurrent_dropout=0.2, input_shape=(None,20), return_sequences=True))
	model.add(TimeDistributed(Dense(1, activation='sigmoid')))

	# try using different optimizers and different optimizer configs
	model.compile(loss='binary_crossentropy',
	              optimizer='adam',
	              metrics=['accuracy'])

	print('Train...')
	model.fit(X_train, Y_train,
	          batch_size=batch_size,
	          epochs=15,
	          validation_data=(X_validation, Y_validation))
	# model.fit_generator()
	score, acc = model.evaluate(X_test, Y_test,
	                            batch_size=batch_size)
	print('Test score:', score)
	print('Test accuracy:', acc)
"""
def generator(mfcc_file, vad_file, batch_size)
"""
# outputs a tuple (inputs, targets, sample_weights). All arrays should contain the same number of samples. 
# The generator is expected to loop over its data indefinitely. 
# An epoch finishes when steps_per_epoch samples have been seen by the model.

"""	
	with open(mfcc_file) as f:
		content = f.readlines()

	max_frame = 0
	recordings = 0
	for count, element in enumerate(content):
		if element[-2] is "[":
			i = 0
			recordings += 1
		else: 
			i += 1
			if element[-2] is "]" and i > max_frame: 
				max_frame = i

	assert recordings > batch_size

	inputs = np.zeros((batch_size, max_frame, 20), dtype='float32')

	i,j = 0,0
	for count, element in enumerate(content):
		if element[-2] is "[":
			continue
		else:
			x_train[i,j,:] = np.asarray([float(x) for x in element.split(" ")[2:-1]])
			j += 1
			if element[-2] is "]":
				j=0
				i += 1

	return x_train
"""
def open_mfcc_file(file):

	with open(file) as f:
		content = f.readlines()

	max_frame = 0
	recordings = 0
	for count, element in enumerate(content):
		if element[-2] is "[":
			i = 0
			recordings += 1
		else: 
			i += 1
			if element[-2] is "]" and i > max_frame: 
				max_frame = i

	print(recordings) #718
	print(max_frame) #1724

	x_train = np.zeros((recordings, max_frame, 20), dtype='float32')
	print(x_train.shape)

	i,j = 0,0
	for count, element in enumerate(content):
		if element[-2] is "[":
			shit += 1 
			continue
		else:
			x_train[i,j,:] = np.asarray([float(x) for x in element.split(" ")[2:-1]])
			j += 1
			if element[-2] is "]":
				j=0
				i += 1
	
	# print(x_train[717,1723])
	#print(x_train.ndim)
	return x_train

def open_vad_file(file, train_size, validation_size, test_size):

	with open(file) as f: 
		content = f.readlines()
	content = [x.strip() for x in content]

	train_max_frame = 0 
	validation_max_frame = 0
	test_max_frame = 0 
	for count, element in enumerate(content):
		if count < train_size: 
			dummy = 0
			for _ in [int(x) for x in element.split("  ")[1][2:-2].split(' ')]:
				dummy += 1
			if dummy > train_max_frame: train_max_frame = dummy 
		elif count < (train_size + validation_size): 
			dummy = 0
			for _ in [int(x) for x in element.split("  ")[1][2:-2].split(' ')]:
				dummy += 1
			if dummy > validation_max_frame: validation_max_frame = dummy 
		elif count < (train_size + validation_size + test_size):
			dummy = 0
			for _ in [int(x) for x in element.split("  ")[1][2:-2].split(' ')]:
				dummy += 1
			if dummy > test_max_frame: test_max_frame = dummy			

	print(train_max_frame) #1724
	print(validation_max_frame) #1698
	print(test_max_frame) #1712

	y_train = np.zeros((train_size, train_max_frame, 1), dtype='int')
	y_validation = np.zeros((validation_size, validation_max_frame, 1), dtype='int')
	y_test = np.zeros((test_size, test_max_frame, 1), dtype='int')

	for count, element in enumerate(content):
		if count < train_size:
			A = [int(x) for x in element.split("  ")[1][2:-2].split(' ')]
			for j, x in enumerate(A):
				y_train[count, j] = x
		elif count < (train_size + validation_size):
			A = [int(x) for x in element.split("  ")[1][2:-2].split(' ')]
			for j, x in enumerate(A):
				y_validation[count-train_size, j] = x
		elif count < (train_size + validation_size + test_size):
			A = [int(x) for x in element.split("  ")[1][2:-2].split(' ')]
			for j, x in enumerate(A):
				y_test[count-train_size-validation_size, j] = x					

	return y_train, y_validation, y_test 

if __name__ == '__main__':
	# open_vad_file('vad_all.txt', 718, 711, 714)
	# open_mfcc_file('mfcc_all.txt')
	lstm()
