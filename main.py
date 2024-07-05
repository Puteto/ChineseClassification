# ~~~~~~~~~~~~~~~~~~~~
# Code by Anleo YUAN
# Please visit https://www.anleo.top
# Copyrights reserved by Chongqing University
# ~~~~~~~~~~~~~~~~~~~~
from tkinter import *
from tkinter import messagebox
import jieba
import jieba.posseg as pseg
import math
from array import array
import numpy as np
import scipy
from scipy import sparse
from libsvm.svmutil import *
from libsvm.svm import *
from libsvm.commonutil import *
from testFeatureWeight import *

# 导入文件
classCode = [ '财经','房产','股票','家居','教育','科技','社会','时尚','时政','体育','游戏','娱乐' ]
emotionCode = [ '褒义的', '贬义的']
classFeature = "classFeature.txt"
emotionFeature = "emotionFeature.txt"
classDfFeature = "classDfFeature.txt"
emotionDfFeature = "emotionDfFeature.txt"
classTrainData = "classTrainData.svm"
emotionTrainData = "emotionTrainData.svm"
classModel = "classTrain.model"
emotionModel = "emotionTrain.model"
classParam = "classParam.svm"
emotionParam = "emotionParam.svm"
trainDocumentCount = 60000

# 交互GUI设计
window = Tk()
window.title('中文文本分类和情感分析系统')
window.geometry('465x500')

lbl1 = Label(window, text="中文文本分类与情感分析",font=('黑体', 20))
lbl1.grid(row=0, column=0, columnspan=4, pady=10)

lbl2= Label(window, text="请输入文本:",font=('楷体', 8))
lbl2.grid(row=2, column=0, padx=20, pady=10)

txt = Text(window, width=60, height=13, font=('宋体', 10), relief=FLAT)
txt.grid(row=3, column=0, columnspan=4, padx=20)

# 将输入的文本分词处理
def textSeg(content):
    words = pseg.cut(content) # 分词
    finalContent = []
    # 停用词列表
    stopWords = [line.strip() for line in open('Chinesestopword.txt', 'r', encoding='utf-8').readlines()]

    for word in words:
        word = str(word.word)
        # 如果该单词非空格、换行符、不在听用词表中就将其添加进入最终分词列表中
        if len(word) > 1 and word != '\n' and word != '\u3000' and word not in stopWords:
            finalContent.append(word)

    # 组合成最终需要的字符串
    finalStr = " ".join(finalContent)
    finalFeature = finalStr.split(' ')
    return finalFeature

# 读取缩放范围
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

# 将输入文本特征转为TF-IDF值，并缩放存为libsvm格式
def featureToData(testFeature, featureName, dfFeatureName, paramName):
    feature = readFeature(featureName)
    dfFeatureDic = readDfFeature(dfFeatureName)
    xParam = readParam(paramName)
    prob_x = array('d')
    row_ptr = array('l', [0])
    col_idx = array('l')
    nz = 0
    for i in range(len(feature)):
        if feature[i] in testFeature:
            curFeature = feature[i]
            featureCount = testFeature.count(feature[i])
            tf = float(featureCount)/(len(testFeature))
            idfFeature = math.log(float(trainDocumentCount+1)/(int(dfFeatureDic[curFeature])+2))
            featureValue = tf * idfFeature
            featureValue = float(featureValue)/float(xParam[i])
            col_idx.append(int(i))
            prob_x.append(featureValue)
            nz += 1
    if nz == 0:
        return nz
    row_ptr.append(row_ptr[-1]+nz)
    prob_x = np.frombuffer(prob_x, dtype='d')
    col_idx = np.frombuffer(col_idx, dtype='l')
    row_ptr = np.frombuffer(row_ptr, dtype='l')
    prob_x = sparse.csr_matrix((prob_x, col_idx, row_ptr))
    return prob_x

# 预测函数
def testData(xData, modelName):
    model = svm_load_model(modelName)
    yt = array('d')
    yt = np.frombuffer(yt, dtype='d')
    p_lable, p_acc, p_val = svm_predict(yt, xData, model)
    return p_lable, p_acc, p_val

def classed():
    content = txt.get('1.0', 'end')
    entryFeature = textSeg(content)
    x = featureToData(entryFeature, classFeature, classDfFeature, classParam)
    if isinstance(x, int):
        messagebox.showerror("文本分类", '很抱歉：\n当前模型无法预测')
    else:
        p_lable, p_acc, p_val = testData(x, classModel)
        print(p_lable)
        result = classCode[int(p_lable[0])]
        messagebox.showinfo("文本分类", '预测结果：\n ' + str(result) + " 类文本")#占位
    content = ""

def emotion():
    content = txt.get('1.0', 'end')
    entryFeature = textSeg(content)
    x = featureToData(entryFeature, emotionFeature, emotionDfFeature, emotionParam)
    if isinstance(x, int):
        messagebox.showerror("情感分析", '很抱歉：\n当前模型无法预测')
    else:
        p_lable, p_acc, p_val = testData(x, emotionModel)
        print(p_lable)
        result = emotionCode[int(p_lable[0])]
        messagebox.showinfo("情感分析", '预测结果：\n ' + str(result))  # 占位
    content = ""

def delete():
    txt.delete('1.0', 'end')


btnclass = Button(window, text="文本分类", command=classed, font=('思源黑体 CN Medium', 12))
btnclass.grid(row=1,column=1,padx=10, ipadx=5)

btnemotion = Button(window, text="情感分析", command=emotion, font=('思源黑体 CN Medium', 12))
btnemotion.grid(row=1, column=2, padx=10, ipadx=5)

btndelete = Button(window, text="清空", command=delete)
btndelete.grid(row=4, column=3, padx=20, pady=10, ipadx=10)

lbl3= Label(window, text="2023 © CQU",font=('思源宋体 CN Medium', 8))
lbl3.grid(row=5, column=0, padx=20, pady=10)

window.mainloop()