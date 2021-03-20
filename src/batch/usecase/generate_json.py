# coding: UTF-8
from io import FileIO
from typing import Literal
from batch.util.file import create_folder, json_dump, clear_directory, list_file
from batch.domain.extract_game_index import main as index_extract
from batch.domain.extract_game_playbyplay import main as playbyplay_extract

class GenerateJson:
    def __init__(self, year, month, date, data_path):
        self.year = year
        self.month = month
        self.date = date
        self.data_path = data_path
        self.json_path = self.data_path + 'json/' + self.year + self.month + '/' + self.year + self.month + self.date
        self.extract_func_list = {'index': index_extract, 'playbyplay': playbyplay_extract}
        self.json_input_data = None

    def output_game_data (self, info_type: Literal['index', 'playbyplay'], file:FileIO, data, json_file):
        print("output_game_data")
        if info_type in file:
            game_data = self.extract_func_list[info_type](file)
            if not data is None and game_data['game_status'] == '試合終了':
                data.update(game_data)
            else:
                data = game_data
            json_dump(json_file, data, 'a')

    def prepare_directory (self):
        # month folder
        create_folder(self.data_path + 'json/' + self.year + self.month)
        # check date folder
        create_folder(self.json_path)
        clear_directory(self.json_path)

    def run (self):
        print("gemerate json start")
        files = list_file(self.data_path + 'html/' +
            self.year + self.month + '/' + self.year + self.month + self.date)
        if len(files) == 0:
            print('no html file:' + self.year, self.month, self.date)
            return

        self.prepare_directory()
        for file in files:
            print('**************')
            print(file)
            json_file = self.json_path + '/' + \
                file.split('/')[-1].split('.')[0].rsplit('_', 1)[0]+'.json'
            for type in ['index', 'playbyplay']:
                self.output_game_data(type, file, self.json_input_data, json_file)