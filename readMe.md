# このツールは何をするか

    ・NPBの試合スコアを元に、試合の展開を解析してニュース文に変換する
    ・バッチでスクレイピングでデータ収集して、APIでニュース文を生成する
    ・現時点でDBは使用せずJSONにまとめているだけ

# 実行手順

- batch
  下記を実行
  python batchExec.py date 2023 07 05
- api
  下記を実行(テスト)
  python flaskServer.py
