"""
000_my_app — 自分だけの学習統合アプリ

各章(001〜)で学んだ内容を、動くアプリとして少しずつ育てていく。
「その章で何を学び、このアプリのどこに反映したか」を README.md のチェックリストで管理する。

実行:
    python app.py
"""
from flask import Flask

app = Flask(__name__)

# ここに 001_flask_basic のルーティングから追加していく


if __name__ == '__main__':
    app.run(debug=True)
