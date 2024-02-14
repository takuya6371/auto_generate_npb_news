# coding: UTF-8
import requests

# htmlファイルのダウンロード
def downloadHtml (url):
    print('dowmload:' + url)
    html = requests.get(url)
    html.encoding = html.apparent_encoding
    return html
