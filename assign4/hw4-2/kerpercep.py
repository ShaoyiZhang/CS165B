# kernel perceptron
import numpy as np
import sys


    
    
def kerpercep(sigma, pos_train_file, neg_train_file, pos_test_file, neg_test_file):
    # prepare labeled input
    pos_train = open(pos_train_file,"rt")
    neg_train = open(neg_train_file,"rt")
    pos_test = open(pos_test_file,"rt")
    neg_test = open(neg_test_file,"rt")

    meta = []

    meta.append(list(map(int,pos_train.readline().split())).append(1))
    meta.append(list(map(int,neg_train.readline().split())).append(-1))
    meta.append(list(map(int,pos_test.readline().split())).append(1))
    meta.append(list(map(int,neg_test.readline().split())).append(-1))
    print meta
    x = np.concatenate( np.array(pos_train.read()), np.array(neg_train.read()) )
    print x
    y = []
    for metaRow in meta:
        for ithData in range(metaRow[0]):   # num of obs in one of the four data set
            y.append(metaRow[2])
    print y 
    # nobs = number of observations

if (False):
    alpha = [0] * nobs
    converged = False
    while (converged == False):
        converged = True
        for i in range(nobs):
            dicide = 0.0
            for j in range(nobs):
                decide = decide + alpha[j]*y[i]*(x[j].dot(x[i]))
            decide = decide * y[i]
            if (decide <= 0):
                alpha[i] += 1
                converged = False


if (len(sys.argv) != 6):
    print("Error: Invalid Filename, Expectin 2 .txt file")
else:
    kerpercep(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])