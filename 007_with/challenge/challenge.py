"""
練習問題：メモデータをmemos.jsonから読み込むようにしよう

006_jinja2で作ったメモ一覧・詳細ページ・リダイレクトはそのまま使います。
これまでハードコードしていた memos 辞書を、with open() + os.path + json.load()
を使って memos.json から読み込むように変更します。

以下の TODO コメントの箇所にコードを書いて完成させてください。
実行方法: python challenge/challenge.py
"""
from flask import Flask, redirect, render_template, url_for

app = Flask(__name__)

# ============================================================
# 問題：memos.json を読み込んで memos 辞書を作る
#
# 1. os.path.join(os.path.dirname(__file__), 'memos.json') でパスを組み立てる
# 2. with open(パス, encoding='utf-8') as f: で開く
# 3. json.load(f) でリストとして読み込む（[{"title": ..., "category": ...}, ...]）
# 4. {i + 1: memo for i, memo in enumerate(リスト)} で
#    これまでと同じ「idをキーにした辞書」に変換する
# ============================================================
# TODO: 上のヒントに沿って memos を作る（下の1行を置き換える）
memos = {}


@app.route('/')
def memo_list():
    memo_list_data = [{"id": memo_id, **memo} for memo_id, memo in memos.items()]
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
    app.run(debug=True, port=5016)
