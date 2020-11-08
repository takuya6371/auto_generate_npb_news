# coding: UTF-8
import npb_const


def trans_play_name(play, get_score, f):
    if 'ホームラン' in play:
        play_name = npb_const.PLAY_SHORT_NAME[play]
    else:
        if int(get_score) > 1:
            play_name = str(get_score) + '点' + npb_const.PLAY_SHORT_NAME[play]
        else:
            play_name = npb_const.PLAY_SHORT_NAME[play]
    return play_name


def compare_game_status(
    current_up_down,
    current_ining_num,
    hilight_ining,
    hilight_synario,
    current_score_target,
    current_score_other,
    current_get_score,
    ining_begin_score,
    hilight_ining_begin_score,
    hilight_ining_get_score,
    tuikaten_flg,
):
    # sensei
    if hilight_ining == '' and current_score_target > current_score_other:
        hilight_ining = str(current_ining_num) + '-' + str(current_up_down)
        hilight_synario = npb_const.SENSEI
        hilight_ining_begin_score = ining_begin_score
        hilight_ining_get_score = current_get_score
        tuikaten_flg = False
    # katikosi
    elif (not hilight_ining == ''
          and not hilight_synario == npb_const.SENSEI
          and not hilight_synario == npb_const.KATIKOSI
          and not hilight_synario == npb_const.GYAKUTEN
          and current_score_target > current_score_other):

        hilight_ining = str(current_ining_num) + '-' + str(current_up_down)
        hilight_synario = npb_const.KATIKOSI
        hilight_ining_begin_score = ining_begin_score
        hilight_ining_get_score = current_get_score
        tuikaten_flg = False
    # gyakuten
    elif (not hilight_ining == ''
          and not str(hilight_ining).split('-')[1] == current_up_down
          and current_score_target > current_score_other):

        hilight_ining = str(current_ining_num) + '-' + str(current_up_down)
        hilight_synario = npb_const.GYAKUTEN
        hilight_ining_begin_score = ining_begin_score
        hilight_ining_get_score = current_get_score
        tuikaten_flg = False
    # oituki
    elif (not hilight_synario == npb_const.OITUKI
          and not hilight_ining == ''
          and not hilight_ining.split('-')[1] == current_up_down
          and current_score_target == current_score_other):

        hilight_ining = str(current_ining_num) + '-' + str(current_up_down)
        hilight_synario = npb_const.OITUKI
        hilight_ining_begin_score = ining_begin_score
        hilight_ining_get_score = current_get_score
        tuikaten_flg = False
    # tuikaten
    elif ((hilight_synario == npb_const.SENSEI
           or hilight_synario == npb_const.KATIKOSI
           or hilight_synario == npb_const.GYAKUTEN)
          and current_get_score > 0):
        tuikaten_flg = True

    return hilight_ining, hilight_synario, hilight_ining_begin_score, int(hilight_ining_get_score), tuikaten_flg


def list_hilight_ining_play_with_score(visitor_score_board,
                                       home_score_board,
                                       hilight_ining_num,
                                       hilight_ining_up_down,
                                       hilight_synario,
                                       playbyplay,
                                       hilight_ining_begin_score
                                       ):
    if hilight_ining_begin_score[0] == hilight_ining_begin_score[1]:
        current_score_diff = 0
    else:
        current_score_diff = min(hilight_ining_begin_score) - \
            max(hilight_ining_begin_score)

    score_play_list = []
    score_critical_play_list = []
    cnt_score = 0
    before_runner = -1
    before_out = 0
    before_type = ''
    before_play = ''
    before_player = ''
    before_get_score = 0

    for i, play in enumerate(playbyplay['com' + hilight_ining_num + '-' + hilight_ining_up_down]):
        print(play)
        if not play['play_type'] == 'pitcher':
            out_cnt = int(play['play-'+str(i + 1)][0].split('アウト')[0])
            runner_cnt = int(
                npb_const.runner_cnt_list[play['play-'+str(i + 1)][1].strip()])
            player = play['play-'+str(i + 1)][2]
            by_play = play['play-'+str(i + 1)][4]
            print(out_cnt, runner_cnt, player, by_play)
            if before_type == 'runner':
                runner_cnt_up = 0
            else:
                runner_cnt_up = 1

            if before_get_score == 0:
                get_score = before_runner - runner_cnt + \
                    runner_cnt_up - (out_cnt - before_out)
                print(get_score)
    #            print(before_play)
                cnt_score += get_score
                current_score_diff += get_score
                # find critical play
                if get_score > 0:
                    score_play_list.append({'play': before_play, 'get_score': get_score,
                                            'current_score_diff': current_score_diff, 'player': before_player})

            # check current play getting score
            if '打点' in by_play:
                curernt_get_score = int(by_play.split('打点')[1][:-1])
                cnt_score += curernt_get_score
                current_score_diff += curernt_get_score
                score_play_list.append({'play': by_play.split('（')[0], 'get_score': curernt_get_score,
                                        'current_score_diff': current_score_diff, 'player': before_player})
            else:
                curernt_get_score = 0
            print(curernt_get_score)
            # print(out_cnt,runner_cnt,get_score)
            before_out = out_cnt
            before_runner = runner_cnt
            before_play = by_play.split('（')[0]
            before_player = player
            before_type = play['play_type']
            before_get_score = curernt_get_score

    # print(cnt_score)
    print("score_list"+str(score_play_list))
    return score_play_list


