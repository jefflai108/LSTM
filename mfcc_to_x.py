import numpy as np 

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

# with open('output_x_y.txt', 'w') as f:
# 	for t in (x_train, y_train):
# 		f.write(''.join(str(t)) + '\n')


