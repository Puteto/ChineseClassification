# ~~~~~~~~~~~~~~~~~~~~
# Code by Anleo YUAN
# Please visit https://www.anleo.top
# Copyrights reserved by Chongqing University
# ~~~~~~~~~~~~~~~~~~~~
import numpy as np
import scipy
from scipy import sparse
from array import array
from libsvm.svmutil import *
from libsvm.svm import *
from libsvm.commonutil import *

testName = "test.svm"
classModel = "classTrain.model"
emotionModel = "train.model"
classParam = "classParam.svm"
emotionParam = "emotionParam.svm"

def readParam(paramName):
    paramFile = open(paramName, 'r', encoding='utf-8')
    paramContent = paramFile.read().split("\n")
    paramFile.close()
    xParam = []
    for eachParam in paramContent:
        eachParam = eachParam.split(" ")
        if len(eachParam) == 3:
            xParam.append(eachParam[2])
    return xParam
def dataScale(dataName, paramName):
    xParam = readParam(paramName)
    prob_y = array('d')
    prob_x = array('d')
    row_ptr = array('l', [0])
    col_idx = array('l')
    indx_start = 1
    for i, line in enumerate(open(dataName)):
        line = line.split(None, 1)
        # In case an instance with all zero features
        if len(line) == 1: line += ['']
        label, features = line
        prob_y.append(float(label))
        nz = 0
        for e in features.split():
            ind, val = e.split(":")
            if ind == '0':
                indx_start = 0
            val = float(val)
            if val != 0:
                col_idx.append(int(ind) - indx_start)
                val = float(val)/float(xParam[int(ind)-indx_start])
                prob_x.append(val)
                nz += 1
        row_ptr.append(row_ptr[-1] + nz)
    prob_y = np.frombuffer(prob_y, dtype='d')
    prob_x = np.frombuffer(prob_x, dtype='d')
    col_idx = np.frombuffer(col_idx, dtype='l')
    row_ptr = np.frombuffer(row_ptr, dtype='l')
    prob_x = sparse.csr_matrix((prob_x, col_idx, row_ptr))
    return (prob_y, prob_x)

yt, xt = dataScale(testName, emotionParam)
m = svm_load_model(emotionModel)
p_lable, p_acc, p_val = svm_predict(yt, xt, m)
print(p_acc)
