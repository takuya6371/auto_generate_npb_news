# coding: UTF-8
import sys
import os
from batch.usecase.download_npb_game_page import DownloadNpbGamePage
from batch.usecase.generate_json import GenerateJson
sys.path.append(os.path.abspath(".."))

class GenerateNpbNewsData:
    def __init__(self, year, month, date):
        abs_path = os.path.dirname(os.path.abspath(__file__))
        home_path = '/'.join(abs_path.split('/')[0:-3])
        data_path = home_path + '/data/'
        self.download_npb_game_page_class = DownloadNpbGamePage(year, month, date, data_path);
        self.generate_json = GenerateJson(year, month, date, data_path);

    def main_process (self):
        self.download_npb_game_page_class.run()
        self.generate_json.run()