def make_hilight_ining_play_sentence(hilight_play_list, hilight_ining, f):
    print(len(hilight_play_list), file=f)
    print('hilight_play_list')
    print(hilight_play_list)
    if int(hilight_ining.split('-')[0]) >= 9 and int(hilight_ining.split('-')[1]) == 2:
        pickup_play = hilight_play_list[len(hilight_play_list)-1]['player'] + 'の' \
            + (trans_play_name(npb_const.PLAY_SHORT_NAME[hilight_play_list[len(hilight_play_list)-1]['play']], hilight_play_list[len(hilight_play_list)-1]['get_score'], f) if hilight_play_list[len(hilight_play_list)-1]['play'] in npb_const.PLAY_SHORT_NAME else trans_play_name(hilight_play_list[len(hilight_play_list)-1]['play'], hilight_play_list[len(hilight_play_list)-1]['get_score'], f)) \
            + 'で'

    else:
        if len(hilight_play_list) > 1:
            sorted_hilight_play_list = sorted(
                hilight_play_list, key=lambda x: x['get_score'], reverse=True)
            print(sorted_hilight_play_list, file=f)
            pickup_play = sorted_hilight_play_list[0]['player'] + 'の'
            + (npb_const.PLAY_SHORT_NAME[sorted_hilight_play_list[0]['play']] if sorted_hilight_play_list[0]
               ['play'] in npb_const.PLAY_SHORT_NAME else sorted_hilight_play_list[0]['play'])
            + '、' + sorted_hilight_play_list[1]['player'] + 'の'
            + (npb_const.PLAY_SHORT_NAME[sorted_hilight_play_list[1]['play']] if sorted_hilight_play_list[1]
               ['play'] in npb_const.PLAY_SHORT_NAME else sorted_hilight_play_list[1]['play'])
            print(pickup_play, file=f)
            if len(hilight_play_list) > 2:
                pickup_play_end = 'など'
            else:
                pickup_play_end = ''
            pickup_play += pickup_play_end
        else:
            pickup_play = hilight_play_list[0]['player'] + 'の' \
                + npb_const.PLAY_SHORT_NAME[hilight_play_list[0]['play']]\
                if hilight_play_list[0]['play'] in npb_const.PLAY_SHORT_NAME \
                else hilight_play_list[0]['play'] + ''

    return pickup_play


def make_hilight_ining_sayonara_play_sentence(hilight_play_list, f):
    print(len(hilight_play_list), file=f)
    pickup_play = hilight_play_list[len(hilight_play_list)-1]['player'] + 'の'
    + npb_const.PLAY_SHORT_NAME[hilight_play_list[len(hilight_play_list)-1]['play']] if hilight_play_list[len(
        hilight_play_list)-1]['play'] in npb_const.PLAY_SHORT_NAME else hilight_play_list[len(hilight_play_list)-1]['play']
    + 'で'

    return pickup_play


"""
    # oituki after gyakuten
    '''
    elif (not hilight_ining == ''
         and  hilight_ining.split('-')[1] == current_up_down
         and hilight_synario == npb_const.OITUKI
         and current_score_target > current_score_other):

        hilight_ining = str(current_ining_num) + '-' + str(current_up_down)
        hilight_synario = npb_const.OITUKIKATIKOSI
        hilight_ining_begin_score = ining_begin_score
    '''
"""
