# coding: UTF-8
import os
from .downloadNpbGameHtml import DownloadNpbGameHtml
from .generateNewsData import GenerateNewsData

# 試合結果をWEb情報からデータ化するユースケース
class GenerateNewsDataUseCase:
    def __init__(self, year, month, date):
        self.year = year
        self.month = month
        self.date = date
        absPath = os.path.dirname(os.path.abspath(__file__))
        homePath = '/'.join(absPath.split('/')[0:-4])
        self.dataPath = homePath + '/data/'

    def prosess (self):
        DownloadNpbGameHtml(self.year, self.month, self.date, self.dataPath).prosess()
        GenerateNewsData(self.year, self.month, self.date, self.dataPath).prosess()
