# coding: UTF-8
import sys
import os
from typing import Literal
import calendar
sys.path.append(os.path.abspath(".."))
#import download_html as dh
from batch.handler.news_file import GenerateNpbNewsData 
args = sys.argv
"""
パッケージ
import
分ける

ファイルをダウンロード
HTMLをJSONに変換
"""
# TODO Log 
def exec_process(mode, year, month, date):
    print("job start")
    print(args)

    if mode == 'date':
        GenerateNpbNewsDataClass = GenerateNpbNewsData(year, month, date)
        GenerateNpbNewsDataClass.main_process()
    elif mode == 'month':
        end_date = calendar.monthrange(int(year), int(month))[1]
        for i in range(1, end_date + 1):
            print(str(i).zfill(2))
            GenerateNpbNewsData(year, month, i.zfill(2))
            GenerateNpbNewsData.main_process()

if __name__ == '__main__':
    mode: Literal['date', 'month']
    mode = 'fff'
    mode = args[1]
    year = args[2]
    month = args[3]
    if len(args) > 4:
        date = args[4]
    else:
        date = "01"

    exec_process(mode, year, month, date)
