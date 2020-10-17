import datetime
import calendar
import sys
import download_html as dh
args = sys.argv
if __name__ == '__main__':
    print("job start")
    print(args)
    if len(args) > 1:
        mode = args[1]
        if mode == 'date':
            year = args[2]
            month = args[3]
            date = args[4]
            dh.file_download(year, month, date)
            index_data = dh.make_json(year, month, date)
        elif mode == 'month':
            year = args[2]
            month = args[3]
            print(month)
            end_date = calendar.monthrange(int(year), int(month))[1]
            for i in range(1, end_date + 1):
                print(str(i).zfill(2))
                dh.file_download(str(year), str(month), str(i).zfill(2))
                index_data = dh.make_json(
                    str(year), str(month), str(i).zfill(2))
    else:
        # target year
        target_year = 2020
        # target month
        target_month = 8
        # target date
        target_date = 8
