from math import *
import numpy as np
class LDA:
    def __init__(self,filename):
        self.txtToMatrix(filename)
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
        endOfClass = -1
        
        for i in range(self.numOfClass):
            if (i <= self.numOfClass):
                endOfClass += (self.metadata[i+1])
            for ele in range(startOfClass,endOfClass):

                self.matrix[index].append(i+1)
                index+=1
            startOfClass = endOfClass+1

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


        print(meanMatrix)
        print(np.zeros((4,4)))
    '''
    def scatterWithinClass(self):
        S_W = np.zeros((4,4))
        for cl,mv in zip(range(1,4), mean_vectors):
            class_sc_mat = np.zeros((4,4))                  # scatter matrix for every class
            for row in X[y == cl]:
                row, mv = row.reshape(4,1), mv.reshape(4,1) # make column vectors
                class_sc_mat += (row-mv).dot((row-mv).T)
            S_W += class_sc_mat                             # sum class scatter matrices
        print('within-class Scatter Matrix:\n', S_W)
    '''        
#example = LDA("/Users/Shawn/Desktop/cs165b/HW2-6/testing.txt")
example = LDA("testing.txt")
example.centroid()
