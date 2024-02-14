# coding: UTF-8
import json
import os
from repository.news import getNews
from domain.newsSentenseHead import NewsSentenseHead
from domain.gameHightlightIning import GameHightlightIning
from domain.gameHightlightPlays import GameHightlightPlays
from domain.newsSentenseGameDetail import NewsSentenseGameDetail

import util.file as file

# abs path
absPath = os.path.dirname(os.path.abspath(__file__))
homePath = '/'.join(absPath.split('/')[0:-3])
dataPath = homePath + '/data/'

# ニュース文を生成するユースケース
class GenerateNews:
    def getJsonList(self, year, month, date):
        files = file.listFiles(
            dataPath + 'json/' + year + month + '/' + year + month + date
        )
        return files

    def process(self, targetYear, targetMonth, targetDate):
        gameResultList = []
        print("generateNews start")
        fileList = self.getJsonList(targetYear, targetMonth, targetDate)
        newsList = getNews(targetYear, targetMonth, targetDate)
        if len(fileList) == 0:
            return ''
        for news in newsList:
            gameHightlightIning = GameHightlightIning().process(
                news['visitor_score_board'],
                news['home_score_board'],
            )
            sentenceHead = NewsSentenseHead().process(news)
            hightlightInningPlays = GameHightlightPlays().process(
                gameHightlightIning,
                news['playbyplay'],
            )
            sentenseGameDetail = NewsSentenseGameDetail().process(
                news['home_team'],
                news['visitor_team'],
                gameHightlightIning,
                hightlightInningPlays,
            )
            with open('news.txt', 'a') as f:
                print(sentenceHead, file=f)
                print(sentenseGameDetail, file=f)
            gameResultList.append(sentenceHead + sentenseGameDetail)
        return gameResultList
