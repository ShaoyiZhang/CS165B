from math import *
import numpy as np
import sys

def txtToMatrix(self,filename):
    infile = open(filename,'r')
    buffer = infile.read()
    buffer = buffer.split('\n')
    buffer = map(lambda row: row.split(),buffer)
    self.metadata = buffer[0]
    self.metadata = map(lambda x: x and x.isdigit() and int(x) or None,buffer[0])
        
    # index 0: the # of classes in the test set
    # index 1-n: the # of data point in each class
    
    self.numOfClass = 3
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
        #print self.matrix

    def midPoint(self,pointA,pointB):
        midPoint = []
        for coeff in range(len(pointA)):
            midPoint.append((pointA[coeff] + pointB[coeff])/2)
        return midPoint

    def normalVec(self,centroid1,centroid2):
        normVec = []
        euclidianDist = 0
        for indexOfFeature in range(self.p-1):
            normVec.append(centroid2[indexOfFeature] - centroid1[indexOfFeature])
            euclidianDist += (centroid2[indexOfFeature] - centroid1[indexOfFeature])**2
        for scaler in normVec:
            scaler = scaler/(2*euclidianDist)
        return normVec
    
    def buildDiscFuncs(self):
        funcs = []
        mids = []
        normVecs = []
        
        mids.append(self.midPoint(self.meanMatrix[0],self.meanMatrix[1]))
        mids.append(self.midPoint(self.meanMatrix[0],self.meanMatrix[2]))
        mids.append(self.midPoint(self.meanMatrix[1],self.meanMatrix[2]))
        # A/B A/C B/C

        normVecs.append(self.normalVec(self.meanMatrix[0],self.meanMatrix[1]))
        normVecs.append(self.normalVec(self.meanMatrix[0],self.meanMatrix[2]))
        normVecs.append(self.normalVec(self.meanMatrix[1],self.meanMatrix[2]))
        # A/B A/C B/C

        funcs = normVecs

        sum = 0
        for cl in range(self.numOfClass):
            sum = 0
            for index in range(self.p - 1):
                sum -= (mids[cl][index]*normVecs[cl][index])
            funcs[cl].append(sum)
            sum = 0

        self.funcs = funcs
        #print(funcs)
class triclassify:            
    def __init__(self,trainFile,testFile):
        self.classifier = LDA(trainFile).funcs
        self.applyToTest(testFile)
        self.result()
        
    def classify(self,dataPoint):
        if (applyFunc(self,self.classifier[0],dataPoint) > 0):
            # might be B or C
            if (applyFunc(self,self.classifier[2],dataPoint) > 0):
                return 3    # indicating C
            else:
                return 2    # indicating B        
        else:
            # might be A or C
            if (applyFunc(self,self.classifier[1],dataPoint) > 0):
                return 3    # indicating C
            else:
                return 1    # indicating A
            
    def applyToTest(self,testFile):
        txtToMatrix(self,testFile)
        #print(self.matrix)
        predict = -1
        PA,PB,PC,NA,NB,NC = 0.0,0.0,0.0,0.0,0.0,0.0
        TPA,TPB,TPC = 0.0,0.0,0.0
        FPA,FPB,FPC = 0.0,0.0,0.0
        TNA,TNB,TNC = 0.0,0.0,0.0
        FNA,FNB,FNC = 0.0,0.0,0.0
        
        
        for index in range(self.n):
            trueClass = self.matrix[index][self.p-1]
            predict = self.classify(self.matrix[index])
            if (predict == 1):
                PA += 1
                NB+=1
                NC+=1
                if (trueClass == 1):
                    TPA+=1
                    TNB+=1
                    TNC+=1 
                elif (trueClass == 2):
                    FPA+=1
                    FNB+=1
                    TNC+=1
                else:
                    FPA+=1
                    TNB+=1
                    FNC+=1
            elif (predict == 2):
                PB += 1
                NA+=1
                NC+=1
                if (trueClass == 1):
                    FNA+=1
                    FPB+=1
                    TNC+=1
                elif (trueClass == 2):
                    TNA+=1
                    TPB+=1
                    TNC+=1
                else:
                    TNA+=1
                    FPB+=1
                    FNC+=1
            elif (predict == 3):
                PC += 1
                NA+=1
                NB+=1
                if (trueClass == 1):
                    FNA+=1
                    TNB+=1
                    FPC+=1
                elif (trueClass == 2):
                    TNA+=1
                    FNB+=1
                    FPC+=1
                else:
                    TNA+=1
                    TNB+=1
                    TPC+=1
        
        TPRA = TPA/(TPA+FNA)
        TPRB = TPB/(TPB+FNB)
        TPRC = TPC/(TPC+FNC)
        self.TPR = (TPRA+TPRB+TPRC)/3

        FPRA = FPA/(FPA+TNA)
        FPRB = FPB/(FPB+TNB)
        FPRC = FPC/(FPC+TNC)
        self.FPR = (FPRA+FPRB+FPRC)/3
        P = PA+PB+PC
        N = NA+NB+NC
        self.ERROR = (FPA+FPB+FPC+FNA+FNB+FNC)/(P+N)
        self.ACCUR = 1 - self.ERROR
        self.PRECI = (TPA/PA + TPB/PB + TPC/PC)/3
        
    def result(self):
        print "True positive Rate = ","%.2f" % self.TPR
        print "False positive Rate = ","%.2f" % self.FPR
        print "Error rate = ","%.2f" % self.ERROR
        print "Accuracy = ","%.2f" % self.ACCUR
        print "Precision = ","%.2f" % self.PRECI

# Helper
def applyFunc(self,func,dataPoint):
    sum = 0
    # last index of func is a constant
    # others are coefficients
    for indexOfCoeff in range(len(func)-1):
        sum += func[indexOfCoeff] * dataPoint[indexOfCoeff]
    sum += func[-1]
    return sum 

if (len(sys.argv) != 3):
    print("Error: Invalid Filename, Expectin 2 .txt file")
else:
    triclassify(sys.argv[1],sys.argv[2])

#example = triclassify("training.txt","testing.txt")
#example = LDA("testing.txt")
#example.centroid()

