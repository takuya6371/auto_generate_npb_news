import api.util.npb_const as nc

class GameHightlightPlayList:
    def extract_hightlight_inning_play_list(
        self, 
        visitor_score_board,
        home_score_board,
        hightlight_info,
        playbyplay,
    ):
        print(visitor_score_board)
        print(home_score_board)
        highlight_inning_num = hightlight_info['highlight_inning'].split("-")[0]
        highlight_inning_up_down = hightlight_info['highlight_inning'].split("-")[1]

        if hightlight_info['highlight_inning_begin_score'][0] == hightlight_info['highlight_inning_begin_score'][1]:
            current_score_diff = 0
        else:
            current_score_diff = min(hightlight_info['highlight_inning_begin_score']) - \
                max(hightlight_info['highlight_inning_begin_score'])

        score_play_list = []
        cnt_score = 0
        before_runner = -1
        before_out = 0
        before_type = ''
        before_play = ''
        before_player = ''
        before_get_score = 0

        #print(playbyplay)
        for i, play in enumerate(playbyplay['com' + highlight_inning_num + '-' + highlight_inning_up_down]):
            #print(play)
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
                    current_get_score = int(by_play.split('打点')[1][:-1])
                    cnt_score += current_get_score
                    current_score_diff += current_get_score
                    score_play_list.append({'play': by_play.split('（')[0], 'get_score': current_get_score,
                                            'current_score_diff': current_score_diff, 'player': before_player})
                else:
                    current_get_score = 0
                print(current_get_score)
                # print(out_cnt,runner_cnt,get_score)
                before_out = out_cnt
                before_runner = runner_cnt
                before_play = by_play.split('（')[0]
                before_player = player
                before_type = play['play_type']
                before_get_score = current_get_score

        if get_score > 0:
            score_play_list.append({'play': before_play, 'get_score': get_score,
                                    'current_score_diff': current_score_diff, 'player': before_player})

        print("score_list"+str(score_play_list))
        return score_play_list

    def run (self, visitor_score_board, home_score_board, hightlight_info, playbyplay):
        return self.extract_hightlight_inning_play_list(
            visitor_score_board,
            home_score_board,
            hightlight_info,
            playbyplay,
        )