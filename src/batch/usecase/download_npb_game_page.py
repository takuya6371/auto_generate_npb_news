# coding: UTF-8
from bs4 import BeautifulSoup
import re
import os
import sys
from batch.util.file import file_read, create_folder, file_write
from batch.util.constant import url_head
from batch.infla.web.download_html import download_html
sys.path.append(os.path.abspath(".."))

# download page for scryping
class DownloadNpbGamePage:

    def __init__(self, year, month, date, data_path):
        self.year = year
        self.month = month
        self.date = date
        self.data_path = data_path
        self.month_folder_path = self.data_path + 'html/' + self.year + self.month
        self.date_folder_path = self.data_path + 'html/' + self.year + self.month + '/' + self.year + self.month + self.date

    def npb_game_schedule_page_download(self):
        create_folder(self.data_path + 'html/schedule/')
        # download schedule page
        target_url = url_head + 'games/' + self.year + '/schedule_' + self.month + '_detail.html'
        dl_html_path = self.data_path + 'html/schedule/' + self.year + self.month + '_schedule.html'
        if not os.path.exists(dl_html_path):
            try:
                html = download_html(target_url)
                file_write(dl_html_path, html.text)
            except:
                print("failed")
                return None
        return dl_html_path

    def get_links_in_schedule(self, schedule_html_path):
        # create filder for each month and date
        html = file_read(schedule_html_path)
        soup = BeautifulSoup(html, 'lxml')
        parsed_links = soup.find_all(
            "a", href=re.compile('/' + self.year + '/' + self.month + self.date))
        return parsed_links

    def npb_game_content_page_download (self, links):
        create_folder(self.month_folder_path)
        create_folder(self.date_folder_path)
        for link in links:
            url = link.get("href")
            game_card = url.split('/')[-2]
            for content_type in ['index', 'playbyplay', 'box']:
                path = self.date_folder_path + '/' + self.year + \
                    self.month + self.date + '_' + game_card + '_' + content_type + '.html'
                if not os.path.exists(path):
                    html = download_html(url_head + url + content_type + '.html')
                    file_write(path, html.text)

    def run (self):
        print("main start")
        schedule_html_path = self.npb_game_schedule_page_download()
        links = self.get_links_in_schedule(schedule_html_path)
        self.npb_game_content_page_download(links)

  
