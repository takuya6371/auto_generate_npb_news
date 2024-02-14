import json
import os
import util.file as file

# abs path
absPath = os.path.dirname(os.path.abspath(__file__))
homePath = '/'.join(absPath.split('/')[0:-3])
dataPath = homePath + '/data/'

# ニュースデータを取得、現状JSONファイルから取得している

def getNews(targetYear, targetMonth, targetDate):
    newsDfs = []
    newsList = file.listFiles(
                dataPath + 'json/' + targetYear + targetMonth + '/' 
                + targetYear + targetMonth + targetDate
            )
    for news in newsList:
        with open(news) as f:
            newsDfs.append(json.load(f))
    return newsDfs

