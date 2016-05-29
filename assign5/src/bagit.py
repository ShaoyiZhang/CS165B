import numpy as np
#from numpy.linalg import inv
import sys
#import math

def parseX(data):
    x = data.split("\n")
    x = map((lambda row: row.split()),x)
    x = [map(float,attribute) for attribute in x]
    return x

class bagging:

	def __init__(self,numOfSample, sizeOfSample, trainData,testData):
		train = open(trainData,"rt")
		test = open(testData,"rt")
		self.meta = [[],[]]
		self.meta[0] = map(int,train.readline().split())
		self.meta[1] = map(int,test.readline().split())
		self.dimension = self.meta[0][0]
		self.train = parseX(train.read())
		self.test = parseX(test.read())
		#self.train_pos = []
		#for i in range(self.meta[0][1]):
		#	self.train_pos.append(train[i])
		#for j in range(self.meta[0][2]):
		#print "20:", len(self.train[self.meta[0][1]:])
		self.buildClassifier(self.train[0:(self.meta[0][1])], self.train[self.meta[0][1]:])
		# preparation finished

	def buildClassifier(self,positives,negatives):
		print "gg"
		pos_centroid = self.centroid(positives)
		print pos_centroid
		#neg_centroid = self.centroid(negatives)
		#midPoint = self.midPoint(pos_centroid,neg_centroid)
		#normalVec = self.normalVec(pos_centroid,neg_centroid)
		#normalVect dot (newPoint - midPoint) > 0 -> Positive

	def centroid(self,data):
		centroid = [0.0]*self.dimension
		for dataPoint in data:
			for ithAttr in range(self.dimension):
				centroid[ithAttr] += dataPoint[ithAttr]
		centroid = map((lambda x: x/len(data)),centroid)
		#print len(data)
		return centroid


if (len(sys.argv) == 6):
	# verbose
	pass
elif (len(sys.argv) == 5):
	bagging(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
	# numOfSample, sizeOfSample, trainData, testData
else:
    print("Error: Invalid Filename")
