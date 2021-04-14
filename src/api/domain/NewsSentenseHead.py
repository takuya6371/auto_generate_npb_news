class NewsSentenseHead:   
    def __init__(self, game_data_df):
        self.game_data_df = game_data_df

    def generate_first_sentence (self, home_team, visitor_team):
        return home_team + '対' + visitor_team + 'の試合は、'

    def generate_second_sentence (self, game_status, home_score_board_total, visitor_score_board_total):
        if not game_status == '試合終了':
            return '中止となりました。'
        else:
            return home_score_board_total + '対' \
                + visitor_score_board_total
    
    def define_win_team(self, visitor_team, visitor_score_board, home_team, home_score_board):
        visitor_score = visitor_score_board['total']
        home_score = home_score_board['total']

        if int(visitor_score) == int(home_score):
            return ''
        elif int(visitor_score) > int(home_score):
            return visitor_team
        else:
            return home_team

    def generate_third_sentence (self, win_team):
        if win_team == '':
             return 'で引き分けました。'
        else:
            return 'で' + win_team + 'が勝ちました。'

    def run (self):
        first_sentence_vs = self.generate_first_sentence(self.game_data_df['home_team'], self.game_data_df['visitor_team'])
        second_sentence_team = self.generate_second_sentence(
            self.game_data_df['game_status'],
            self.game_data_df['home_score_board']['total'],
            self.game_data_df['visitor_score_board']['total'],
        )
        win_team = self.define_win_team(
            self.game_data_df['visitor_team'],
            self.game_data_df['visitor_score_board'],
            self.game_data_df['home_team'],
            self.game_data_df['home_score_board']
        )
        third_sentence_win_team = self.generate_third_sentence(win_team)

        return first_sentence_vs + second_sentence_team + third_sentence_win_team
