# coding: UTF-8
from bs4 import BeautifulSoup
import re
import os
from util.file import fileRead, createFolder, fileWrite
from constant import URL_HEAD
from util.downloadHtml import downloadHtml

# 試合結果を持つページのHtmlファイルをダウンロード
class DownloadNpbGameHtml:

    def __init__(self, year, month, date, dataPath):
        self.year = year
        self.month = month
        self.date = date
        self.dataPath = dataPath
        self.monthFolderPath = self.dataPath + 'html/' + self.year + self.month
        self.dateFolderPath = self.dataPath + 'html/' + self.year + self.month + '/' + self.year + self.month + self.date

    # スケジュールページをダウンロード
    def downloadNpbGameSchedule(self):
        createFolder(self.dataPath + 'html/schedule/')
        targetUrl = URL_HEAD + 'games/' + self.year + '/schedule_' + self.month + '_detail.html'
        dlHtmlPath = self.dataPath + 'html/schedule/' + self.year + self.month + '_schedule.html'
        if not os.path.exists(dlHtmlPath):
            try:
                html = downloadHtml(targetUrl)
                fileWrite(dlHtmlPath, html.text)
            except:
                print("failed")
                return None
        return dlHtmlPath

    # スケジュールの必要なリンクを取得
    def getLinksInSchedule(self, scheduleHtmlPath):
        html = fileRead(scheduleHtmlPath)
        soup = BeautifulSoup(html, 'lxml')
        # 指定した日のリンクを取得
        parsedLinks = soup.find_all(
            "a", href=re.compile('/' + self.year + '/' + self.month + self.date))
        return parsedLinks

    # 試合結果ページをダウンロード
    def downloadNpbGameResult (self, links):
        # ダウンロード用のフォルダー作成
        createFolder(self.monthFolderPath)
        createFolder(self.dateFolderPath)
        for link in links:
            url = link.get("href")
            gameCard = url.split('/')[-2]
            for contentType in ['index', 'playbyplay', 'box']:
                path = self.dateFolderPath + '/' + self.year + \
                    self.month + self.date + '_' + gameCard + '_' + contentType + '.html'
                if not os.path.exists(path):
                    html = downloadHtml(URL_HEAD + url + contentType + '.html')
                    fileWrite(path, html.text)

    def prosess (self):
        print("Download Html start")
        scheduleHtmlPath = self.downloadNpbGameSchedule()
        links = self.getLinksInSchedule(scheduleHtmlPath)
        self.downloadNpbGameResult(links)

  
