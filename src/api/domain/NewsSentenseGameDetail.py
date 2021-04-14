import api.util.npb_const as nc

class NewsSentenseGameDetail:
    def extract_sentense (self, home_team, visitor_team, hightlight_info, hightlight_inning_play_list):
        first_sentense = self.extract_detail_sentense(home_team, visitor_team, hightlight_info, hightlight_inning_play_list)
        second_sentense = self.extract_end_sentense(hightlight_info)
        print(first_sentense)
        return first_sentense + second_sentense

    def extract_detail_sentense(self, home_team, visitor_team, hightlight_info, hightlight_inning_play_list):
        highlight_inning_num = int(hightlight_info['highlight_inning'].split("-")[0])
        highlight_inning_up_down = int(hightlight_info['highlight_inning'].split("-")[1])
        if highlight_inning_up_down == 1:
            highlight_team = visitor_team
        else:
            highlight_team = home_team

        print(hightlight_info)
        print(hightlight_inning_play_list)
        if hightlight_info['highlight_scenario'] == nc.START_SCORE:
            highlight_play_list = self.make_highlight_inning_play_sentence(
                hightlight_inning_play_list, hightlight_info['highlight_inning'])
            return nc.TEAM_SHORT_NAME[highlight_team] + 'は' \
                + str(highlight_inning_num) + '回、' \
                + highlight_play_list \
                + 'で' + str(hightlight_info['highlight_inning_get_score']) + '点を先制し'
            
        if hightlight_info['highlight_scenario'] == nc.CATCH_UP:
            pickup_index = [i for i, _ in enumerate(hightlight_inning_play_list) if _[
                'current_score_diff'] == 0][0]
            return nc.TEAM_SHORT_NAME[highlight_team] + 'は' \
                + str((max(hightlight_info['highlight_inning_begin_score']) - min(hightlight_info['highlight_inning_begin_score']))) \
                + '点を追う' + str(highlight_inning_num) \
                + '回、' + hightlight_inning_play_list[pickup_index]['player'] \
                + 'の' + self.trans_play_name(hightlight_inning_play_list[pickup_index]['play'], hightlight_inning_play_list[pickup_index]['get_score']) \
                + 'で追いつきました。'
        elif hightlight_info['highlight_scenario'] == nc.WIN_SCORE:
            highlight_play_list = self.make_highlight_inning_play_sentence(
                hightlight_inning_play_list, hightlight_info['highlight_inning'])

            return nc.TEAM_SHORT_NAME[highlight_team] + 'は' \
                + str(highlight_inning_num) + '回、' \
                + highlight_play_list \
                + 'で' + str(hightlight_info['highlight_inning_get_score']) + '点を勝ち越し'

        elif hightlight_info['highlight_scenario'] == nc.REVERERSAL:
            highlight_play_list = self.make_highlight_inning_play_sentence(
                hightlight_inning_play_list, hightlight_info['highlight_inning'])

            return nc.TEAM_SHORT_NAME[highlight_team] + 'は' \
                + str((max(hightlight_info['highlight_inning_begin_score']) - min(hightlight_info['highlight_inning_begin_score']))) \
                + '点ビハインドで迎えた' + str(highlight_inning_num) + '回、'\
                + highlight_play_list \
                + 'で逆転し'

    def extract_end_sentense (self, hightlight_info):
        if int(hightlight_info['highlight_inning'].split('-')[0]) >= 9:
            return 'サヨナラ勝ちしました。'
        if hightlight_info['has_additional_points']:
            end_sentense = 'その後も追加点を上げました。'
        else:
            end_sentense = 'ました。'
        return end_sentense

    def trans_play_name(self, play, get_score):
        if 'ホームラン' in play:
            play_name = nc.PLAY_SHORT_NAME[play]
        else:
            if int(get_score) > 1:
                play_name = str(get_score) + '点' + nc.PLAY_SHORT_NAME[play] if play in nc.PLAY_SHORT_NAME else play
            else:
                play_name =  nc.PLAY_SHORT_NAME[play] if play in nc.PLAY_SHORT_NAME else play
        return play_name


    def make_highlight_inning_play_sentence(self, highlight_play_list, highlight_inning):
        if int(highlight_inning.split('-')[0]) >= 9 and int(highlight_inning.split('-')[1]) == 2:
            pickup_play = highlight_play_list[len(highlight_play_list)-1]['player'] + 'の' \
                + (self.trans_play_name(nc.PLAY_SHORT_NAME[highlight_play_list[len(highlight_play_list)-1]['play']], highlight_play_list[len(highlight_play_list)-1]['get_score']) if highlight_play_list[len(highlight_play_list)-1]['play'] in nc.PLAY_SHORT_NAME else self.trans_play_name(highlight_play_list[len(highlight_play_list)-1]['play'], highlight_play_list[len(highlight_play_list)-1]['get_score'])) \
                + 'で'
        else:
            if len(highlight_play_list) > 1:
                sorted_highlight_play_list = sorted(
                    highlight_play_list, key=lambda x: x['get_score'], reverse=True)
                print(sorted_highlight_play_list)
                pickup_play = sorted_highlight_play_list[0]['player'] + 'の' \
                    + (nc.PLAY_SHORT_NAME[sorted_highlight_play_list[0]['play']] \
                    if sorted_highlight_play_list[0] ['play'] in nc.PLAY_SHORT_NAME else sorted_highlight_play_list[0]['play']) \
                    + '、' + sorted_highlight_play_list[1]['player'] + 'の' + (nc.PLAY_SHORT_NAME[sorted_highlight_play_list[1]['play']] \
                    if sorted_highlight_play_list[1]['play'] in nc.PLAY_SHORT_NAME else sorted_highlight_play_list[1]['play'])
                print(pickup_play)
                if len(highlight_play_list) > 2:
                    pickup_play_end = 'など'
                else:
                    pickup_play_end = ''
                pickup_play += pickup_play_end
            else:
                pickup_play = highlight_play_list[0]['player'] + 'の' \
                    + nc.PLAY_SHORT_NAME[highlight_play_list[0]['play']]\
                    if highlight_play_list[0]['play'] in nc.PLAY_SHORT_NAME \
                    else highlight_play_list[0]['play']

        return pickup_play

    def run (self, home_team, visitor_team, hightlight_info, hightlight_inning_play_list):
        return self.extract_sentense(home_team, visitor_team, hightlight_info, hightlight_inning_play_list)