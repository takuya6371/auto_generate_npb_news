import batch_job as bj
import datetime


dt_now = datetime.datetime.now() - datetime.timedelta(days=1)
print(str(dt_now.year).zfill(2))
print(str(dt_now.month).zfill(2))
print(str(dt_now.day).zfill(2))
bj.exe_process('date', str(dt_now.year).zfill(2), str(
    dt_now.month).zfill(2), str(dt_now.day).zfill(2))
