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
        print(buffer)
        self.matrix = buffer
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
                print("start: ",startOfClass," end: ",endOfClass)
            for ele in range(startOfClass,endOfClass):
                self.matrix[index].append(i+1)
                index+=1
                print("index: ",index," class: ",i+1)
            startOfClass += endOfClass+1
        # matrix is a n*p dimensional matrix
        # n = # of data points
        # p-1 = number of attributes
        # last column is a numeric label
        
        #with open("Output.txt", "w") as text_file:
        #        text_file.write(''.join(for ele in self.matrix))
        #for ele in self.matrix:
            #print(ele,"\n")

        
        
    #def centroid():
example = LDA("/Users/Shawn/Desktop/cs165b/HW2-6/testing.txt")

