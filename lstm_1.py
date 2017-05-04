from __future__ import print_function

import numpy as np 
from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM

#maxlen = 80  # cut texts after this number of words (among top max_features most common words)
batch_size = 32

print('Loading data...')
####### Training data ##############
with open('mfcc_1.txt') as f:
	content = f.readlines()

x_train = []
for count, element in enumerate(content):
	if element[-2] is "[":
		continue
	else:
		x_train.append([float(x) for x in element.split(" ")[2:-1]])

x_train = np.vstack(x_train)

with open('vad_1.txt') as f: 
	content = f.readlines()
content = [x.strip() for x in content]

y_train = []
for count, element in enumerate(content):
	y_train = y_train + [int(x) for x in element.split("  ")[1][2:-2].split(' ')]

####### Validation data ##############
with open('mfcc_2.txt') as f:
	content = f.readlines()

x_validation = []
for count, element in enumerate(content):
	if element[-2] is "[":
		continue
	else:
		x_validation.append([float(x) for x in element.split(" ")[2:-1]])

x_validation = np.vstack(x_validation)

with open('vad_2.txt') as f: 
	content = f.readlines()
content = [x.strip() for x in content]

y_validation = []
for count, element in enumerate(content):
	y_validation = y_validation + [int(x) for x in element.split("  ")[1][2:-2].split(' ')]

####### Testing data ##############
with open('mfcc_3.txt') as f:
	content = f.readlines()

x_test = []
for count, element in enumerate(content):
	if element[-2] is "[":
		continue
	else:
		x_test.append([float(x) for x in element.split(" ")[2:-1]])

x_test = np.vstack(x_test)

with open('vad_3.txt') as f: 
	content = f.readlines()
content = [x.strip() for x in content]

y_test = []
for count, element in enumerate(content):
	y_test = y_test + [int(x) for x in element.split("  ")[1][2:-2].split(' ')]
######################################################
print(len(x_train), 'train sequences')
print(len(x_validation), 'validation sequences')
print(len(x_test), 'test sequences')


print('Build model...')
model = Sequential()
model.add(LSTM(128, dropout=0.2, recurrent_dropout=0.2))
model.add(Dense(1, activation='sigmoid'))

# try using different optimizers and different optimizer configs
model.compile(loss='binary_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

print('Train...')
model.fit(x_train, y_train,
          batch_size=batch_size,
          epochs=15,
          validation_data=(x_validation, y_validation))
score, acc = model.evaluate(x_test, y_test,
                            batch_size=batch_size)
print('Test score:', score)
print('Test accuracy:', acc)