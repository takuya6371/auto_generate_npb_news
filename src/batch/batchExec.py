# coding: UTF-8
import sys
import os
from typing import Literal
import calendar

from usecase.generateNewsData.generateNewsDataUseCase import GenerateNewsDataUseCase
sys.path.append(os.path.abspath(".."))
args = sys.argv

def startBatch(mode, year, month, date):
    print("job start input:" + str(args))

    # 指定した日の試合データを取得
    if mode == 'date':
        GenerateNewsDataUseCase(year, month, date).prosess()
    # 指定した月の試合データをまとめて取得
    elif mode == 'month':
        endDate = calendar.monthrange(int(year), int(month))[1]
        for i in range(1, endDate + 1):
            print(str(i).zfill(2))
            GenerateNewsDataUseCase(year, month, i.zfill(2)).prosess()

# バッチの実行メイン処理
if __name__ == '__main__':
    mode: Literal['date', 'month']
    mode = args[1]
    year = args[2]
    month = args[3]
    if len(args) > 4:
        date = args[4]
    else:
        date = "01"

    startBatch(mode, year, month, date)
