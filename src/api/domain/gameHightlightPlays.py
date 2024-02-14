import const as nc

class GameHightlightPlays:

    # イニング開始時のスコア差を返却
    def __getCurrentScoreDiff(self, highlightInningBeginScores):
        if highlightInningBeginScores[0] == highlightInningBeginScores[1]:
            return 0
        return min(highlightInningBeginScores) - \
            max(highlightInningBeginScores)

    # イニングの得点に絡んだプレイ一覧を抽出
    def __extractHightlightInningScorePlayList(
        self, 
        highlightInningNum,
        highlightInningUpDown,
        currentScoreDiff,
        playbyplay,
    ):
        # 初期の各値を設定
        scorePlayList = []
        cntScore = 0
        beforeRunner = -1
        beforeOut = 0
        beforeType = ''
        beforePlay = ''
        beforePlayer = ''
        beforeGetScore = 0

        for i, play in enumerate(playbyplay['com' + highlightInningNum + '-' + highlightInningUpDown]):
            if not play['play_type'] == 'pitcher':
                outCnt = int(play['play-'+str(i + 1)][0].split('アウト')[0])
                runnerCnt = int(
                    nc.runner_cnt_list[play['play-'+str(i + 1)][1].strip()])
                # プレイした選手
                player = play['play-'+str(i + 1)][2]
                # プレイ内容（ヒット打ったとか、四球とか）
                byPlay = play['play-'+str(i + 1)][4]

                if beforeGetScore == 0:
                    # ランナーの前後とアウトカウントで得点を推測
                    if beforeType == 'runner':
                        runnerCntUp = 0
                    else:
                        runnerCntUp = 1
                    getScore = beforeRunner - runnerCnt + \
                        runnerCntUp - (outCnt - beforeOut)
                    cntScore += getScore
                    currentScoreDiff += getScore
                    if getScore > 0:
                        scorePlayList.append({'play': beforePlay, 'get_score': getScore,
                                                'current_score_diff': currentScoreDiff, 'player': beforePlayer})

                if '打点' in byPlay:
                    currentGetScore = int(byPlay.split('打点')[1][:-1])
                    cntScore += currentGetScore
                    currentScoreDiff += currentGetScore
                    scorePlayList.append({'play': byPlay.split('（')[0], 'get_score': currentGetScore,
                                            'current_score_diff': currentScoreDiff, 'player': beforePlayer})
                else:
                    currentGetScore = 0
 
                beforeOut = outCnt
                beforeRunner = runnerCnt
                beforePlay = byPlay.split('（')[0]
                beforePlayer = player
                beforeType = play['play_type']
                beforeGetScore = currentGetScore

        if getScore > 0:
            scorePlayList.append({'play': beforePlay, 'get_score': getScore,
                                    'current_score_diff': currentScoreDiff, 'player': beforePlayer})

        return scorePlayList

    def process(self, hightlightInfo, playbyplay):
        highlightInningNum = hightlightInfo['highlight_inning'].split("-")[0]
        # 表裏を取得
        highlightInningUpDown = hightlightInfo['highlight_inning'].split("-")[1]
        currentScoreDiff = self.__getCurrentScoreDiff(hightlightInfo['highlight_inning_begin_score'])

        return self.__extractHightlightInningScorePlayList(
            highlightInningNum,
            highlightInningUpDown,
            currentScoreDiff,
            playbyplay,
        )