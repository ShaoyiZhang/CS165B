import numpy as np
from numpy.linalg import inv
import sys
import math

def mahadist(traindata,testdata):

    train = open(traindata,"rt")
    trainMeta = map(int,train.readline().split())
    train = train.read().split('\n')

    train = map(lambda row: row.split(), train)
    for i in range(trainMeta[0]):
        train[i] = map(lambda attr: float(attr), train[i])

    # why last number is str????
  
    
    
    #train[trainMeta[0]-1][trainMeta[1]-1] = float(train[trainMeta[0]-1][trainMeta[1]-1])
    
    #for row in train:
    #    print type(row[0])
    #    print type(row[1])
    #.replace('\n',';')
    #print train

    test = open(testdata,"rt")
    testMeta = map(int,test.readline().split())
    test = test.read().split('\n')

 
    test = map(lambda row: row.split(), test)
    for i in range(testMeta[0]):
        test[i] = map(lambda attr: float(attr), test[i])  
    test = np.asmatrix(test)
    #print test
    # since we already used readline function once
    # the file pointer is on the second line, which is desired
    #train = np.asmatrix(train)
    #test = np.matrix(test)
    #print train[0][1]
    #
    
    # compute centroid of training points
    centroid = [0.0] * trainMeta[1]
    for ithRow in range(trainMeta[0]):
        for jthAttribute in range(trainMeta[1]):
            centroid[jthAttribute] = centroid[jthAttribute] + train[ithRow][jthAttribute]
    for i in range(trainMeta[1]):
        centroid[i] = centroid[i] / trainMeta[0]
    #print centroid
    
    
    # we also need the centroid of the test data
    #centroidTest = [0.0] * testMeta[1]
    #for ithRow in range(testMeta[0]):
    #    for jthAttribute in range(testMeta[1]):
    #        centroidTest[jthAttribute] = centroidTest[jthAttribute] + test[ithRow][jthAttribute]
    #for i in range(testMeta[1]):
    #    centroidTest[i] = centroidTest[i] / testMeta[0]
    
    # minus the X(train) with centroidTest, we will get zero-centered xrange
    trainT = np.transpose(np.asmatrix(train))
    print ""
    meanMatrix = np.transpose(np.asmatrix([centroid]*trainMeta[0]))
    trainZ = trainT - meanMatrix
    #for ithRow in range(trainMeta[0]):
    #    row = []
    #    for jthAttribute in range(trainMeta[1]):
    #        row.append(train[ithRow][jthAttribute]/centroid[jthAttribute])
    #    trainZ.append(row)
    print trainZ.shape
    # find the covariance matrix
    
    #trainZ = np.asmatrix(trainZ)
    
    scatter = trainZ.dot(np.transpose(trainZ)) 
    
    cov = scatter / trainMeta[0]
    centroid = np.asmatrix(centroid)
    #centroidMatrix = [centroid]*testMeta[0]
    mahadistance = []
    print cov 
    print testMeta[0]

    for ithRow in range(testMeta[0]):
        #print "test - centroid" 
        #print np.transpose(test[ithRow])
        #print np.transpose(test[i]-centroid)
        print math.sqrt(np.transpose(np.transpose(test[ithRow]-centroid)).dot(inv(cov)).dot(np.transpose(test[ithRow]-centroid)))
    #xMinusY = np.asmatrix(test) - np.asmatrix(test)
    #print xMinusY
    #print np.transpose(xMinusY).dot(inv(cov)).dot(xMinusY)
    #result = math.sqrt()
    #print mahadistance
#def construct

if (len(sys.argv) != 3):
    print("Error: Invalid Filename, Expectin 2 .txt file")
else:
    mahadist(sys.argv[1],sys.argv[2])
