# coding: UTF-8
from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os
import datetime
sys.path.append(os.path.abspath("../../"))
import api.usecase.news as news
import api.usecase.latestNewsDate as latest
import api.util.npb_const as nc

api = Flask(__name__)
CORS(api)

@api.route('/')
def hello():
    name = "Hello World"
    return name


@api.route('/api/npb/news/<date>', methods=['GET'])
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
        return_data = news.main_process(date[0:4], date[4:6], date[6:8])
    return jsonify({'auto_news': '¥n'.join(return_data)})


@api.route('/api/npb/news/latestdate', methods=['GET'])
def latestdate():
    print(request.headers.get('Auth'))
    auth = request.headers.get('Auth')
    if not auth == nc.auth:
        return 'auth failed'
    return_data = latest.main()
    return jsonify({'latest_news_date': return_data})


# おまじない
if __name__ == "__main__":
    api.run()
