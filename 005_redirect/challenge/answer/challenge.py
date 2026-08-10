"""
練習問題：メモ一覧・詳細ページに「旧URL」からのリダイレクトを追加しよう

004_flask_basicで作ったメモ一覧・詳細ページはそのまま使います。
以下の TODO コメントの箇所にコードを書いて完成させてください。
実行方法: python challenge/challenge.py
"""
from flask import Flask, redirect, render_template, url_for

app = Flask(__name__)

memos = {
    1: {"title": "買い物リスト", "category": "家事", "body": "牛乳、卵、パン、洗剤を買う。特売は火曜日まで。"},
    2: {"title": "企画会議メモ", "category": "仕事", "body": "来週の企画会議の議題を整理する。新商品の販促案について。"},
    3: {"title": "読書メモ：銀河鉄道の夜", "category": "趣味", "body": "宮沢賢治の作品。銀河や星座の描写が美しい。"},
    4: {"title": "アプリのアイデア", "category": "アイデア", "body": "習慣トラッカーアプリを作る。毎日の記録をグラフで見せる。"},
    5: {"title": "旅行の持ち物リスト", "category": "プライベート", "body": "パスポート、充電器、常備薬を忘れずに。"},
}


@app.route('/')
def memo_list():
    return render_template('top.html')


@app.route('/memos/<int:memo_id>')
def memo_detail(memo_id):
    memo = memos.get(memo_id)

    if memo:
        title = memo['title']
        category = memo['category']
        body = memo['body']
    else:
        title = f'メモID {memo_id} は見つかりません'
        category = ''
        body = ''

    return render_template(
        'detail.html',
        title=title,
        category=category,
        body=body,
    )


# ============================================================
# 問題：旧URLからのリダイレクト
# GET /old-memos にアクセスされたら、メモ一覧ページ（/）へリダイレクトしてください
# redirect() と url_for() を使うこと
# ============================================================
@app.route('/old-memos')
def old_memos():
    return redirect(url_for('memo_list'))


if __name__ == '__main__':
    app.run(debug=True, port=5010)
