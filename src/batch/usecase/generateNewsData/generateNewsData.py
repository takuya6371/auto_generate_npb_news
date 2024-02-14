# coding: UTF-8
from io import FileIO
import os
from typing import Literal
from domain.gameIndex import GameIndex
from domain.gamePlaybyplay import GamePlaybyplay
from util.file import createFolder, jsonDump, clearDirectory, listFiles, jsonFileRead

# 試合結果をデータ化する
class GenerateNewsData:
    def __init__(self, year, month, date, dataPath):
        self.year = year
        self.month = month
        self.date = date
        self.dataPath = dataPath
        self.jsonPath = self.dataPath + 'json/' + self.year + self.month + '/' + self.year + self.month + self.date

    # 実行環境のパスを作成
    def makeDirectory (self):
        # month 
        createFolder(self.dataPath + 'json/' + self.year + self.month)
        # date
        createFolder(self.jsonPath)
        # フォルダ内をクリア
        clearDirectory(self.jsonPath)

    def prosess (self):
        print("Generate json start")
        # データ生成するhtmlファイルリストを取得
        filePaths = listFiles(self.dataPath + 'html/' +
            self.year + self.month + '/' + self.year + self.month + self.date)
        if len(filePaths) == 0:
            print('no html file:' + self.year, self.month, self.date)
            return
        # jsonファイル用のパスを作成
        self.makeDirectory()
        # 読み込む必要のないファイルをリストから削除
        filePaths = [i for i in filePaths if '_box' not in i]
        #del filePaths[2:]
        for filePath in filePaths:
            targetJsonFilePath = self.jsonPath + '/' + \
                filePath.split('/')[-1].split('.')[0].rsplit('_', 1)[0]+'.json'
            # 書き込み対象のJSONが存在する場合その値を取得
            targetJsonData = jsonFileRead(targetJsonFilePath) if os.path.isfile(targetJsonFilePath) else {}
            # ファイルの種類に応じてデータ取得
            if 'index' in filePath:
                extractData = GameIndex().process(filePath)
            elif 'playbyplay' in filePath:
                # 試合が終了していない場合playByplayDataが取得できな場合があるのでスキップ
                if not targetJsonData['game_status'] == '試合終了':
                    break
                extractData = GamePlaybyplay().process(filePath)
            # 取得したデータをjsonデータに挿入
            targetJsonData.update(extractData)
            # jsonに書き込み
            jsonDump(targetJsonFilePath, targetJsonData, 'w')
