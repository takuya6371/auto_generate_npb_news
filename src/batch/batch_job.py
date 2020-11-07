import datetime
import calendar
import sys
import download_html as dh
args = sys.argv


def exe_process(mode, year, month, date):
    print("job start")
    print(args)

    if mode == 'date':
        dh.file_download(year, month, date)
        index_data = dh.make_json(year, month, date)
    elif mode == 'month':
        end_date = calendar.monthrange(int(year), int(month))[1]
        for i in range(1, end_date + 1):
            print(str(i).zfill(2))
            dh.file_download(str(year), str(month), str(i).zfill(2))
            index_data = dh.make_json(
                str(year), str(month), str(i).zfill(2))


if __name__ == '__main__':
    mode = args[1]
    year = args[2]
    month = args[3]
    if len(args) > 3:
        date = args[4]

    exe_process(mode, year, month, date)
