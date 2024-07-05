# ~~~~~~~~~~~~~~~~~~~~
# Code by Anleo YUAN
# Please visit https://www.anleo.top
# Copyrights reserved by Chongqing University
# ~~~~~~~~~~~~~~~~~~~~
# coding=utf-8

posDicName = "positiveDic.txt"
nefDicName = "negativeDic.txt"
featureName = "SVMFeature.txt"
combineName = "featureComb.txt"

# 读取特征set
def readFeature(featureName):
    featureFile = open(featureName, 'r', encoding='utf-8')
    featureContent = featureFile.read().split('\n')
    featureFile.close()
    feature = set()
    for eachfeature in featureContent:
        eachfeature = eachfeature.split(" ")
        if (len(eachfeature)==2):
            feature.add(eachfeature[1])
    # print(feature)
    return feature

def combineDic(dicName, featureSet):
    dicFile = open(dicName, 'r', encoding='utf-8')
    dicContent = dicFile.read().split('\n')
    dicFile.close()
    for eachfeature in dicContent:
        featureSet.add(eachfeature)
    return featureSet

def writeComb(featureSet, fileName):
    count = 1
    file = open(fileName, 'w', encoding='utf-8')
    for feature in featureSet:
        # 判断feature 不为空
        stripfeature = feature.strip(" ")
        if len(stripfeature) > 0 and feature != " " :
            file.write(str(count)+" " +feature+"\n")
            count = count + 1
    file.close()

if __name__ == '__main__':
    feature = readFeature(featureName)
    feature = combineDic(posDicName, feature)
    feature = combineDic(nefDicName, feature)
    writeComb(feature, combineName)
    print('结束')