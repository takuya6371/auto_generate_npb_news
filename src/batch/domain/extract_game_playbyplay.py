# coding: UTF-8
from io import FileIO
from bs4 import BeautifulSoup
import re

from batch.util.file import file_read

def extract_playbyplay(soup):
    return_data = {}
    current_ining = ''
    play_cnt = 1

    # extract playbyplay
    playbyplay_all = soup.find(id='progress')
    print(playbyplay_all)
    for i, element in enumerate(playbyplay_all.find_all(['tr', re.compile("^h")])):
        if i == 0:
            continue
        if 'id' in element.attrs and 'com' in element['id']:
            current_ining = element['id']
            play_cnt = 1
            return_data[current_ining] = []
        else:
            td_list = []
            for td in element.find_all('td'):
                td_list.append(td.text)
            if '投手' in element.text:
                return_data[current_ining].append(
                    {'play-'+str(play_cnt): td_list, 'play_type': 'pitcher'})
                play_cnt += 1
            elif '盗塁' in element.text:
                return_data[current_ining].append(
                    {'play-'+str(play_cnt): td_list, 'play_type': 'runner'})
                play_cnt += 1
            else:
                return_data[current_ining].append(
                    {'play-'+str(play_cnt): td_list, 'play_type': 'batther'})
                play_cnt += 1

    return {'playbyplay': return_data}

def main (file):
    return_data = {}
    print("extract playbyplay start")
    html = file_read(file)
    # get html data
    soup = BeautifulSoup(html, 'lxml')
    game_status = soup.find(class_='game_info').text
    if not '試合終了' in game_status:
        return None
    return_data = extract_playbyplay(soup)
    return return_data
