# ~~~~~~~~~~~~~~~~~~~~
# Code by Anleo YUAN
# Please visit https://www.anleo.top
# Copyrights reserved by Chongqing University
# ~~~~~~~~~~~~~~~~~~~~
# coding=utf-8
# import FeatureSelecion
import math
import sys
# 采用TF-IDF 算法对选取得到的特征进行计算权重
documentCount = 5000 # 每个类别选取10000篇文档

ClassCode =  [ '财经','房产','股票','家居','教育','科技','社会','时尚','时政','体育','游戏','娱乐' ]
# 构建每个类别的词Set
# 分词后的文件路径
textCutBasePath = "E:/cutTHUCNews/"

def readFeature(featureName):
    featureFile = open(featureName, 'r', encoding='utf-8')
    featureContent = featureFile.read().split('\n')
    featureFile.close()
    feature = list()
    for eachfeature in featureContent:
        eachfeature = eachfeature.split(" ")
        if (len(eachfeature)==2):
            feature.append(eachfeature[1])
    # print(feature)
    return feature

# 读取所有类别的训练样本到字典中,每个文档是一个list
def readFileToList(textCutBasePath, ClassCode, documentCount):
    dic = dict()
    for eachclass in ClassCode:
        currClassPath = textCutBasePath + eachclass + "/"
        eachclasslist = list()
        for i in range(documentCount):
            eachfile = open(currClassPath+str(i)+".txt", 'r', encoding='utf-8')
            eachfilecontent = eachfile.read()
            eachfilewords = eachfilecontent.split(" ")
            eachclasslist.append(eachfilewords)
            # print(eachfilewords)
        dic[eachclass] = eachclasslist
    return dic

# 计算特征的逆文档频率
def featureIDF(dic, feature, dffilename):
    dffile = open(dffilename, "w", encoding='utf-8')
    dffile.close()
    dffile = open(dffilename, "a", encoding='utf-8')
    

    idffeature = dict()
    dffeature = dict()
    
    for eachfeature in feature:
        docFeature = 0
        totalDocCount = 0
        for key in dic:
            totalDocCount = totalDocCount + len(dic[key])
            classfiles = dic[key]
            for eachfile in classfiles:
                if eachfeature in eachfile:
                    docFeature = docFeature + 1
        # 计算特征的逆文档频率
        featurevalue = math.log(float(totalDocCount)/(docFeature+1))
        dffeature[eachfeature] = docFeature
        # 写入文件，特征的文档频率
        dffile.write(eachfeature + " " + str(docFeature)+"\n")
        # print(eachfeature+" "+str(docFeature))
        idffeature[eachfeature] = featurevalue
    dffile.close()
    return idffeature

# 计算Feature's TF-IDF 值
def TFIDFCal(feature, dic,idffeature,filename):
    file = open(filename, 'w', encoding='utf-8')
    file.close()
    file = open(filename, 'a', encoding='utf-8')
    for key in dic:
        classFiles = dic[key]
        # 谨记字典的键是无序的
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
                    featurevalue = idffeature[currentfeature]*tf
                    file.write(str(i+1)+":"+str(featurevalue) + " ")
            file.write("\n")

if __name__ == '__main__':
    dic = readFileToList(textCutBasePath, ClassCode, documentCount)
    feature = readFeature("SVMFeature.txt")
    # print(len(feature))
    idffeature = featureIDF(dic, feature, "dffeature.txt")
    TFIDFCal(feature, dic,idffeature, "train.svm")
    print("结束")











