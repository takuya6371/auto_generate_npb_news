import api.util.npb_const as nc


class GameHightlightInfo:
    score_pattern = [nc.START_SCORE, nc.WIN_SCORE, nc.REVERERSAL]

    def extract_game_hightlight_info(self, visitor_score_board, home_score_board):
        current_score = [0, 0]
        hightlight_info = {
            'highlight_inning': '',
            'highlight_scenario': '',
            'highlight_inning_begin_score': [],
            'highlight_inning_get_score': 0,
            'has_additional_points': False,
        }
        score_board = [visitor_score_board, home_score_board]
        current_inning_score = []
        inning_cnt = len(visitor_score_board) - 3
        for i in range(inning_cnt):
            other_score_index = 1
            for j in range(2):
                inning_begin_score = current_score.copy()
                current_score[j], current_inning_score = self.sum_current_score(current_score[j], score_board[j][str(i+1)])
                hightlight_info = self.compare_game_status(
                    j+1,
                    str(i+1),
                    hightlight_info,
                    current_score[j],
                    current_score[other_score_index],
                    current_inning_score,
                    inning_begin_score,
                )
                other_score_index -= 1
        return hightlight_info

    def compare_game_status(
        self,
        current_up_down,
        current_inning_num,
        highlight_info,
        current_score_target,
        current_score_other,
        current_get_score,
        inning_begin_score,
    ):

        if highlight_info['highlight_inning'] == '' and current_score_target > current_score_other:
            print("START_SCORE")
            highlight_info['highlight_inning'] = str(current_inning_num) + '-' + str(current_up_down)
            highlight_info['highlight_scenario'] = nc.START_SCORE
            highlight_info['highlight_inning_begin_score'] = inning_begin_score
            highlight_info['highlight_inning_get_score'] = current_get_score
            highlight_info['has_additional_points'] = False
        elif (not highlight_info['highlight_inning'] == ''
            and not highlight_info['highlight_scenario'] in self.score_pattern
            and current_score_target > current_score_other):
            print("win")
            print(current_inning_num)
            highlight_info['highlight_inning'] = str(current_inning_num) + '-' + str(current_up_down)
            highlight_info['highlight_scenario'] = nc.REVERERSAL
            highlight_info['highlight_inning_begin_score'] = inning_begin_score
            highlight_info['highlight_inning_get_score'] = current_get_score
            highlight_info['has_additional_points'] = False
        elif (not highlight_info['highlight_inning'] == ''
            and not int(highlight_info['highlight_inning'].split('-')[1]) == current_up_down
            and current_score_target > current_score_other):
            print("Reversal")

            highlight_info['highlight_inning'] = str(current_inning_num) + '-' + str(current_up_down)
            highlight_info['highlight_scenario'] = nc.REVERERSAL
            highlight_info['highlight_inning_begin_score'] = inning_begin_score
            highlight_info['highlight_inning_get_score'] = current_get_score
            highlight_info['has_additional_points'] = False
        elif (not highlight_info['highlight_scenario'] == nc.CATCH_UP
            and not highlight_info['highlight_inning'] == ''
            and not int(highlight_info['highlight_inning'].split('-')[1]) == current_up_down
            and current_score_target == current_score_other):
            print("catch up")
            print(inning_begin_score)
            highlight_info['highlight_inning'] = str(current_inning_num) + '-' + str(current_up_down)
            highlight_info['highlight_scenario'] = nc.CATCH_UP
            highlight_info['highlight_inning_begin_score'] = inning_begin_score
            highlight_info['highlight_inning_get_score'] = current_get_score
            highlight_info['has_additional_points'] = False
        # additional_points
        elif highlight_info['highlight_scenario'] in self.score_pattern and current_get_score > 0:
            highlight_info['has_additional_points'] = True

        return highlight_info


    def sum_current_score (self, current_score, score_board ):
        if score_board == '' or score_board == 'x':
            current_inning_score = 0
        else:
            current_inning_score = int(score_board)
        # plus score in current inning
        current_score += current_inning_score
        return current_score, current_inning_score


    def run (self, visitor_score_board, home_score_board):
        return self.extract_game_hightlight_info(
        visitor_score_board,
        home_score_board,
    )