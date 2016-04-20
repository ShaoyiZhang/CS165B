from math import *

class LDA:
    def __init__(self,filename):
        self.txtToMatrix(filename)
    def txtToMatrix(self,filename):
        infile = open(filename,'r')
        buffer = infile.read()
        buffer = buffer.split('\n')
        
        self.metadata = buffer[0]
        # index 0: the # of classes in the test set
        # index 1-n: the # of data point in each class
        
        del buffer[0]
        self.matrix = map(lambda row: row.split(),buffer)

        # matrix is a n*p dimensional matrix
        # n = # of data points
        # p = number of attributes

        

        
        
    #def centroid():
example = LDA("/Users/Shawn/Desktop/cs165b/HW2-6/testing.txt")

