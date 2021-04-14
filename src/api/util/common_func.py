# coding: UTF-8
import api.util.npb_const as nc


def trans_play_name(play, get_score, f):
    if 'ホームラン' in play:
        play_name = nc.PLAY_SHORT_NAME[play]
    else:
        if int(get_score) > 1:
            play_name = str(get_score) + '点' + nc.PLAY_SHORT_NAME[play] if play in nc.PLAY_SHORT_NAME else play
        else:
            play_name =  nc.PLAY_SHORT_NAME[play] if play in nc.PLAY_SHORT_NAME else play
    return play_name


def compare_game_status(
    current_up_down,
    current_inning_num,
    highlight_inning,
    highlight_scenario,
    current_score_target,
    current_score_other,
    current_get_score,
    ining_begin_score,
    highlight_inning_begin_score,
    highlight_inning_get_score,
    has_additional_points,
):
    # sensei
    if highlight_inning == '' and current_score_target > current_score_other:
        highlight_inning = str(current_inning_num) + '-' + str(current_up_down)
        highlight_scenario = nc.SENSEI
        highlight_inning_begin_score = ining_begin_score
        highlight_inning_get_score = current_get_score
        has_additional_points = False
    # katikosi
    elif (not highlight_inning == ''
          and not highlight_scenario == nc.SENSEI
          and not highlight_scenario == nc.KATIKOSI
          and not highlight_scenario == nc.GYAKUTEN
          and current_score_target > current_score_other):

        highlight_inning = str(current_inning_num) + '-' + str(current_up_down)
        highlight_scenario = nc.KATIKOSI
        highlight_inning_begin_score = ining_begin_score
        highlight_inning_get_score = current_get_score
        has_additional_points = False
    # gyakuten
    elif (not highlight_inning == ''
          and not str(highlight_inning).split('-')[1] == current_up_down
          and current_score_target > current_score_other):

        highlight_inning = str(current_inning_num) + '-' + str(current_up_down)
        highlight_scenario = nc.GYAKUTEN
        highlight_inning_begin_score = ining_begin_score
        highlight_inning_get_score = current_get_score
        has_additional_points = False
    # oituki
    elif (not highlight_scenario == nc.OITUKI
          and not highlight_inning == ''
          and not highlight_inning.split('-')[1] == current_up_down
          and current_score_target == current_score_other):

        highlight_inning = str(current_inning_num) + '-' + str(current_up_down)
        highlight_scenario = nc.OITUKI
        highlight_inning_begin_score = ining_begin_score
        highlight_inning_get_score = current_get_score
        has_additional_points = False
    # tuikaten
    elif ((highlight_scenario == nc.SENSEI
           or highlight_scenario == nc.KATIKOSI
           or highlight_scenario == nc.GYAKUTEN)
          and current_get_score > 0):
        has_additional_points = True

    return highlight_inning, highlight_scenario, highlight_inning_begin_score, int(highlight_inning_get_score), has_additional_points


def list_hilight_ining_play_with_score(visitor_score_board,
                                       home_score_board,
                                       hilight_ining_num,
                                       hilight_ining_up_down,
                                       hilight_scenario,
                                       playbyplay,
                                       hilight_ining_begin_score
                                       ):
    print(visitor_score_board)
    if int(hilight_ining_up_down) == 1:
        hilight_ining_get_score = visitor_score_board[hilight_ining_num]
    else:
        hilight_ining_get_score = home_score_board[hilight_ining_num]

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
                nc.runner_cnt_list[play['play-'+str(i + 1)][1].strip()])
            player = play['play-'+str(i + 1)][2]
            by_play = play['play-'+str(i + 1)][4]
            print(out_cnt, runner_cnt, player, by_play)
            if before_type == 'runner':
                runner_cnt_up = 0
            else:
                runner_cnt_up = 1

            if before_get_score == 0:
                # ランナーの前後とアウトカウントで得点を推測
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
    if not hilight_ining_get_score == get_score:
        score_play_list.append({'play': before_play, 'get_score': get_score,
                                'current_score_diff': current_score_diff, 'player': before_player})

    print("score_list"+str(score_play_list))
    return score_play_list


def make_hilight_ining_play_sentence(hilight_play_list, hilight_ining, f):
    print(len(hilight_play_list), file=f)
    print('hilight_play_list')
    print(hilight_play_list)
    if int(hilight_ining.split('-')[0]) >= 9 and int(hilight_ining.split('-')[1]) == 2:
        pickup_play = hilight_play_list[len(hilight_play_list)-1]['player'] + 'の' \
            + (trans_play_name(nc.PLAY_SHORT_NAME[hilight_play_list[len(hilight_play_list)-1]['play']], hilight_play_list[len(hilight_play_list)-1]['get_score'], f) if hilight_play_list[len(hilight_play_list)-1]['play'] in nc.PLAY_SHORT_NAME else trans_play_name(hilight_play_list[len(hilight_play_list)-1]['play'], hilight_play_list[len(hilight_play_list)-1]['get_score'], f)) \
            + 'で'

    else:
        if len(hilight_play_list) > 1:
            sorted_hilight_play_list = sorted(
                hilight_play_list, key=lambda x: x['get_score'], reverse=True)
            print(sorted_hilight_play_list, file=f)
            pickup_play = sorted_hilight_play_list[0]['player'] + 'の' \
                + (nc.PLAY_SHORT_NAME[sorted_hilight_play_list[0]['play']] \
                if sorted_hilight_play_list[0] ['play'] in nc.PLAY_SHORT_NAME else sorted_hilight_play_list[0]['play']) \
                + '、' + sorted_hilight_play_list[1]['player'] + 'の' + (nc.PLAY_SHORT_NAME[sorted_hilight_play_list[1]['play']] \
                if sorted_hilight_play_list[1] ['play'] in nc.PLAY_SHORT_NAME else sorted_hilight_play_list[1]['play'])
            print(pickup_play, file=f)
            if len(hilight_play_list) > 2:
                pickup_play_end = 'など'
            else:
                pickup_play_end = ''
            pickup_play += pickup_play_end
        else:
            pickup_play = hilight_play_list[0]['player'] + 'の' \
                + nc.PLAY_SHORT_NAME[hilight_play_list[0]['play']]\
                if hilight_play_list[0]['play'] in nc.PLAY_SHORT_NAME \
                else hilight_play_list[0]['play'] + ''

    return pickup_play


def make_hilight_ining_sayonara_play_sentence(hilight_play_list, f):
    print(len(hilight_play_list), file=f)
    pickup_play = hilight_play_list[len(hilight_play_list)-1]['player'] + 'の'
    + nc.PLAY_SHORT_NAME[hilight_play_list[len(hilight_play_list)-1]['play']] if hilight_play_list[len(
        hilight_play_list)-1]['play'] in nc.PLAY_SHORT_NAME else hilight_play_list[len(hilight_play_list)-1]['play']
    + 'で'

    return pickup_play
