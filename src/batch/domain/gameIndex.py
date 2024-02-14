# coding: UTF-8
from bs4 import BeautifulSoup
import re
from util.file import fileRead

# 試合結果の基本情報を生成する
class GameIndex:
    def extractGameSchedule (self, soup):
        returnData = {}
        # extract game info
        gameAllInfo = soup.find(class_='game_tit')
        # game place
        returnData['game_place'] = gameAllInfo.find(class_='place').text
        # game date
        returnData['game_date'] = gameAllInfo.find('time').text
        # game card count
        gameDiscription = gameAllInfo.find('h3').text.split(' ')
        listGameDiscription = filter(lambda a: a != '', gameDiscription)
        returnData['game_card_cnt'] = list(listGameDiscription)[-1]
        return returnData

    def extractGameStatus (self, soup):
        returnData = {}
        gameStatus = soup.find(class_='game_info').text
        # 中止の場合、visitor_team等はこちらで取得
        if '中止' in gameStatus or 'ノーゲーム' in gameStatus:
            visitorBoard = soup.find(class_='top')
            returnData['visitor_team'] = visitorBoard.find('span').text
            homeBoard = soup.find(class_='bottom')
            returnData['home_team'] = homeBoard.find('span').text
            returnData['game_status'] = gameStatus
            return returnData
        elif not '試合終了' in gameStatus:
            return None
        returnData['game_status'] = '試合終了'
        return returnData

    def extractGameScore (self, soup):
        returnData = {}
        score_board = {}
        score_board['visitor'] = soup.find(class_='top')
        score_board['home'] = soup.find(class_='bottom')
        for k, v in score_board.items(): 
            returnData[k + '_team'] = v.find('span', class_='hide_sp').text
            print( v.find('span', class_='hide_sp').text)

            scoreTd = v.find_all('td')
            max_ining = len(scoreTd) - 3
            score = {}
            for i in range(max_ining):
                score[i + 1] = scoreTd[i].text
            score['total'] = scoreTd[max_ining].text
            score['h'] = scoreTd[max_ining + 1].text
            score['e'] = scoreTd[max_ining + 2].text
            returnData[k + '_score_board'] = score
        return returnData

    # 試合の勝ち負け
    def extractGameResult (self, soup):
        returnData = {}
        gameResultInfo = soup.find(class_='game_result_info')
        trList = gameResultInfo.find_all('tr')
        for tr in trList:
            for k,v in {'win':'勝', 'lose':'負'}.items():
                if v in tr.find('th').text:
                    tmpText = re.split('[(（]', tr.text)
                    pitcher = re.split('[¥】]', tmpText[0])[1].replace('\n', '')
                    pitcherCurrentResult = re.split('[])¥）]', tmpText[1])[0]
                    returnData[k + '_pitcher'] = pitcher
                    returnData[k + '_pitcherCurrentResult'] = pitcherCurrentResult
        return returnData

    def process (self, filePath):
        print("extract index start")
        html = fileRead(filePath)
        soup = BeautifulSoup(html, 'lxml')
        scheduleData = self.extractGameSchedule(soup)
        statusData = self.extractGameStatus(soup)
        if statusData is None or not statusData['game_status'] == '試合終了':
            return statusData
        scoreData = self.extractGameScore(soup)
        gameResultData = self.extractGameResult(soup)
        gameResultData = dict(scheduleData, **statusData, **scoreData, **gameResultData)
        return gameResultData
