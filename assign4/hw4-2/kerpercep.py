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
    #x = map((lambda row: row.reverse()), x)# for ele in x]
    return x
    
def kernelFunc(pointA,pointB,sigma):
    norm = 0.0
    #print type(sigma)

    #print pointA[0]
    #print pointB[0]
    for ithAttr in range(len(pointA)):
        norm = norm + (pointA[ithAttr] - pointB[ithAttr]) ** 2
    #norm = math.sqrt(norm)
    #print norm
    kernel = math.exp(-norm/(2*sigma**2))
    print kernel
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

    #print meta
    x = []
    #x.append(np.array(pos_train.read()))
    #x.append(np.array(neg_train.read()))
    #xpos = pos_train.read().split("\n")
    #xpos = map((lambda row: row.split()),xpos)
    #xpos = [map(float,x) for x in xpos]
    xpos = parseX(pos_train)
    xneg = parseX(neg_train)
    x = xpos + xneg
    #print x
    #x = np.asmatrix(x)
    #x = np.concatenate(([xpos],[xneg]),axis=0)
    #x = np.concatenate((np.array(pos_train.read()),np.array(neg_train.read())),axis=0)
    #np.concatenate( list(np.array(pos_train.read())).append(np.array(neg_train.read())), axis = 0 )
    #print x
    #print np.array(neg_train.read())
    y = []
    for metaRow in meta:
        for ithData in range(metaRow[0]):   # num of obs in one of the four data set
            y.append(metaRow[2])
    #print y 
    # nobs = number of observations
    nobs = meta[0][0] + meta[1][0]

    print "nobs: ", nobs

    alpha = [0] * nobs
    converged = False
    while (converged == False):
        converged = True
        for i in range(nobs):
            decision = 0.0
            for j in range(nobs):
                #decision = decision + alpha[j]*y[i]*(x[j].dot(np.transpose(x[i])))
                decision = decision + alpha[j] * y[j] * kernelFunc(x[i],x[j],sigma)
            decision = decision * y[i]
            #print decision
            if (decision <= 0):
                alpha[i] = alpha[i] + 1
                converged = False
            print alpha



if (len(sys.argv) != 6):
    print("Error: Invalid Filename, Expectin 2 .txt file")
else:
    kerpercep(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])