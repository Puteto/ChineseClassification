# ~~~~~~~~~~~~~~~~~~~~
# Code by Anleo YUAN
# Please visit https://www.anleo.top
# Copyrights reserved by Chongqing University
# ~~~~~~~~~~~~~~~~~~~~
# 使用卡方检验选择特征
# coding=utf-8
# 按UTF-8编码格式读取文件
import codecs
import math
import sys

ClassCode =  [ '财经','房产','股票','家居','教育','科技','社会','时尚','时政','体育','游戏','娱乐' ]
# 构建每个类别的词Set
# 分词后的文件路径
textCutBasePath = "E:/cutTHUCNews/"

# 构建每个类别的词向量
def buildItemSets(classDocCount):
    termDic = dict()
    
    # 每个类别下的文档集合用list<set>表示, 每个set表示一个文档，整体用一个dict表示
    termClassDic = dict()
    for eachclass in ClassCode:
        currClassPath = textCutBasePath+eachclass+"/"
        eachClassWordSets = set()
        eachClassWordList = list()
        for i in range(classDocCount):
            eachDocPath = currClassPath+str(i)+".txt"
            eachFileObj = open(eachDocPath, 'r', encoding='utf-8')
            eachFileContent = eachFileObj.read()
            eachFileWords = eachFileContent.split(" ")
            eachFileSet = set()
            for eachword in eachFileWords:
                stripEachWord = eachword.strip(" ")
                if len(stripEachWord) > 0:
                    eachFileSet.add(eachword)
                    eachClassWordSets.add(eachword)
            eachClassWordList.append(eachFileSet)
        termDic[eachclass] = eachClassWordSets
        termClassDic[eachclass] = eachClassWordList
    return termDic, termClassDic



# 对得到的两个词典进行计算，可以得到a b c d 值
# K为每个类别选取的特征个数
# 卡方计算公式
def ChiCalc(a, b, c, d):
    result = float(pow((a*d - b*c), 2)) /float((a+c) * (a+b) * (b+d) * (c+d))
    return result

def featureSelection(termDic, termClassDic, K):
    termCountDic = dict()
    for key in termDic:
        # C000008  
        classWordSets = termDic[key]
        # print(classWordSets)
        classTermCountDic = dict()
        for eachword in classWordSets:  # 对某个类别下的每一个单词的 a b c d 进行计算
            # 对卡方检验所需的 a b c d 进行计算
            # a：在这个分类下包含这个词的文档数量
            # b：不在该分类下包含这个词的文档数量
            # c：在这个分类下不包含这个词的文档数量
            # d：不在该分类下，且不包含这个词的文档数量
            a = 0
            b = 0
            c = 0
            d = 0
            for eachclass in termClassDic:
                # C000008
                if eachclass == key: #在这个类别下进行处理
                    for eachdocset in termClassDic[eachclass]:
                        if eachword in eachdocset:
                            a = a + 1
                        else:
                            c = c + 1
                else: # 不在这个类别下进行处理
                    for eachdocset in termClassDic[eachclass]:
                        if eachword in eachdocset:
                            b = b + 1
                        else:
                            d = d + 1

            eachwordcount = ChiCalc(a, b, c, d)
            classTermCountDic[eachword] = eachwordcount
        
        # 对生成的计数进行排序选择前K个
        # 这个排序后返回的是元组的列表
        sortedClassTermCountDic = sorted(classTermCountDic.items(), key=lambda d:d[1], reverse=True)
        count = 0
        subDic = dict()
        for i in range(K):
            subDic[sortedClassTermCountDic[i][0]] = sortedClassTermCountDic[i][1]
        termCountDic[key] = subDic
    return termCountDic


def writeFeatureToFile(termCountDic , fileName):
    featureSet = set()
    for key in termCountDic:
        for eachkey in termCountDic[key]:
            featureSet.add(eachkey)
    
    count = 1
    file = open(fileName, 'w', encoding='utf-8')
    for feature in featureSet:
        # 判断feature 不为空
        stripfeature = feature.strip(" ")
        if len(stripfeature) > 0 and feature != " " :
            file.write(str(count)+" " +feature+"\n")
            count = count + 1
            # print(feature)
    file.close()

if __name__ == '__main__':
    # 调用buildItemSets
    # buildItemSets形参表示每个类别的文档数目,在这里训练模型时每个类别取前10000个文件
    termDic, termClassDic = buildItemSets(100)
    termCountDic = featureSelection(termDic, termClassDic, 2)
    writeFeatureToFile(termCountDic, "SVMFeature.txt")
    print("结束")















