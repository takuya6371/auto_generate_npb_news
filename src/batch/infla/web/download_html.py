# coding: UTF-8
import requests

def download_html (url):
    print('dowmload:' + url)
    html = requests.get(url)
    html.encoding = html.apparent_encoding
    return html
