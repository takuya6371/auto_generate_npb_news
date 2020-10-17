# coding: UTF-8
from flask import Flask, make_response, request
from flask_cors import CORS, cross_origin
import output_news as on
import datetime
import npb_const as nc
api = Flask(__name__)
CORS(api)
# target year
target_year = '2020'
# target month
target_month = '08'
# target date
target_date = '01'


@api.route('/')
def hello():
    name = "Hello World"
    return name


@api.route('/npb/news/<date>', methods=['POST'])
def npb(date=None):
    print(request.headers.get('Auth'))
    auth = request.headers.get('Auth')
    if not auth == nc.auth:
        return 'auth failed'

    if date is None:
        return_data = '日付を入れてください。'
    else:
        try:
            #newDataStr = "%04d/%02d/%02d" % (date)
            newDate = datetime.datetime.strptime(date, "%Y%m%d")
        except:
            return '日付が不正です。'
        name = "Good"
        return_data = on.main_process(date[0:4], date[4:6], date[6:8])
        print(return_data)
    return '¥n'.join(return_data)


# おまじない
if __name__ == "__main__":
    api.run(debug=True)
