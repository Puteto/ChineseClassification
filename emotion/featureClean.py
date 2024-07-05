# ~~~~~~~~~~~~~~~~~~~~
# Code by Anleo YUAN
# Please visit https://www.anleo.top
# Copyrights reserved by Chongqing University
# ~~~~~~~~~~~~~~~~~~~~
dfFlieName = "emotionDfFeature.txt"
writeName = "dfFeature.txt"
featureFinal = "featureFinal.txt"
finalContent = []
featureContent = []
dfFile = open(dfFlieName, 'r', encoding='utf-8')
dfContent = dfFile.read().split("\n")
dfFile.close()
i = 0
for eachline in dfContent:
    eachline = eachline.split(" ")
    if len(eachline) == 2 and eachline[1] != '0':
        i += 1
        finalContent.append(eachline[0] + " " + eachline[1])
        featureContent.append(str(i) + " " + eachline[0])
finalStr = "\n".join(finalContent)
featureStr = "\n".join(featureContent)
with open(writeName, 'w', encoding='utf-8') as f:
    f.write(finalStr)
with open(featureFinal, 'w', encoding='utf-8') as f:
    f.write(featureStr)