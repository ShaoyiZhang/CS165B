# k nearest neighbour

import numpy as np
import sys
import math

def parseX(data):
    x = data.read().split("\n")
    x = map((lambda row: row.split()),x)
    x = [map(float,ele) for ele in x]
    #x = [map(row.reverse(),row) for row in x]
    #x = [map(row.append(1),row) for row in x]
    #print x
    return x
def distance(pointA,pointB):
    norm = 0.0
    for ithAttr in range(len(pointA)):
        norm = norm + (pointA[ithAttr] - pointB[ithAttr]) ** 2
    norm = math.sqrt(norm)
    return norm

def knn(k,traindata,testdata):
    train = open(traindata,"rt")
    test = open(testdata,"rt")
    meta = [None]*2
    meta[0] = map(int,train.readline().split())    
    meta[1] = map(int,test.readline().split())
    #print meta
    train = parseX(train)
    test = parseX(test)
    # figure out number of classes
    classes = set()
    for i in range(meta[0][0]):
        classes.add(train[i][meta[0][1]])
    nclass = len(classes)

    predictClass = []
    for ithTest in range(meta[1][0]):
        distVec = []
        # calculate distance between test point and all points in the training data
        for jthTrain in range(meta[0][0]):
            distVec.append([ distance(test[ithTest],train[jthTrain]), int(train[jthTrain][meta[0][1]]) ])
        #print "Unsorted: ", distVec
        distVec = sorted(distVec, key = lambda x: x[0])
        #print "Sorted: ", distVec

        occurrence = [0]*nclass
        for knn in range(int(k)):
            # label 1 ~ nclass
            # index 0 ~ nclass-1
            occurrence[distVec[knn][1] - 1] += 1
        #print "occurrence: ", occurrence

        # find the most frequent class in occurrence array
        maxFreq = occurrence[0]
        maxFreqClass = 0
        for ithClass in range(len(occurrence)):
            if (occurrence[ithClass]>maxFreq):
                maxFreq = occurrence[ithClass]
                maxFreqClass = ithClass
        #print maxFreqClass
        maxFreqClass += 1
        #print maxFreqClass
        #print
        #print
        predictClass.append(maxFreqClass)

    # then we need to print the result
    result = ""
    for ithTest in range(meta[1][0]):
        result += str(ithTest+1)
        result += ". "
        for jthAttr in range(meta[1][1]):
            result += "%.1f" % test[ithTest][jthAttr]
            result += " "
        result += "-- "
        result += str(predictClass[ithTest])
        result += "\n"

    print result[0:-1]


if (len(sys.argv) != 4):
    print("Error: Invalid Filename, Expectin 2 .txt file")
else:
    knn(sys.argv[1],sys.argv[2],sys.argv[3])


