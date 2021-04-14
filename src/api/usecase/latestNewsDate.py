import datetime
import util.file as file
import api.util.npb_const as nc

def main ():
    print("dddd")
    print(file.list_file(nc.data_path + 'json/'))
    year_month_list = file.list_file(nc.data_path + 'json/')
    print(year_month_list[len(year_month_list)-1])
    for i in range(1, len(year_month_list) + 1):
        print('aaa')
        print(year_month_list[len(year_month_list)-i])
        date_list = file.list_file(year_month_list[len(year_month_list)-i] + '/')
        print(date_list)
        for j in range(1, len(date_list) + 1):
            print(date_list[len(date_list)-j])
            json_list = file.list_file(date_list[len(date_list)-j] + '/')
            print(json_list)
            for k in range(1, len(json_list) + 1):
                print(json_list[len(json_list)-k])
                json = file.json_file_read(json_list[len(json_list)-k])
                if json['game_status'] and json['game_status'] == '試合終了':
                    game_date_YMD = date_list[len(date_list)-j].split('/')[-1]
                    return game_date_YMD[0:4] + '/' + game_date_YMD[4:6] + '/' + game_date_YMD[6:8]
  
# おまじない
if __name__ == "__main__":
    main()
