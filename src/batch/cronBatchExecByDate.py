# coding: UTF-8
import batch.batchExec as bj
import datetime

# cron登録用の事項ファイル
# 1日前の野球データを取得
dtYesterday = datetime.datetime.now() - datetime.timedelta(days=1)
print(str(dtYesterday.year).zfill(2))
print(str(dtYesterday.month).zfill(2))
print(str(dtYesterday.day).zfill(2))
bj.startBatch('date', str(dtYesterday.year).zfill(2), str(
    dtYesterday.month).zfill(2), str(dtYesterday.day).zfill(2))
