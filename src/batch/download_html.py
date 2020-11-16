# coding: UTF-8
import requests
import urllib.request
from bs4 import BeautifulSoup
import re
import os
import glob
import json
import time

# abs path
abs_path = os.path.dirname(os.path.abspath(__file__))
home_path = '/'.join(abs_path.split('/')[0:-2])
data_path = home_path + '/data/'
# npb url header
url_head = 'https://npb.jp/'

# target year
target_year = '2020'
# target month
target_month = '08'
# target date
target_date = '03'

# download page for scryping


def file_download(year, month, date):

    if os.path.exists(data_path + 'html/schedule/'):
        result = 'schedule folder exist'
    else:
        os.mkdir(data_path + 'html/schedule/')
        result = 'schedule folder create:' + data_path + 'html/schedule/'
    # download schedule page
    target_url = url_head + 'games/' + year + '/schedule_' + month + '_detail.html'
    html_path = data_path + 'html/schedule/' + year + month + '_schedule.html'
    print('start schedule page reading')
    print(target_url)

    if os.path.exists(html_path):
        print(html_path + ' exist')
    else:
        print(year+month+' schedule page download')
        print(target_url)
        html = requests.get(target_url)
        # html.encoding = 'shift_jis'
        html.encoding = html.apparent_encoding
        with open(html_path, 'w') as file:
            file.write(html.text)
        # urllib.request.urlretrieve(target_url,"{0}".format(html_path), False)

    # create filder for each month
    month_folder_path = data_path + 'html/' + year + month
    if os.path.exists(month_folder_path):
        result = 'month folder exist'
    else:
        os.mkdir(month_folder_path)
        result = 'month folder create:' + month_folder_path

    # create filder for each date
    folder_path = data_path + 'html/' + year + month + '/' + year + month + date
    if os.path.exists(folder_path):
        result = 'folder exist'
    else:
        os.mkdir(folder_path)
        result = 'folder create:' + folder_path
    print(result)

    print('start file reading')
    print('')
    with open(html_path) as f:
        html = f.read()

    soup = BeautifulSoup(html, 'lxml')
    parsed_links = soup.find_all(
        "a", href=re.compile('/' + year + '/' + month + date))

    for parsed_link in parsed_links:
        print('')
        url = parsed_link.get("href")
        print(url)
        game_card = url.split('/')[-2]
        print(game_card)
        # index.html download
        index_path = folder_path + '/' + year + \
            month+date+'_' + game_card + '_index.html'
        if os.path.exists(index_path):
            print(index_path + ' exist')
        else:
            print('index download')
            print(url_head + url + '_index.html')
            html = requests.get(url_head + url)
            html.encoding = html.apparent_encoding
            with open(index_path, 'w') as file:
                file.write(html.text)
            # urllib.request.urlretrieve(url_head+url,"{0}".format(index_path))

        # playbyplay.html download
        playbyplay_path = folder_path + '/' + year+month + \
            date + '_' + game_card + '_playbyplay.html'
        if os.path.exists(playbyplay_path):
            print(playbyplay_path+' exist')
        else:
            print('playbyplay download')
            html = requests.get(url_head + url + 'playbyplay.html')
            html.encoding = html.apparent_encoding

            with open(playbyplay_path, 'w') as file:
                file.write(html.text)
            # urllib.request.urlretrieve(url_head+url+'playbyplay.html',"{0}".format(playbyplay_path))

        box_path = folder_path + '/' + year + month + \
            date + '_' + game_card + '_box.html'
        if os.path.exists(box_path):
            print(box_path+' exist')
        else:
            print('box download')
            print(url_head + url + 'box.html')
            html = requests.get(url_head + url + 'box.html')
            html.encoding = html.apparent_encoding
            with open(box_path, 'w') as file:
                file.write(html.text)
            # urllib.request.urlretrieve(url_head+url+'box.html',"{0}".format(box_path))

# making json from html files


def make_json(year, month, date):
    data = None
    files = sorted(glob.glob(data_path + 'html/' +
                             year + month + '/' + year + month + date + '/*'))
    json_path = data_path + 'json/' + year + month + '/' + year + month + date

    # check month folder exist
    if os.path.exists(data_path + 'json/' + year + month):
        result = 'json month folder exist'
    else:
        os.mkdir(data_path + 'json/' + year + month)
        result = 'json month folder create:' + data_path + 'json/' + year + month

    # check date folder exist
    if os.path.exists(json_path):
        result = 'json folder exist'
    else:
        os.mkdir(json_path)
        result = 'json folder create:' + json_path

    if len(glob.glob(json_path + '*')) > 0:
        print("exist")
        for p in glob.glob(json_path + '*', recursive=True):
            if os.path.isfile(p):
                os.remove(p)
    time.sleep(1)
    if len(files) == 0:
        print('no html file' + year, month, date)
        return False
    for file in files:
        print('')
        print('**************')
        print(file)
        json_file = json_path + '/' + \
            file.split('/')[-1].split('.')[0].rsplit('_', 1)[0]+'.json'
        if 'index' in file:
            print('index')
            index_data = extract_index(file)

            '''
            if os.path.exists(json_file):
                with open(json_file) as f:
                    data = json.load(f)
                    if not data is None:
                        data.update(index_data)
                    else:
                        data = index_data
            else:
            '''
            if not data is None and index_data['game_status'] == '試合終了':
                data.update(index_data)
            else:
                data = index_data
            print(index_data)

            with open(json_file, 'a') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

        if 'playbyplay' in file:
            print('playbyplay')


            playbyplay_data = extract_playbyplay(file)

            '''
            if os.path.exists(json_file):
                with open(json_file) as f:
                    data = json.load(f)
                    if not data is None:
                        data.update(playbyplay_data)
                    else:
                        data = playbyplay_data
            else:
            '''
            # data = playbyplay_data
            print(playbyplay_data)
            print(data)
            if not playbyplay_data is None:
                if not data is None and data['game_status'] == '試合終了':
                    data.update(playbyplay_data)
                else:
                    data = playbyplay_data
                playbyplay_data = ''
            with open(json_file, 'w') as f:
                #json.dump(',', f)
                json.dump(data, f, ensure_ascii=False, indent=4)

