# ~~~~~~~~~~~~~~~~~~~~
# Code by Anleo YUAN
# Please visit https://www.anleo.top
# Copyrights reserved by Chongqing University
# ~~~~~~~~~~~~~~~~~~~~
# coding=utf-8
import math
import sys
ClassCode =  [ '财经','房产','股票','家居','教育','科技','社会','时尚','时政','体育','游戏','娱乐' ]
textCutBasePath = "E:/cutTHUCNews/"
testDocumentCount = 20
documentCount = 5000
trainDocumentCount = 60000

# 读取特征
def readFeature(featureName):
    featureFile = open(featureName, 'r', encoding='utf-8')
    featureContent = featureFile.read().split('\n')
    featureFile.close()
    feature = list()
    for eachfeature in featureContent:
        eachfeature = eachfeature.split(" ")
        if (len(eachfeature)==2):
            feature.append(eachfeature[1])
    return feature

# 读取特征的文档计数
def readDfFeature(dffilename):
    dffeaturedic = dict()
    dffile = open(dffilename, "r", encoding='utf-8')
    dffilecontent = dffile.read().split("\n")
    dffile.close()
    for eachline in dffilecontent:
        eachline = eachline.split(" ")
        if len(eachline) == 2:
            dffeaturedic[eachline[0]] = eachline[1]
            # print(eachline[0] + ":"+eachline[1])
    # print(len(dffeaturedic))
    return dffeaturedic

# 对测试集进行特征向量表示
def readFileToList(textCutBasePath, ClassCode, documentCount, testDocumentCount):
    dic = dict()
    for eachclass in ClassCode:
        currClassPath = textCutBasePath + eachclass + "/"
        eachclasslist = list()
        
        for i in range(documentCount, documentCount+testDocumentCount):
            #print(currClassPath+str(i)+".cut")
            eachfile = open(currClassPath+str(i)+".txt", 'r', encoding='utf-8')
            eachfilecontent = eachfile.read()
            eachfilewords = eachfilecontent.split(" ")
            eachclasslist.append(eachfilewords)
            # print(eachfilewords)
        dic[eachclass] = eachclasslist
    return dic

def TFIDFCal(feature, dic,dffeaturedic,filename):
    file = open(filename, 'w', encoding='utf-8')
    file.close()
    file = open(filename, 'a', encoding='utf-8')
    # classid = 0
    for key in dic:
        # print(key)
        classFiles = dic[key]
        classid = ClassCode.index(key)
        for eachfile in classFiles:
            # 对每个文件进行特征向量转化
            file.write(str(classid)+" ")
            for i in range(len(feature)):
                if feature[i] in eachfile:
                    currentfeature = feature[i]
                    featurecount = eachfile.count(feature[i])
                    tf = float(featurecount)/(len(eachfile))
                    # 计算逆文档频率
                    idffeature = math.log(float(trainDocumentCount+1)/(int(dffeaturedic[currentfeature])+2))
                    featurevalue = idffeature * tf
                    file.write(str(i+1)+":"+str(featurevalue) + " ")
            file.write("\n")

if __name__ == '__main__':
    # 对200至250序号的文档作为测试集
    feature = readFeature("classFeature.txt")
    dffeaturedic = readDfFeature("classDfFeature.txt")
    dic = readFileToList(textCutBasePath, ClassCode, documentCount, testDocumentCount)
    TFIDFCal(feature, dic, dffeaturedic, "test.svm")
