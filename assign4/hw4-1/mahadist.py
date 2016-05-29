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
    test = open(testdata,"rt")
    testMeta = map(int,test.readline().split())
    test = test.read().split('\n')
    test = map(lambda row: row.split(), test)

    for i in range(testMeta[0]):
        test[i] = map(lambda attr: float(attr), test[i])  
    testNonMatrix = test
    test = np.asmatrix(test)
    # since we already used readline function once
    # the file pointer is on the second line, which is desired

    # compute centroid of training points
    centroid = [0.0] * trainMeta[1]
    for ithRow in range(trainMeta[0]):
        for jthAttribute in range(trainMeta[1]):
            centroid[jthAttribute] = centroid[jthAttribute] + train[ithRow][jthAttribute]
    for i in range(trainMeta[1]):
        centroid[i] = centroid[i] / trainMeta[0]
    
    # minus the X(train) with centroidTest, we will get zero-centered x
    trainT = np.transpose(np.asmatrix(train))
    meanMatrix = np.transpose(np.asmatrix([centroid]*trainMeta[0]))
    trainZ = trainT - meanMatrix
    
    scatter = trainZ.dot(np.transpose(trainZ)) 
    
    cov = scatter / trainMeta[0]
    centroid = np.asmatrix(centroid)

    mahadistance = []
    distVec = []
    for ithRow in range(testMeta[0]):
        distVec.append(math.sqrt(np.transpose(np.transpose(test[ithRow]-centroid)).dot(inv(cov)).dot(np.transpose(test[ithRow]-centroid))))
    distVec = map((lambda x: "%.2f" %  x),distVec)
    centroid = np.asarray(centroid)[0]
    #print cov
    centroid = map((lambda x: "%.2f" %  x),centroid)

    cov = np.asarray(cov)
    #print cov
    result = "Centroid:\n"
    result = result + " ".join(centroid) + "\n" + "Covariance Matrix: \n"
    for i in range(trainMeta[1]):
        cov[i] = np.asarray(cov[i])
        for j in range(trainMeta[1]):
            result += "%.2f " % cov[i][j]
        result += "\n"
    result += "Distances: \n"
    for ithTest in range(testMeta[0]):
        result += str(ithTest+1)
        result += ". "
        for jthAttr in range(testMeta[1]):
            result += "%.1f" % testNonMatrix[ithTest][jthAttr]
            result += " "
        result += "-- "
        result += str(distVec[ithTest])
        result += "\n"
    print result[0:-1]

if (len(sys.argv) != 3):
    print("Error: Invalid Filename, Expectin 2 .txt file")
else:
    mahadist(sys.argv[1],sys.argv[2])