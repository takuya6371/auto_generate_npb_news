# coding: UTF-8
import os
import json
import time
import glob
import npb_const
import common_func
import numpy as np

# target year
target_year = '2020'
# target month
target_month = '07'
# target date
target_date = '21'


def get_json_list(year, month, date):
    file_list = glob.glob(npb_const.data_path +
                          'json/' + year + month + '/' + year + month + date + '/*')
    return file_list

# return win,lose team name


def win_lose_team(visitor_team, visitor_score_board, home_team, home_score_board):
    visitor_score = visitor_score_board['total']
    home_score = home_score_board['total']

    if int(visitor_score) == int(home_score):
        win_team, lose_team = '', ''
    elif int(visitor_score) > int(home_score):
        win_team, lose_team = visitor_team, home_team
    else:
        win_team, lose_team = home_team, visitor_team

    return win_team, lose_team

# return game synario


def define_game_scenario(visitor_team, visitor_score_board, home_team, home_score_board, playbyplay):
    ining_cnt = len(visitor_score_board) - 3
    hilight_ining_begin_score = []
    current_score_vis = 0
    current_score_home = 0
    hilight_ining_get_score = 0
    tuikaten_flg = False
    synario_flg = ''
    hilight_synario = ''
    # even visitor home
    hilight_ining_up_down = ''
    # 0=even 1=katikosi 2=gyakuten 3=oituki
    process = 0
    hilight_ining = ''
    print(ining_cnt)
    for i in range(ining_cnt):

        # See up ining
        # current score
        ining_begin_score = [current_score_vis, current_score_home]
        # plus score in current ining
        current_score_vis += int(
            visitor_score_board[str(i+1)].replace('x', '0').replace('', '0'))
        # find whether critical score or not
        hilight_ining, hilight_synario, hilight_ining_begin_score, hilight_ining_get_score, tuikaten_flg = common_func.compare_game_status(
            '1',
            str(i+1),
            hilight_ining,
            hilight_synario,
            current_score_vis,
            current_score_home,
            int(visitor_score_board[str(i+1)
                                    ].replace('x', '0').replace('', '0')),
            ining_begin_score,
            hilight_ining_begin_score,
            hilight_ining_get_score,
            tuikaten_flg,
        )

        # See down ining
        # adapt score in up ining
        ining_begin_score = [current_score_vis, current_score_home]
        # plus score in current ining
        print(home_score_board[str(i+1)])

        current_score_home += int(
            home_score_board[str(i+1)].replace('x', '0').replace('', '0'))
        # find whether critical score or not
        hilight_ining, hilight_synario, hilight_ining_begin_score, hilight_ining_get_score, tuikaten_flg = common_func.compare_game_status(
            '2',
            str(i+1),
            hilight_ining,
            hilight_synario,
            current_score_home,
            current_score_vis,
            int(home_score_board[str(i+1)].replace('x', '0').replace('', '0')),
            ining_begin_score,
            hilight_ining_begin_score,
            hilight_ining_get_score,
            tuikaten_flg,
        )

    hilight_ining_num = hilight_ining.split("-")[0]
    hilight_ining_up_down = hilight_ining.split("-")[1]
    if int(hilight_ining_up_down) == 1:
        hilight_team = visitor_team
    else:
        hilight_team = home_team
    with open('print.txt', 'a') as f:
        print('synario:'+hilight_synario, file=f)
        print('hilight_ining:'+hilight_ining, file=f)
        print('visitor team:'+str(visitor_team), file=f)
        print('home team  :'+str(home_team), file=f)
        print('visitor:'+str(visitor_score_board.values()), file=f)
        print('home   :'+str(home_score_board.values()), file=f)
        print('hilight team   :'+hilight_team, file=f)
        print('hilight_ining_get_score   :' +
              str(hilight_ining_get_score), file=f)
        # tuikaten
        if tuikaten_flg:
            sentense_end = 'その後も追加点を上げました。'
        else:
            sentense_end = 'ました。'
        print(tuikaten_flg, file=f)
        print(hilight_ining_num, hilight_ining_up_down,
              process, hilight_ining_begin_score, file=f)
        hilight_play_list = common_func.list_hilight_ining_play_with_score(
            visitor_score_board,
            home_score_board,
            hilight_ining_num,
            hilight_ining_up_down,
            hilight_synario,
            playbyplay,
            hilight_ining_begin_score,
        )
        print(hilight_play_list)
        # find synario

        # oituki pattern(Maybe drow)
        if hilight_synario == npb_const.OITUKI:
            pickup_index = [i for i, _ in enumerate(hilight_play_list) if _[
                'current_score_diff'] == 0][0]
            print(pickup_index, file=f)
            print(hilight_play_list, file=f)
            return npb_const.TEAM_SHORT_NAME[hilight_team] + 'は' \
                + str((max(hilight_ining_begin_score) - min(hilight_ining_begin_score))) \
                + '点を追う' + str(hilight_ining.split('-')[0]) \
                + '回、' + hilight_play_list[pickup_index]['player'] \
                + 'の' + common_func.trans_play_name(hilight_play_list[pickup_index]['play'], hilight_play_list[pickup_index]['get_score'], f) \
                + 'で追いつきました。'
        # katikosi
        elif hilight_synario == npb_const.KATIKOSI:
            print(hilight_synario, file=f)
            print(len(hilight_play_list), file=f)
            print(hilight_play_list)
            highlight_play_list = common_func.make_hilight_ining_play_sentence(
                hilight_play_list, hilight_ining, f)

            return npb_const.TEAM_SHORT_NAME[hilight_team] + 'は' \
                + str(hilight_ining.split('-')[0]) + '回、' \
                + highlight_play_list \
                + 'で' + str(hilight_ining_get_score) + '点を勝ち越し' \
                + sentense_end

        # gyakuten
        elif hilight_synario == npb_const.GYAKUTEN:
            print(hilight_synario, file=f)
            print(len(hilight_play_list), file=f)
            sentence_end = 'で逆転しました。'
            highlight_play_list = common_func.make_hilight_ining_play_sentence(
                hilight_play_list, hilight_ining, f)
            if int(hilight_ining.split('-')[0]) >= 9:
                sentence_end = 'サヨナラ勝ちしました。'

            return npb_const.TEAM_SHORT_NAME[hilight_team] + 'は' \
                + str((max(hilight_ining_begin_score) - min(hilight_ining_begin_score))) \
                + '点ビハインドで迎えた' + str(hilight_ining.split('-')[0]) + '回、'\
                + highlight_play_list \
                + sentence_end

    return ''


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
        with open(file) as f:
            df = json.load(f)
            # get name of win,lose team
            win_team, lose_team = win_lose_team(
                df['visitor_team'],
                df['visitor_score_board'],
                df['home_team'],
                df['home_score_board']
            )
            # print(win_team,lose_team)
            sentence2 = define_game_scenario(
                df['visitor_team'],
                df['visitor_score_board'],
                df['home_team'],
                df['home_score_board'],
                df['playbyplay']
            )

        # first sentence
        if win_team == '':
            sentence1_end = 'で引き分けました。'
        else:
            sentence1_end = 'で' + win_team + 'が勝ちました。'
        sentence1 = df['home_team'] + '対' + df['visitor_team'] + 'は、' + df['home_score_board']['total'] + '対' \
            + df['visitor_score_board']['total'] + sentence1_end
        with open('print.txt', 'a') as f:
            print(sentence1, file=f)
            print(sentence2, file=f)
        game_result_list.append(sentence1 + sentence2)
    return {'auto_news': game_result_list}


if __name__ == '__main__':
    main_process(target_year, target_month, target_date)

'''
逃げ切りました
序盤の大量点を守りきりました。
逆転しました
勝ち越しました
値千金のタイムリーが飛び出し、そのまま逃げ切りました

'''
