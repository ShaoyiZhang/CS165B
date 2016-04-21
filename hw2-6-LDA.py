from math import *
import numpy as np


def txtToMatrix(self,filename):
    infile = open(filename,'r')
    buffer = infile.read()
    buffer = buffer.split('\n')
    buffer = map(lambda row: row.split(),buffer)
    self.metadata = buffer[0]
    self.metadata = map(lambda x: x and x.isdigit() and int(x) or None,buffer[0])
        
    # index 0: the # of classes in the test set
    # index 1-n: the # of data point in each class
    
    self.numOfClass = self.metadata[0]
    del buffer[0]
    del buffer[-1]
    
    self.matrix = buffer
    for i in range(len(self.matrix)):
        self.matrix[i] = map(lambda x: float(x),self.matrix[i])
            
    index = 0
    startOfClass = 0
    endOfClass = 0
            
    for cl in range(self.numOfClass):
        for ele in range(self.metadata[cl+1]):
            self.matrix[index].append(cl+1)
            index+=1
                
                
    # matrix is a n*p dimensional matrix
    # n = # of data points
    # p = # of columns
    # p-1 = number of attributes
    # last column is a numeric label

    self.n = len(self.matrix)
    if (self.n>1):
        self.p = len(self.matrix[0])
    else:
        self.p = 0

    
    
class LDA:
    def __init__(self,filename):
        txtToMatrix(self,filename)
        self.centroid()
        self.buildDiscFuncs()
        print(self.matrix)

    def centroid(self):
        index = 0
        startOfClass = 0
        endOfClass = -1

        totalVector = [0] * (self.p - 1)

        meanMatrix = []

        for cl in range(self.numOfClass):
            for i in range(self.metadata[cl+1]):
                for p in range(self.p-1):
                    totalVector[p] += self.matrix[index][p]
                index+=1
            meanMatrix.append(map(lambda col: col/self.metadata[cl+1] ,totalVector))
            totalVector = [0] * (self.p - 1)
        
            #        self.matrix = np.matrix(self.matrix)
        self.meanMatrix = meanMatrix
            

    def midPoint(self,pointA,pointB):
        midPoint = []
        for coeff in range(len(pointA)):
            midPoint.append((pointA[coeff] + pointB[coeff])/2)
        return midPoint

    def buildDiscFuncs(self):
        funcs = []
        mids = []
        funcs.append(np.cross(self.meanMatrix[0],self.meanMatrix[1]).tolist())
        funcs.append(np.cross(self.meanMatrix[0],self.meanMatrix[2]).tolist())
        funcs.append(np.cross(self.meanMatrix[1],self.meanMatrix[2]).tolist())
        mids.append(self.midPoint(self.meanMatrix[0],self.meanMatrix[1]))
        mids.append(self.midPoint(self.meanMatrix[0],self.meanMatrix[2]))
        mids.append(self.midPoint(self.meanMatrix[1],self.meanMatrix[2]))
        
        for cl in range(self.metadata[0]):
            constant = 0
            for coeff in range(self.p-1):
                constant -= funcs[cl][coeff] * mids[cl][coeff]
                funcs[cl].append(constant)
        self.funcs = funcs

class triclassify:            
    def __init__(self,trainFile,testFile):
        self.classifer = LDA(trainFile).funcs
        self.applyToTest(testFile)
        
    def classify(self,dataPoint):
        if (applyFunc(self.classifer[0]) > 0):
            # might be B or C
            if (applyFunc(self.classfier[2]) > 0):
                return 3    # indicating C
            else:
                return 2    # indicating B        
        else:
            # might be A or C
            if (applyFunc(self.classifer[1] > 0)):
                return 3    # indicating C
            else:
                return 1    # indicating A
    def applyToTest(self,testFile):
        txtToMatrix(self,testFile)
        print(self.matrix)
        
    #def applyFunc(self,listOfCoeffs,dataPoint):

example = triclassify("training.txt","testing.txt")
#example = LDA("testing.txt")
#example.centroid()

