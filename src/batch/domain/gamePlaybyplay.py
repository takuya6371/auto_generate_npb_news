# coding: UTF-8
from bs4 import BeautifulSoup
import re

from util.file import fileRead

# 試合の１個１個のプレイ情報を生成する
class GamePlaybyplay:
    def extractPlaybyplay(self, soup):
        playByplayData = {}
        currentIning = ''
        playCnt = 1

        # 要素から１個１個プレイを抽出
        playbyplayAll = soup.find(id='progress')
        for i, element in enumerate(playbyplayAll.find_all(['tr', re.compile("^h")])):
            if i == 0:
                continue
            if 'id' in element.attrs and 'com' in element['id']:
                currentIning = element['id']
                playCnt = 1
                playByplayData[currentIning] = []
            else:
                td_list = []
                for td in element.find_all('td'):
                    td_list.append(td.text)
                if '投手' in element.text:
                    playByplayData[currentIning].append(
                        {'play-'+str(playCnt): td_list, 'play_type': 'pitcher'})
                    playCnt += 1
                elif '盗塁' in element.text:
                    playByplayData[currentIning].append(
                        {'play-'+str(playCnt): td_list, 'play_type': 'runner'})
                    playCnt += 1
                else:
                    playByplayData[currentIning].append(
                        {'play-'+str(playCnt): td_list, 'play_type': 'batther'})
                    playCnt += 1

        return {'playbyplay': playByplayData}

    def process (self, filePath):
        print("extract playbyplay start")
        html = fileRead(filePath)
        soup = BeautifulSoup(html, 'lxml')
        gameStatus = soup.find(class_='game_info').text
        if not '試合終了' in gameStatus:
            return None
        playByplayData = self.extractPlaybyplay(soup)
        return playByplayData
