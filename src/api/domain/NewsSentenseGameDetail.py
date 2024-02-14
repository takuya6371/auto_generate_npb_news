import const as nc
# ニュース文の詳細部を生成
class NewsSentenseGameDetail:
    # 試合経過の詳細を生成
    def __generateDetailSentense(self, homeTeam, visitorTeam, hightlightInfo, hightlightInningPlayList):
        highlightInningNum = int(hightlightInfo['highlight_inning'].split("-")[0])
        highlightInningUpDown = int(hightlightInfo['highlight_inning'].split("-")[1])
        if highlightInningUpDown == 1:
            highlightTeam = visitorTeam
        else:
            highlightTeam = homeTeam

        if hightlightInfo['highlight_scenario'] == nc.START_SCORE:
            highlightPlayList = self.__generateHighlightInningPlaySentence(
                hightlightInningPlayList, hightlightInfo['highlight_inning'])
            return nc.TEAM_SHORT_NAME[highlightTeam] + 'は' \
                + str(highlightInningNum) + '回、' \
                + highlightPlayList \
                + 'で' + str(hightlightInfo['highlight_inning_get_score']) + '点を先制し'
            
        if hightlightInfo['highlight_scenario'] == nc.CATCH_UP:
            pickupIndex = [i for i, _ in enumerate(hightlightInningPlayList) if _[
                'current_score_diff'] == 0][0]
            return nc.TEAM_SHORT_NAME[highlightTeam] + 'は' \
                + str((max(hightlightInfo['highlight_inning_begin_score']) - min(hightlightInfo['highlight_inning_begin_score']))) \
                + '点を追う' + str(highlightInningNum) \
                + '回、' + hightlightInningPlayList[pickupIndex]['player'] \
                + 'の' + self.__transPlayName(hightlightInningPlayList[pickupIndex]['play'], hightlightInningPlayList[pickupIndex]['get_score']) \
                + 'で追いつきました。'
        elif hightlightInfo['highlight_scenario'] == nc.WIN_SCORE:
            highlightPlayList = self.__generateHighlightInningPlaySentence(
                hightlightInningPlayList, hightlightInfo['highlight_inning'])

            return nc.TEAM_SHORT_NAME[highlightTeam] + 'は' \
                + str(highlightInningNum) + '回、' \
                + highlightPlayList \
                + 'で' + str(hightlightInfo['highlight_inning_get_score']) + '点を勝ち越し'

        elif hightlightInfo['highlight_scenario'] == nc.REVERERSAL:
            highlightPlayList = self.__generateHighlightInningPlaySentence(
                hightlightInningPlayList, hightlightInfo['highlight_inning'])

            return nc.TEAM_SHORT_NAME[highlightTeam] + 'は' \
                + str((max(hightlightInfo['highlight_inning_begin_score']) - min(hightlightInfo['highlight_inning_begin_score']))) \
                + '点ビハインドで迎えた' + str(highlightInningNum) + '回、'\
                + highlightPlayList \
                + 'で逆転し'

    # 文の最後を生成
    def __generateEndSentense (self, hightlightInfo):
        if int(hightlightInfo['highlight_inning'].split('-')[0]) >= 9:
            return 'サヨナラ勝ちしました。'
        if hightlightInfo['has_additional_points']:
            end_sentense = 'その後も追加点を上げました。'
        else:
            end_sentense = 'ました。'
        return end_sentense

    # プレイ内容をニュース文用に変換
    def __transPlayName(self, play, get_score):
        if 'ホームラン' in play:
            playName = nc.PLAY_SHORT_NAME[play]
        else:
            if int(get_score) > 1:
                playName = str(get_score) + '点' + nc.PLAY_SHORT_NAME[play] if play in nc.PLAY_SHORT_NAME else play
            else:
                playName =  nc.PLAY_SHORT_NAME[play] if play in nc.PLAY_SHORT_NAME else play
        return playName


    # ハイライトのイニングのプレイを抽出
    def __generateHighlightInningPlaySentence(self, highlightPlayList, highlightInning):
        if int(highlightInning.split('-')[0]) >= 9 and int(highlightInning.split('-')[1]) == 2:
            pickupPlay = highlightPlayList[len(highlightPlayList)-1]['player'] + 'の' \
                + (self.__transPlayName(nc.PLAY_SHORT_NAME[highlightPlayList[len(highlightPlayList)-1]['play']], highlightPlayList[len(highlightPlayList)-1]['get_score']) if highlightPlayList[len(highlightPlayList)-1]['play'] in nc.PLAY_SHORT_NAME else self.__transPlayName(highlightPlayList[len(highlightPlayList)-1]['play'], highlightPlayList[len(highlightPlayList)-1]['get_score'])) \
                + 'で'
        else:
            if len(highlightPlayList) > 1:
                sortedHighlightPlayList = sorted(
                    highlightPlayList, key=lambda x: x['get_score'], reverse=True)
                pickupPlay = sortedHighlightPlayList[0]['player'] + 'の' \
                    + (nc.PLAY_SHORT_NAME[sortedHighlightPlayList[0]['play']] \
                    if sortedHighlightPlayList[0] ['play'] in nc.PLAY_SHORT_NAME else sortedHighlightPlayList[0]['play']) \
                    + '、' + sortedHighlightPlayList[1]['player'] + 'の' + (nc.PLAY_SHORT_NAME[sortedHighlightPlayList[1]['play']] \
                    if sortedHighlightPlayList[1]['play'] in nc.PLAY_SHORT_NAME else sortedHighlightPlayList[1]['play'])
                if len(highlightPlayList) > 2:
                    pickupPlayEnd = 'など'
                else:
                    pickupPlayEnd = ''
                pickupPlay += pickupPlayEnd
            else:
                pickupPlay = highlightPlayList[0]['player'] + 'の' \
                    + nc.PLAY_SHORT_NAME[highlightPlayList[0]['play']]\
                    if highlightPlayList[0]['play'] in nc.PLAY_SHORT_NAME \
                    else highlightPlayList[0]['play']

        return pickupPlay

    def process(self, homeTeam, visitorTeam, hightlightInfo, hightlightInningPlayList):
        detailSentense = self.__generateDetailSentense(homeTeam, visitorTeam, hightlightInfo, hightlightInningPlayList)
        endSentense = self.__generateEndSentense(hightlightInfo)
        return detailSentense + endSentense
