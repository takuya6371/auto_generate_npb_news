# coding: UTF-8
import batch.batch_job as bj
import datetime

# 1日前
dt_yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
print(str(dt_yesterday.year).zfill(2))
print(str(dt_yesterday.month).zfill(2))
print(str(dt_yesterday.day).zfill(2))
bj.exe_process('date', str(dt_yesterday.year).zfill(2), str(
    dt_yesterday.month).zfill(2), str(dt_yesterday.day).zfill(2))
