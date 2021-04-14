# coding: UTF-8
import json
import api.util.npb_const as nc
import api.util.common_func as cf
from api.domain.NewsSentenseHead import NewsSentenseHead
from api.domain.GameHightlightInfo import GameHightlightInfo
from api.domain.GameHightlightPlayList import GameHightlightPlayList
from api.domain.NewsSentenseGameDetail import NewsSentenseGameDetail

import util.file as file

# target year
target_year = '2020'
# target month
target_month = '07'
# target date
target_date = '21'

def get_json_list(year, month, date):
    print(nc.data_path)
    files = file.list_file(
        nc.data_path + 'json/' + year + month + '/' + year + month + date
    )
    return files

def main_process(target_year, target_month, target_date):
    game_result_list = []
    print("main start")
    with open('print.txt', 'w') as f:
        print(' ', file=f)

    file_list = get_json_list(target_year, target_month, target_date)
    print(file_list)
    if len(file_list) == 0:
        return ''
    for file in file_list:
        print(file)
        with open(file) as f:
            df = json.load(f)
            # get name of win,lose team
            newsSentenseHead = NewsSentenseHead(df)
            sentence_head = newsSentenseHead.run()
            gameHightlightInfo = GameHightlightInfo()
            hightlight_info = gameHightlightInfo.run(
                df['visitor_score_board'],
                df['home_score_board'],
            )
            gameHightlightPlayList = GameHightlightPlayList()
            hightlight_inning_play_list = gameHightlightPlayList.run(
                df['visitor_score_board'],
                df['home_score_board'],
                hightlight_info,
                df['playbyplay'],
            )
            newsSentenseGameDetail = NewsSentenseGameDetail()
            sentense_game_detail = newsSentenseGameDetail.run(
                df['home_team'],
                df['visitor_team'],
                hightlight_info,
                hightlight_inning_play_list,
            )
            with open('print.txt', 'a') as f:
                print(sentence_head, file=f)
                print(sentense_game_detail, file=f)
            game_result_list.append(sentence_head + sentense_game_detail)
    return game_result_list


if __name__ == '__main__':
    main_process(target_year, target_month, target_date)

'''
逃げ切りました
序盤の大量点を守りきりました。
逆転しました
勝ち越しました
値千金のタイムリーが飛び出し、そのまま逃げ切りました

'''
