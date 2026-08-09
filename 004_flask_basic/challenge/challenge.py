"""
練習問題：002_html_cssで作ったブックストアのトップページをFlaskで配信し、
書籍詳細ページをrender_templateで表示しよう

以下の TODO コメントの箇所にコードを書いて完成させてください。
実行方法: python challenge/challenge.py
"""
from flask import Flask, render_template

app = Flask(__name__)

books = {
    1: {"title": "吾輩は猫である", "author": "夏目漱石", "price": 770, "image": "wagahai_neko.png"},
    2: {"title": "坊っちゃん", "author": "夏目漱石", "price": 660, "image": "bocchan.png"},
    3: {"title": "羅生門", "author": "芥川龍之介", "price": 550, "image": "rashomon.png"},
    4: {"title": "銀河鉄道の夜", "author": "宮沢賢治", "price": 480, "image": "ginga_tetsudo.png"},
    5: {"title": "走れメロス", "author": "太宰治", "price": 440, "image": "hashire_merosu.png"},
}


# ============================================================
# 問題 1：書籍一覧ページ（002_html_cssの静的ページをFlaskで配信する）
# GET / で top.html を描画してください（変数は不要）
# ============================================================
# TODO: ルートを定義する


# ============================================================
# 問題 2：書籍詳細ページ（動的ルーティング + render_template）
# GET /books/<book_id> で detail.html を描画してください
# book_id は int として受け取り、books から該当する書籍を取得すること
#
# 該当する書籍がある場合：
#   title       に書籍タイトル
#   author_line に "著者: xxx"
#   price_line  に "¥xxx"
#   image       に "/static/img/xxx.png"
#   を渡す
#
# 該当する書籍が無い場合：
#   title       に "書籍ID {book_id} は見つかりません"
#   author_line, price_line に空文字
#   image       に "/static/img/not_found.png"
#   を渡す
#
# ※ 表示を分岐させる if 文は、テンプレート側ではなくこの Python 側で書くこと
#   （Jinja2の {% if %} はまだ学習していないため使わない）
# ============================================================
# TODO: ルートを定義する


if __name__ == '__main__':
    app.run(debug=True, port=5006)
