# coding: UTF-8
from bs4 import BeautifulSoup
import re
from batch.util.file import file_read

def extract_game_status (soup):
    return_data = {}
    # check game status
    game_status = soup.find(class_='game_info').text
    # extract game info
    game_all_info = soup.find(class_='game_tit')
    # game place
    return_data['game_place'] = game_all_info.find(class_='place').text
    # game date
    return_data['game_date'] = game_all_info.find('time').text
    # game card count
    game_discription = game_all_info.find('h3').text.split(' ')
    list_game_discription = filter(lambda a: a != '', game_discription)
    return_data['game_card_cnt'] = list(list_game_discription)[-1]
    if '中止' in game_status or 'ノーゲーム' in game_status:
        visitor_board = soup.find(class_='top')
        return_data['visitor_team'] = visitor_board.find('span').text
        home_board = soup.find(class_='bottom')
        return_data['home_team'] = home_board.find('span').text
        return_data['game_status'] = game_status
        return return_data
    elif not '試合終了' in game_status:
        return None
    return_data['game_status'] = '試合終了'
    return return_data

def extract_game_score (soup):
    return_data = {}
    score_board = {}
    score_board['visotor'] = soup.find(class_='top')
    score_board['home'] = soup.find(class_='bottom')
    for k, v in score_board.items(): 
        return_data[k + '_team'] = v.find('span').text
        score_td = v.find_all('td')
        max_ining = len(score_td) - 3
        score = {}
        for i in range(max_ining):
            score[i + 1] = score_td[i].text
        score['total'] = score_td[max_ining].text
        score['h'] = score_td[max_ining + 1].text
        score['e'] = score_td[max_ining + 2].text
        return_data[k + '_score_board'] = score
    return return_data

def extract_game_result (soup):
    return_data = {}
    game_result_info = soup.find(class_='game_result_info')
    tr_list = game_result_info.find_all('tr')
    for tr in tr_list:
        for k,v in {'win':'勝', 'lose':'負'}.items():
            if v in tr.find('th').text:
                tmp_text = re.split('[(（]', tr.text)
                pitcher = re.split('[¥】]', tmp_text[0])[1].replace('\n', '')
                pitcher_current_result = re.split('[])¥）]', tmp_text[1])[0]
                return_data[k + '_pitcher'] = pitcher
                return_data[k + '_pitcher_current_result'] = pitcher_current_result
    return return_data

def main (file):
    print("extract index start")
    html = file_read(file)
    soup = BeautifulSoup(html, 'lxml')
    status_data = extract_game_status(soup)
    if status_data is None or not status_data['game_status'] == '試合終了':
        return status_data
    score_data = extract_game_score(soup)
    result_data = extract_game_result(soup)
    return_data = dict(status_data, **score_data, **result_data)
    return return_data
