# kernel perceptron
import numpy as np
import sys
import math
def parseX(data):
    x = data.read().split("\n")
    x = map((lambda row: row.split()),x)
    x = [map(float,ele) for ele in x]
    x = [map(row.reverse(),row) for row in x]
    x = [map(row.append(1),row) for row in x]
    return x
    
def kernelFunc(pointA,pointB,sigma):
    norm = 0.0
    for ithAttr in range(len(pointA)):
        norm = norm + (pointA[ithAttr] - pointB[ithAttr]) ** 2
    kernel = math.exp(-norm/(2*sigma**2))
    return kernel

def kerpercep(sigma, pos_train_file, neg_train_file, pos_test_file, neg_test_file):
    # prepare labeled input
    pos_train = open(pos_train_file,"rt")
    neg_train = open(neg_train_file,"rt")
    pos_test = open(pos_test_file,"rt")
    neg_test = open(neg_test_file,"rt")
    sigma = float(sigma)
    meta = [None]*4

    meta[0] = map(int,pos_train.readline().split())
    meta[0].append(1)
    meta[1] = map(int,neg_train.readline().split())
    meta[1].append(-1)
    meta[2] = map(int,pos_test.readline().split())
    meta[2].append(1)
    meta[3] = map(int,neg_test.readline().split())
    meta[3].append(-1)

    x = []
    xpos = parseX(pos_train)
    xneg = parseX(neg_train)
    x = xpos + xneg
    xTest = parseX(pos_test) + parseX(neg_test)
    y = []
    for metaRow in meta:
        for ithData in range(metaRow[0]):   # num of obs in one of the four data set
            y.append(metaRow[2])

    # nobs = number of observations in Training data
    nobs = meta[0][0] + meta[1][0]

    alpha = [0] * nobs
    converged = False
    while (converged == False):
        converged = True
        for i in range(nobs):
            decision = 0.0
            for j in range(nobs):
                decision = decision + alpha[j] * y[j] * kernelFunc(x[i],x[j],sigma)
            decision = decision * y[i]
            if (decision <= 0):
                alpha[i] = alpha[i] + 1
                converged = False
    
    P,N,FP,FN = 0,0,0,0

    for ithTest in range(len(xTest)):
        label = 0
        for jthTrain in range(nobs):

            label += alpha[jthTrain] * y[jthTrain] * kernelFunc(xTest[ithTest],x[jthTrain],sigma)
        if (label > 0):
            P += 1
            if not ((ithTest > nobs) and (ithTest < nobs + meta[2][0])):
                FP += 1
        else:
            N += 1
            if (ithTest > nobs) and (ithTest < nobs + meta[2][0]):
                FN += 1

    alpha = map((lambda a: str(a)),alpha)
    result = ""
    result += "Alphas: " + " ".join(alpha) + "\n"
    result += "False positives: " + str(FP) + "\n"
    result += "False negatives: " + str(FN) + "\n"
    result += "Error rate: " +  "%2.f" % (float(FP+FN)/(P*N)*100) + "%"

    print result[0:-1]

if (len(sys.argv) != 6):
    print("Error: Invalid Filename, Expectin 2 .txt file")
else:
    kerpercep(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])