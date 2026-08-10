"""
練習問題：メモを追加するフォームを作ろう

008_requestで作ったメモ一覧・詳細ページ・リダイレクトはそのまま使います。
以下の TODO コメントの箇所にコードを書いて完成させてください。
実行方法: python challenge/challenge.py
"""
import json
import os

from flask import Flask, redirect, render_template, request, url_for

from forms import MemoForm

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

MEMOS_PATH = os.path.join(os.path.dirname(__file__), 'memos.json')

with open(MEMOS_PATH, encoding='utf-8') as f:
    memos_list = json.load(f)

memos = {i + 1: memo for i, memo in enumerate(memos_list)}


@app.route('/')
def memo_list():
    category = request.args.get('category')

    memo_list_data = [{"id": memo_id, **memo} for memo_id, memo in memos.items()]

    if category:
        memo_list_data = [m for m in memo_list_data if m["category"] == category]

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


# ============================================================
# 問題：メモを追加するフォームを作る
# GET  /memos/new : new_memo.html を描画する（form を渡す）
# POST /memos/new : バリデーション成功時、以下を行ってからメモ一覧にリダイレクトする
#   1. 新しいメモデータ（title/category/body）を memos_list に追加する
#   2. memos（idをキーにした辞書）にも追加する
#   3. memos_list を memos.json に書き戻す（with open(..., 'w') + json.dump）
# バリデーション失敗時・GET時は new_memo.html を再描画する
# ============================================================
@app.route('/memos/new', methods=['GET', 'POST'])
def new_memo():
    form = MemoForm()

    # TODO: form.validate_on_submit() が True のときの処理を書く

    return render_template('new_memo.html', form=form)


@app.route('/old-memos')
def old_memos():
    return redirect(url_for('memo_list'))


if __name__ == '__main__':
    app.run(debug=True, port=5030)
