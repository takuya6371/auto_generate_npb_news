import const as nc

# ハイライトのイニング情報を抽出
class GameHightlightIning:
    scorePattern = [nc.START_SCORE, nc.WIN_SCORE, nc.REVERERSAL]

    # スコアの移り変わりを見て、そのイニングの試合状況を算出する
    # そのイニングで逆転したのか、追いついたのか、先制したのか等
    def __compareGameStatus(
        self,
        currentUpDown,
        currentInningNum,
        highlightInfo,
        currentScoreTarget,
        currentScoreOther,
        currentGetScore,
        inningBeginScore,
    ):
        # 先制
        if highlightInfo['highlight_inning'] == '' and currentScoreTarget > currentScoreOther:
            highlightInfo['highlight_inning'] = str(currentInningNum) + '-' + str(currentUpDown)
            highlightInfo['highlight_scenario'] = nc.START_SCORE
            highlightInfo['highlight_inning_begin_score'] = inningBeginScore
            highlightInfo['highlight_inning_get_score'] = currentGetScore
            highlightInfo['has_additional_points'] = False

        # 逆転
        elif (not highlightInfo['highlight_inning'] == ''
            and (
                    not int(highlightInfo['highlight_inning'].split('-')[1]) == currentUpDown
                    and not highlightInfo['highlight_scenario'] in self.scorePattern
                 )
            and currentScoreTarget > currentScoreOther):

            highlightInfo['highlight_inning'] = str(currentInningNum) + '-' + str(currentUpDown)
            highlightInfo['highlight_scenario'] = nc.REVERERSAL
            highlightInfo['highlight_inning_begin_score'] = inningBeginScore
            highlightInfo['highlight_inning_get_score'] = currentGetScore
            highlightInfo['has_additional_points'] = False
        # 追いつき
        elif (not highlightInfo['highlight_scenario'] == nc.CATCH_UP
            and not highlightInfo['highlight_inning'] == ''
            and not int(highlightInfo['highlight_inning'].split('-')[1]) == currentUpDown
            and currentScoreTarget == currentScoreOther):
            highlightInfo['highlight_inning'] = str(currentInningNum) + '-' + str(currentUpDown)
            highlightInfo['highlight_scenario'] = nc.CATCH_UP
            highlightInfo['highlight_inning_begin_score'] = inningBeginScore
            highlightInfo['highlight_inning_get_score'] = currentGetScore
            highlightInfo['has_additional_points'] = False
        elif highlightInfo['highlight_scenario'] in self.scorePattern and currentGetScore > 0:
            highlightInfo['has_additional_points'] = True

        return highlightInfo

    # カウント時点でのスコアを計算
    def __sumCurrentScore(self, currentScore, scoreBoard ):
        # 最終回の攻撃省略時はx等はいる事があるので0に変換
        if scoreBoard == '' or scoreBoard == 'x':
            currentInningScore = 0
        else:
            currentInningScore = int(scoreBoard)
        # 見ているイニングのスコアを加算
        currentScore += currentInningScore
        return currentScore, currentInningScore


    def process(self, visitorScoreBoard, homeScoreBoard):
        currentScore = [0, 0]
        hightlightInfo = {
            'highlight_inning': '',
            'highlight_scenario': '',
            'highlight_inning_begin_score': [],
            'highlight_inning_get_score': 0,
            'has_additional_points': False,
        }
        scoreBoard = [visitorScoreBoard, homeScoreBoard]
        currentInningScore = []
        inningCnt = len(visitorScoreBoard) - 3
        for i in range(inningCnt):
            otherScoreIndex = 1
            for j in range(2):
                inningBeginScore = currentScore.copy()
                currentScore[j], currentInningScore = self.__sumCurrentScore(currentScore[j], scoreBoard[j][str(i+1)])
                hightlightInfo = self.__compareGameStatus(
                    j+1,
                    str(i+1),
                    hightlightInfo,
                    currentScore[j],
                    currentScore[otherScoreIndex],
                    currentInningScore,
                    inningBeginScore,
                )
                otherScoreIndex -= 1
        return hightlightInfo