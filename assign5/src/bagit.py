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

    def __init__(self,numOfSample, sizeOfSample, trainFile,testFile):
        train = open(trainFile,"rt")
        test = open(testFile,"rt")
        self.meta = [[],[]]
        self.meta[0] = map(int,train.readline().split())
        self.meta[1] = map(int,test.readline().split())
        self.dimension = self.meta[0][0]
        self.train = parseX(train.read())
        self.test = parseX(test.read())
        self.classifers = []
        self.train = self.addLabel(self.train,self.meta[0][1])
        self.test = self.addLabel(self.test,self.meta[1][1])
        #self.train_pos = []
        #for i in range(self.meta[0][1]):
        #   self.train_pos.append(train[i])
        #for j in range(self.meta[0][2]):
        #print "20:", len(self.train[self.meta[0][1]:])

        #self.buildClassifier(self.train[0:(self.meta[0][1])], self.train[self.meta[0][1]:])
        #self.applyToTest(self.test, self.classifers[0], self.meta[1][0],self.meta[1][1])
        # preparation finished

        self.bagging(int(numOfSample), int(sizeOfSample))

    def bagging(self,numOfSample, sizeOfSample):
        for ithBootstrap in range(numOfSample):
            indices = np.random.randint(low = 0, high = sizeOfSample, size=sizeOfSample)
            train = [self.train[i] for i in indices]
            train_pos = []
            train_neg = []
            for point in train:
                if point[self.dimension] == 1:
                    train_pos.append(point)
                else:
                    train_neg.append(point)
            self.buildClassifier(train_pos,train_neg)

    def addLabel(self,dataSet,metaPos):
        for ithPoint in range(len(dataSet)):
            if (ithPoint < metaPos):
                dataSet[ithPoint].append(1)
            else:
                dataSet[ithPoint].append(0)
        return dataSet

    def buildClassifier(self,positives,negatives):
        #print "gg"
        pos_centroid = self.centroid(positives)
        #print pos_centroid
        neg_centroid = self.centroid(negatives)
        #print neg_centroid
        midPoint = self.midPoint(pos_centroid,neg_centroid)
        normalVec = self.normalVec(pos_centroid,neg_centroid)
        #print normalVec
        #normalVec dot (newPoint - midPoint) < 0 -> Positive
        
        func = normalVec

        scalar = 0.0
        for ithAttr in range(self.dimension):
            scalar -= (midPoint[ithAttr]*normalVec[ithAttr])
        func.append(scalar)

        self.classifers.append(func)

    def centroid(self,data):
        centroid = [0.0]*self.dimension
        for dataPoint in data:
            for ithAttr in range(self.dimension):
                centroid[ithAttr] += dataPoint[ithAttr]
        centroid = map((lambda x: x/len(data)),centroid)
        #print len(data)
        return centroid
    
    def midPoint(self,pointA,pointB):
        midPoint = []
        for ithAttr in range(self.dimension):
            midPoint.append((pointA[ithAttr] + pointB[ithAttr]) / 2)
        return midPoint

    def normalVec(self,pointA,pointB):
        normalVec = [0.0]*self.dimension
        for ithAttr in range(self.dimension):
            normalVec[ithAttr] = pointB[ithAttr] - pointA[ithAttr]
        return normalVec

    def applyToTest(self,testData,classifer,testPos,testNeg):
        P,N,FP,FN = 0,0,0,0
        label = 0
        for ithTest in range(len(testData)):
            label = applyFunc(classifer,testData[ithTest])
            '''
            if (label < 0): ################ condition@!!@!!!!
                P += 1
                if not ((ithTest > nobs) and (ithTest < nobs + meta[2][0])):
                    FP += 1
            else:
                N += 1
                if (ithTest > nobs) and (ithTest < nobs + meta[2][0]):
                    FN += 1
            '''
            print label,ithTest

# Helper method
def applyFunc(func,dataPoint):
    sum = 0.0
    # last index of func is a constant
    # others are coefficients
    for indexOfCoeff in range(len(func)-1):
        sum += func[indexOfCoeff] * dataPoint[indexOfCoeff]
    sum += func[-1]
    return sum 



if (len(sys.argv) == 6):
    # verbose
    pass
elif (len(sys.argv) == 5):
    bagging(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
    # numOfSample, sizeOfSample, trainData, testData
else:
    print("Error: Invalid Filename")
