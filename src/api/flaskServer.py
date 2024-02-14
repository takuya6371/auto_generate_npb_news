# coding: UTF-8
from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os
import datetime
from usecase.generateNews import GenerateNews
import const as nc

api = Flask(__name__)
CORS(api)

@api.route('/')

@api.route('/api/npb/news/<date>', methods=['GET'])
def npb(date=None):
    if date is None:
        return_data = '日付を入れてください。'
    else:
        try:
            # 日付の形式チェック
            datetime.datetime.strptime(date, "%Y%m%d")
        except:
            return '日付が不正です。'
        return_data = GenerateNews().process(date[0:4], date[4:6], date[6:8])
    return jsonify({'auto_news': '¥n'.join(return_data)})

if __name__ == "__main__":
    api.run()
