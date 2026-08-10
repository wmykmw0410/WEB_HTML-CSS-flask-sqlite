"""
練習問題：メモ一覧ページに、カテゴリで絞り込むクエリパラメータを追加しよう

007_withで作ったメモ一覧・詳細ページ・リダイレクトはそのまま使います。
以下の TODO コメントの箇所にコードを書いて完成させてください。
実行方法: python challenge/challenge.py
"""
import json
import os

from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

MEMOS_PATH = os.path.join(os.path.dirname(__file__), 'memos.json')

with open(MEMOS_PATH, encoding='utf-8') as f:
    memos_list = json.load(f)

memos = {i + 1: memo for i, memo in enumerate(memos_list)}


# ============================================================
# 問題：カテゴリで絞り込むクエリパラメータを追加する
# GET / で、クエリパラメータ category が指定されていれば
# そのカテゴリのメモだけに絞り込んで top.html を描画してください
# （例: /?category=仕事 で仕事カテゴリのメモだけ表示）
# 指定が無ければ全件を表示すること
# ============================================================
@app.route('/')
def memo_list():
    category = request.args.get('category')

    memo_list_data = [{"id": memo_id, **memo} for memo_id, memo in memos.items()]

    # TODO: category が指定されていたら、memo_list_data をカテゴリで絞り込む

    return render_template('top.html', memos=memo_list_data)


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


@app.route('/old-memos')
def old_memos():
    return redirect(url_for('memo_list'))


if __name__ == '__main__':
    app.run(debug=True, port=5021)
