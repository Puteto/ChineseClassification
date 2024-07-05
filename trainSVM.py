# ~~~~~~~~~~~~~~~~~~~~
# Code by Anleo YUAN
# Please visit https://www.anleo.top
# Copyrights reserved by Chongqing University
# ~~~~~~~~~~~~~~~~~~~~
import numpy as np
import scipy
from libsvm.svmutil import *
from libsvm.svm import *
from libsvm.commonutil import *

trainName = "train.svm"
modelName = "train.model"

def trainData(trainName):
    y, x = svm_read_problem(trainName, return_scipy=True)
    param = csr_find_scale_param(x, lower=0, upper=1)
    x0 = csr_scale(x, param)
    model = svm_train(y, x0, '-s 0 -t 2 -c 10')
    svm_save_model(modelName, model)

if __name__ == '__main__':
    trainData(trainName)