# read playbyplay and extract playbyplay data


def extract_playbyplay(file):
    return_data = {}
    current_ining = ''
    # batter_cnt = 1
    play_cnt = 1
    # pitcher_cnt = 1
    playbyplay_json = {}
    with open(file) as f:
        html = f.read()
    # get html data
    soup = BeautifulSoup(html, 'lxml')
    # check game status
    game_status = soup.find(class_='game_info').text
    if not '試合終了' in game_status:
        return None

    # extract playbyplay
    playbyplay_all = soup.find(id='progress')
    # print(len(playbyplay_all))
    for i, element in enumerate(playbyplay_all.find_all(['tr', re.compile("^h")])):
        # print(element)
        # print()
        if i == 0:
            continue
        if 'id' in element.attrs and 'com' in element['id']:
            # print(element['id'])
            current_ining = element['id']
            play_cnt = 1
            playbyplay_json[current_ining] = []
        else:
            td_list = []
            for td in element.find_all('td'):
                td_list.append(td.text)
            if '投手' in element.text:
                playbyplay_json[current_ining].append(
                    {'play-'+str(play_cnt): td_list, 'play_type': 'pitcher'})
                play_cnt += 1
            elif '盗塁' in element.text:
                playbyplay_json[current_ining].append(
                    {'play-'+str(play_cnt): td_list, 'play_type': 'runner'})
                play_cnt += 1
            else:
                playbyplay_json[current_ining].append(
                    {'play-'+str(play_cnt): td_list, 'play_type': 'batther'})
                play_cnt += 1

    return {'playbyplay': playbyplay_json}

# read index and extract needed data


def extract_index(file):
    return_data = {}
    with open(file) as f:
        html = f.read()
    # get html data
    soup = BeautifulSoup(html, 'lxml')
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

    if '中止' in game_status:
        visitor_board = soup.find(class_='top')
        return_data['visitor_team'] = visitor_board.find('span').text
        home_board = soup.find(class_='bottom')
        return_data['home_team'] = home_board.find('span').text
        return_data['game_status'] = '試合中止'
        return return_data
    if 'ノーゲーム' in game_status:
        visitor_board = soup.find(class_='top')
        return_data['visitor_team'] = visitor_board.find('span').text
        home_board = soup.find(class_='bottom')
        return_data['home_team'] = home_board.find('span').text
        return_data['game_status'] = 'ノーゲーム'
        return return_data
    elif not '試合終了' in game_status:
        return None
    return_data['game_status'] = '試合終了'
    # visitor team
    visitor_board = soup.find(class_='top')
    return_data['visitor_team'] = visitor_board.find('span').text
    visitor_td = visitor_board.find_all('td')
    max_ining = len(visitor_td) - 3
    # print(max_ining)
    visitor_score = {}
    for i in range(max_ining):
        visitor_score[i + 1] = visitor_td[i].text
    visitor_score['total'] = visitor_td[max_ining].text
    visitor_score['h'] = visitor_td[max_ining + 1].text
    visitor_score['e'] = visitor_td[max_ining + 2].text
    return_data['visitor_score_board'] = visitor_score

    # home team
    home_board = soup.find(class_='bottom')
    return_data['home_team'] = home_board.find('span').text
    home_td = home_board.find_all('td')
    max_ining = len(home_td) - 3
    # print(max_ining)
    home_score = {}
    for i in range(max_ining):
        home_score[i + 1] = home_td[i].text
    home_score['total'] = home_td[max_ining].text
    home_score['h'] = home_td[max_ining + 1].text
    home_score['e'] = home_td[max_ining + 2].text
    return_data['home_score_board'] = home_score

    game_result_info = soup.find(class_='game_result_info')
    tr_list = game_result_info.find_all('tr')
    for tr in tr_list:
        # extract win pitcher
        if '勝' in tr.find('th').text:
            # print(tr.text)
            tmp_text = re.split('[(（]', tr.text)
            # print(tmp_text)
            win_pitcher = re.split('[¥】]', tmp_text[0])[1].replace('\n', '')
            win_pitcher_current_result = re.split('[])¥）]', tmp_text[1])[0]
            # print(win_pitcher)
            # print(win_pitcher_current_result)
            return_data['win_pitcher'] = win_pitcher
            return_data['win_pitcher_current_result'] = win_pitcher_current_result

        # extract win pitcher
        if '敗' in tr.find('th').text:
            # print(tr.text)
            tmp_text = re.split('[(（]', tr.text)
            # print(tmp_text)
            lose_pitcher = re.split('[¥】]', tmp_text[0])[1].replace('\n', '')
            lose_pitcher_current_result = re.split('[])¥）]', tmp_text[1])[0]
            # print(lose_pitcher)
            # print(lose_pitcher_current_result)
            return_data['lose_pitcher'] = lose_pitcher
            return_data['lose_pitcher_current_result'] = lose_pitcher_current_result
    # print(return_data)
    return return_data


if __name__ == '__main__':
    print("main start")
    file_download(target_year, target_month, target_date)
    index_data = make_json(target_year, target_month, target_date)
'''
soup = BeautifulSoup(r.text, 'lxml') #要素を抽出
print(soup)
topics = soup.find('ul',attrs={'class': 'topicsList_main'})
'''
