from math import *

class LDA:
    def __init__(self,filename):
        self.txtToMatrix(filename)
    def txtToMatrix(self,filename):
        infile = open(filename,'r')
        buffer = infile.read()
        buffer = buffer.split('\n')
        buffer = map(lambda row: row.split(),buffer)
        self.metadata = buffer[0]
        print(len(buffer[0]))
        self.metadata = map(lambda x: x and x.isdigit() and int(x) or None,buffer[0])
        
        
        # index 0: the # of classes in the test set
        # index 1-n: the # of data point in each class
        self.numOfClass = self.metadata[0]
        del buffer[0]
        if buffer[-1] == '':
            del buffer[-1]
        self.matrix = buffer
        for i in range(len(self.matrix)):
            #self.matrix[i] = map(lambda x: x and x.isdigit() and int(x) or None,buffer[0])
            self.matrix[i] = map(lambda x: float(x),self.matrix[i])
#            print(self.matrix[i])
#        print(buffer)

        index = 0
        #print(isinstance(self.metadata[1],str))
        startOfClass = 0
        endOfClass = -1
        '''
        for indexOfClass in range(1,int(self.metadata[0])+1):
            for ele in range(nextClass,(int(self.metadata[indexOfClass])+1)):
                self.matrix[index].append(str(indexOfClass))
                print self.matrix[index]
                index+=1
            nextClass+= int(metadata[indexOfClass])
        print(self.matrix)
        '''
        index = 0
        for i in range(self.numOfClass):
            if (i <= self.numOfClass):
                endOfClass += (self.metadata[i+1]+1)
  #              print("start: ",startOfClass," end: ",endOfClass)
            for ele in range(startOfClass,endOfClass):
                self.matrix[index].append(i+1)
                index+=1
 #               print("index: ",index," class: ",i+1)
            startOfClass = endOfClass+1
 #           print(startOfClass,endOfClass)
        # matrix is a n*p dimensional matrix
        # n = # of data points
        # p-1 = number of attributes
        # last column is a numeric label
        
        x1 = 0
        x2 = 0
        x3 = 0
        for row in range(len(self.matrix)-1):
            if self.matrix[row][3] == 1:
                x1+=1
            if self.matrix[row][3] == 2:
                x2+=1
            if self.matrix[row][3] == 3:
                x3+=1
        print(x1,x2,x3)
        
        print(self.matrix)


    #def centroid():
example = LDA("/Users/Shawn/Desktop/cs165b/HW2-6/testing.txt")

