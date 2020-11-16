# coding: UTF-8
import os
auth = 'test'
SENSEI = 'sensei'
OITUKI = 'oituki'
GYAKUTEN = 'gyakuten'
KATIKOSI = 'katikosi'
OITUKIKATIKOSI = 'oitukikatikosi'
UP_DOWN = {
    '1': '表',
    '2': '裏',
}
TEAM_SHORT_NAME = {
    'オリックス・バファローズ': 'オリックス',
    '阪神タイガース': '阪神',
    '北海道日本ハムファイターズ': 'ファイターズ',
    '読売ジャイアンツ': '巨人',
    '東北楽天ゴールデンイーグルス': '楽天',
    '広島東洋カープ': '広島',
    '福岡ソフトバンクホークス': 'ソフトバンク',
    '横浜DeNAベイスターズ': 'DeNA',
    '千葉ロッテマリーンズ': 'ロッテ',
    '中日ドラゴンズ': '中日',
    '埼玉西武ライオンズ': '西武',
    '東京ヤクルトスワローズ': 'ヤクルト',
}
PLAY_SHORT_NAME = {
    'ショートゴロ': 'ショートゴロ',
    'フォアボール': '押し出し',
    'レフト前タイムリーヒット': 'レフト前タイムリーヒット',
    'レフト前タイムリーヒット': 'レフト前タイムリーヒット',
    'レフト前タイムリーヒット': 'レフト前タイムリーヒット',
    'センター前タイムリーヒット': 'センター前タイムリーヒット',
    'ライト前タイムリーヒット': 'ライト前タイムリーヒット',
    'レフト前タイムリーヒット（2打点）': 'レフト前２点タイムリーヒット',
    'センター前タイムリーヒット（2打点）': 'センター前２点タイムリーヒット',
    'ライト前タイムリーヒット（2打点）': 'ライト前２点タイムリーヒット',
    '右中間タイムリーツーベース': 'タイムリーツーベース',
    '右中間タイムリーツーベース': 'タイムリーツーベース',
    '左中間タイムリーツーベース': 'タイムリーツーベース',
    'センターオーバータイムリーツーベース': 'タイムリーツーベース',
    'センターオーバータイムリーツーベース': 'タイムリーツーベース',
    'ライトーオーバータイムリーツーベース': 'タイムリーツーベース',
    'レフトーオーバータイムリーツーベース': 'タイムリーツーベース',
    '右中間ソロホームラン': 'ソロホームラン',
    '左中間ソロホームラン': 'ソロホームラン',
    'レフトソロホームラン': 'ソロホームラン',
    'ライトソロホームラン': 'ソロホームラン',
    'センターソロホームラン': 'ソロホームラン',
    'レフト2ランホームラン': '2ランホームラン',
    'ライト2ランホームラン': '2ランホームラン',
    'センター2ランホームラン': '2ランホームラン',
    '右中間2ランホームラン': '2ランホームラン',
    '左中間2ランホームラン': '2ランホームラン',
    'レフト3ランホームラン': '3ランホームラン',
    'ライト3ランホームラン': '3ランホームラン',
    'センター3ランホームラン': '3ランホームラン',
    '3ランホームラン':'3ランホームラン',
    '右中間3ランホームラン': '3ランホームラン',
    '左中間3ランホームラン': '3ランホームラン',
    'レフト満塁ホームラン': '満塁ホームラン',
    'ライト満塁ホームラン': '満塁ホームラン',
    'センター満塁ホームラン': '満塁ホームラン',
    '右中間満塁ホームラン': '満塁ホームラン',
    '左中間満塁ホームラン': '満塁ホームラン',
}
# abs path
abs_path = os.path.dirname(os.path.abspath(__file__))
home_path = '/'.join(abs_path.split('/')[0:-2])
data_path = home_path + '/data/'

runner_cnt_list = {'': 0, '1塁': 1, '2塁': 1, '3塁': 1,
                   '1・2塁': 2, '2・3塁': 2, '1・3塁': 2, '満塁': 3}
game_synario = {
    '': '無効',
    '0': '引き分け',
    '1': '先制し、そのまま逃げ切り',
    '2': '先制し、追加点',
    '3': '勝ち越し、決勝点',
    '4': '勝ち越し、追加点',
    '5': '逆転',
    '6': '逆転し、その後も追加点',
    '7': '０対０で迎えた〜に先制し',
    '8': '',
    '9': '',
    '10': '',
    '11': '',
    '12': '',
    '13': '',
    '14': ''
}

play_name = {
    "": ""
}
'''
序盤
    先制点を上げ、そのまま逃げ切った　〜などで〜点を先制し、そのまま逃げ切りました
    先制点を上げ、その後も追加点を上げた　〜などで〜点を先制し、その後も追加点を上げました
    逆転し、そのまま逃げ切った　〜で逆転し、そのまま逃げ切りました
    逆転し、その後も追加点を上げた　〜で逆転し、その後も追加点を上げました

終盤
    〜が決勝点となりました　
    先制点を上げ、その後も追加点を上げた
    逆転しました
    逆転し、その後も追加点を上げた

引き分け
    追いついた
'''
