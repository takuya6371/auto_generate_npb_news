# ニュース分の導入部を生成
class NewsSentenseHead:
    # 導入部の文を生成
    def __generateHeadSentence (self, home_team, visitor_team):
        return home_team + '対' + visitor_team + 'の試合は、'

    # 試合のスコア部の分を生成
    def __generateGameScoreSentence (self, game_status, home_score_board_total, visitor_score_board_total):
        if not game_status == '試合終了':
            return '中止となりました。'
        else:
            return home_score_board_total + '対' \
                + visitor_score_board_total
    # 勝ちチームを返却
    def __findWinTeam(self, visitor_team, visitor_score_board, home_team, home_score_board):
        visitor_score = visitor_score_board['total']
        home_score = home_score_board['total']

        if int(visitor_score) == int(home_score):
            return ''
        elif int(visitor_score) > int(home_score):
            return visitor_team
        else:
            return home_team

    # 試合の結果を生成
    def __generateGameResultSentence (self, winTeam):
        if winTeam == '':
             return 'で引き分けました。'
        else:
            return 'で' + winTeam + 'が勝ちました。'

    def process (self, gameDataDf):
        headSentence = self.__generateHeadSentence(
            gameDataDf['home_team'], gameDataDf['visitor_team']
        )
        gameScoreSentence = self.__generateGameScoreSentence(
            gameDataDf['game_status'],
            gameDataDf['home_score_board']['total'],
            gameDataDf['visitor_score_board']['total'],
        )
        winTeam = self.__findWinTeam(
            gameDataDf['visitor_team'],
            gameDataDf['visitor_score_board'],
            gameDataDf['home_team'],
            gameDataDf['home_score_board']
        )
        gameResultSentence = self.__generateGameResultSentence(winTeam)

        return headSentence + gameScoreSentence + gameResultSentence
