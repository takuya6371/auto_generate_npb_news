# coding: UTF-8
import json
import os
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
        with open('print.txt', 'w') as f:
            print(' ', file=f)

        fileList = self.getJsonList(targetYear, targetMonth, targetDate)
        if len(fileList) == 0:
            return ''
        for file in fileList:
            with open(file) as f:
                df = json.load(f)
                gameHightlightIning = GameHightlightIning().process(
                    df['visitor_score_board'],
                    df['home_score_board'],
                )
                sentenceHead = NewsSentenseHead().process(df)
                hightlightInningPlays = GameHightlightPlays().process(
                    gameHightlightIning,
                    df['playbyplay'],
                )
                sentenseGameDetail = NewsSentenseGameDetail().process(
                    df['home_team'],
                    df['visitor_team'],
                    gameHightlightIning,
                    hightlightInningPlays,
                )
                with open('print.txt', 'a') as f:
                    print(sentenceHead, file=f)
                    print(sentenseGameDetail, file=f)
                gameResultList.append(sentenceHead + sentenseGameDetail)
        return gameResultList
