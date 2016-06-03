import numpy as np
import sys

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
        self.numOfSample = int(numOfSample)
        self.sizeOfSample = int(sizeOfSample)
        # preparation finished
        self.bagging(self.numOfSample, self.sizeOfSample)

    def bagging(self,numOfSample, sizeOfSample):
        classifers = []
        result = []
        self.bootstrapSamples = [] # save for printing result

        for ithBootstrap in range(numOfSample):
            indices = np.random.randint(low = 0, high = (self.meta[0][1] + self.meta[0][2]) , size=sizeOfSample)
            train = [self.train[i] for i in indices]
            self.bootstrapSamples.append(train)
            train_pos = []
            train_neg = []
            ithClassifier = None

            for point in train:
                # parse bootstrapped data into positive and negative
                # in order to build linear classifier
                if point[self.dimension] == 1:
                    train_pos.append(point)
                else:
                    train_neg.append(point)
            if train_pos == []:
                # if all bootstrapped sample are positve
                # we classify all test data positive
                ithClassifier = "ALL POSITIVE"
            elif train_neg == []:
                ithClassifier = "ALL NEGATIVE"
            else:
                # build binary classifier
                ithClassifier = self.buildClassifier(train_pos,train_neg)
            classifers.append(ithClassifier)

            resultOneSample = self.applyToTest(self.test,ithClassifier)
            result.append(resultOneSample)
        # call majority vote and print output
        self.result = self.majorityVote(result)
        self.evaluation()

    def majorityVote(self,predictMatrix):
        result = []
        P,N,FP,FN = 0,0,0,0

        for ithTest in range(self.meta[1][1] + self.meta[1][2]):
            pos,neg = 0,0

            for jthBootstrap in range(len(predictMatrix)):
                # majority vote over different samples
                if (predictMatrix[jthBootstrap][ithTest] == 1):
                    pos+=1
                else:
                    neg+=1
            if pos >= neg:
                result.append(1)
                P += 1
                self.test[ithTest].append("True")
                if (self.test[ithTest][self.dimension] == -1):
                    FP += 1
                    self.test[ithTest].append("(false positive)")
                else:
                    self.test[ithTest].append("(correct)")
            else:
                result.append(-1)
                N += 1
                self.test[ithTest].append("False")
                if (self.test[ithTest][self.dimension] == 1):
                    FN += 1
                    self.test[ithTest].append("(false negative)")
                else:
                    self.test[ithTest].append("(correct)")
        # the statistics will be print regardless of "-v" option
        self.statistics = [P,N,FP,FN]
        return result

    def addLabel(self,dataSet,metaPos):
        for ithPoint in range(len(dataSet)):
            if (ithPoint < metaPos):
                dataSet[ithPoint].append(1)
            else:
                dataSet[ithPoint].append(-1)
        return dataSet

    def convertLabel(self,label):
        if label == 1:
            return "True"
        else:
            return "False"

    def buildClassifier(self,positives,negatives):
        pos_centroid = self.centroid(positives)
        neg_centroid = self.centroid(negatives)
        midPoint = self.midPoint(pos_centroid,neg_centroid)
        normalVec = self.normalVec(pos_centroid,neg_centroid)
        # normalVec dot (newPoint - midPoint) < 0 -> Positive
        
        func = normalVec

        scalar = 0.0
        for ithAttr in range(self.dimension):
            scalar -= (midPoint[ithAttr]*normalVec[ithAttr])
        func.append(scalar)

        return func

    def centroid(self,data):
        centroid = [0.0]*self.dimension
        for dataPoint in data:
            for ithAttr in range(self.dimension):
                centroid[ithAttr] += dataPoint[ithAttr]
        centroid = map((lambda x: x/len(data)),centroid)
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

    def applyToTest(self,testData,classifer):
        # apply classifer to test data
        predict = -1
        predictResult = []
        if isinstance(classifer,list): 
            for ithTest in testData:
                #actual = ithTest[self.dimension]
                predict = sign(applyFunc(classifer,ithTest))
                predictResult.append(predict)
            return predictResult
        elif isinstance(classifer,str):
            if classifer == "ALL POSITIVE":
                return [1]*len(testData)
            else:
                return [0]*len(testData)
        else:
            print("Error! Wrong classifier!")
            
    def evaluation(self):
        # print out result
        output = ""
        output += "Positive examples: " + str(self.statistics[0]) + "\n"
        output += "Negative examples: " + str(self.statistics[1]) + "\n"
        output += "False positives: " + str(self.statistics[2]) + "\n"
        output += "False negatives: " + str(self.statistics[3]) + "\n"
        output += "Error rate: " + "%2.2f" % (float(self.statistics[2]+self.statistics[3])/(self.statistics[0]+self.statistics[1])*100) + "%"


        if (sys.argv[1] == "-v"):
            for ithBootstrap in range(self.numOfSample):
                output += "\nBootstrap sample set " + str(ithBootstrap+1) + ":\n"
                for jthData in range(self.sizeOfSample):
                    output += " ".join(map((lambda x:  "%.2f" % x), self.bootstrapSamples[ithBootstrap][jthData][0:-1])) + " "
                    output += self.convertLabel(self.bootstrapSamples[ithBootstrap][jthData][-1]) + "\n"

            output += "\nClassification: "
            for ithTest in self.test:
                output += "\n" + " ".join(map((lambda x:  "%.2f" % x), ithTest[0:-3])) + " "
                output += ithTest[self.dimension+1] + " "
                output += ithTest[self.dimension+2]

        print output

# Helper method
# essentially dot product
def applyFunc(func,dataPoint):
    sum = 0.0
    # last index of func is a constant
    # others are coefficients
    for indexOfCoeff in range(len(func)-1):
        sum += func[indexOfCoeff] * dataPoint[indexOfCoeff]
    sum += func[-1]
    return sum

# Helper method
def sign(predict):
    if (predict >= 0.0): # negative class
        return -1
    else:
        return 1
        
# Helper method
# parse data into matrix form
def parseX(data):
    x = data.split("\n")
    x = map((lambda row: row.split()),x)
    x = [map(float,attribute) for attribute in x]
    return x

if (len(sys.argv) == 6):
    # verbose
    bagging(sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])
elif (len(sys.argv) == 5):
    bagging(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
            # numOfSample, sizeOfSample, trainData, testData
else:
    print("Error: Invalid Filename")