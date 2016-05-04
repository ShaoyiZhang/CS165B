import numpy as np
from numpy.linalg import inv
import sys

def linreg(traindata,testdata):
	#dataTable = read.table(infile)
	#dataTable = np.loadtxt(infile,skiprows=1)
	train = open(traindata,"rt")
	firstline = train.readline()
	metadata = firstline.split()
	metadata[0] = int(metadata[0])
	metadata[1] = int(metadata[1])
	dataTable = []
	y = []
	x = []
	# create dataTable with output y
	for dataPoint in range(metadata[0]):
		line = map(float,list(train.readline().split())) 
		dataTable.append(line)
		# construct y vector
		temp = []
		temp.append(line[-1])
		y.append(temp)
		# construct x matrix
		x.append(list(reversed([line[i] for i in range(metadata[1]-1)])))
		x[dataPoint].append(1)

	x = np.asmatrix(x)
	y = np.asmatrix(y)

	# W = (X^TX)^(-1)X^Ty
	w = (inv(np.transpose(x).dot(x)).dot(np.transpose(x))).dot(y)

	# read in test data
	test = open(testdata,"rt")
	firstline = test.readline()
	test_metadata = firstline.split()
	test_metadata[0] = int(test_metadata[0])
	test_metadata[1] = int(test_metadata[1])

	test_X = []
	for dataPoint in range(test_metadata[0]):
		row = map(float,list(test.readline().split()))

		temp = list(reversed([row[i] for i in range(test_metadata[1])]))
		temp.append(1)
		test_X.append(temp)

	test_X = np.asmatrix(test_X)
	test_estimate = test_X.dot(w)
	#print test_X,"\n"

	#print w
	w_out = np.squeeze(np.asarray(np.transpose(w)))
	#print w_out
	w_string = "w: "
	for i in range(metadata[1]):
		w_string+=str(round(w_out[i],2))
		w_string+=" "
	print w_string

	out_string = ""

	for i in range(test_metadata[0]):
		for j in range(test_metadata[1]):
			out_string += str(round(np.asarray(np.asarray(test_X[i])[0])[j],1))
			out_string += " "
		out_string += "-- "
		out_string += str(round(np.squeeze(np.asarray(test_estimate[i])[0]),1))
		out_string += "\n"
	print out_string

if (len(sys.argv) != 3):
    print("Error: Invalid Filename, Expectin 2 .txt file")
else:
    linreg(sys.argv[1],sys.argv[2])