# ~~~~~~~~~~~~~~~~~~~~
# Code by Anleo YUAN
# Please visit https://www.anleo.top
# Copyrights reserved by Chongqing University
# ~~~~~~~~~~~~~~~~~~~~
# coding=utf-8

fileName = "E:/weiboEmo/test.txt"
splitDir = "E:/weiboEmo/sources/消极的/"

with open(fileName, 'r', encoding='utf-8') as f:
    content = f.read()
contSplit = content.split('\n')
for i in range(len(contSplit)):
    fileCont = contSplit[i]
    splitName = splitDir + str(i) + ".txt"
    with open(splitName, 'w', encoding='utf-8') as f:
        f.write(fileCont)