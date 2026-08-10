"""
練習問題：メモデータの保存先を memos.json から SQLite（memos.db）に変更しよう

009_formsで作ったメモ一覧・詳細・追加フォーム・リダイレクトの見た目や機能はそのままです。
データの持ち方だけを、Pythonの辞書（memos.json読み込み）から
sqlite3モジュールで操作するデータベース（memos.db）に置き換えます。

以下の TODO コメントの箇所にコードを書いて完成させてください。
実行方法: python challenge/challenge.py
"""
import json
import os
import sqlite3

from flask import Flask, redirect, render_template, request, url_for

from forms import MemoForm

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

DB_PATH = os.path.join(os.path.dirname(__file__), 'memos.db')
SEED_JSON_PATH = os.path.join(os.path.dirname(__file__), 'memos.json')


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS memos (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            title    TEXT    NOT NULL,
            category TEXT    NOT NULL,
            body     TEXT    NOT NULL
        )
    """)

    count = conn.execute("SELECT COUNT(*) FROM memos").fetchone()[0]
    if count == 0:
        # 初回起動時のみ memos.json から初期データを投入する
        with open(SEED_JSON_PATH, encoding='utf-8') as f:
            memos_data = json.load(f)

        with conn:
            conn.executemany(
                "INSERT INTO memos (title, category, body) VALUES (:title, :category, :body)",
                memos_data,
            )

    conn.close()


init_db()


# ============================================================
# 問題1：メモ一覧を SELECT で取得する
# category が指定されていれば WHERE category = ? で絞り込み、
# 指定が無ければ全件取得すること
# ============================================================
@app.route('/')
def memo_list():
    category = request.args.get('category')

    conn = get_db()
    # TODO: conn.execute(...).fetchall() で rows を取得する
    rows = []
    conn.close()

    memo_list_data = [dict(row) for row in rows]

    return render_template('top.html', memos=memo_list_data)


# ============================================================
# 問題2：id を指定してメモを1件 SELECT する
# 見つからない場合の表示（title/category/body）はこれまでと同じ
# ============================================================
@app.route('/memos/<int:memo_id>')
def memo_detail(memo_id):
    conn = get_db()
    # TODO: conn.execute(...).fetchone() で row を取得する
    row = None
    conn.close()

    if row:
        title = row['title']
        category = row['category']
        body = row['body']
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
# 問題3：新しいメモを INSERT する
# with conn: を使って安全に書き込むこと（007_with・本章セクション8）
# ============================================================
@app.route('/memos/new', methods=['GET', 'POST'])
def new_memo():
    form = MemoForm()

    if form.validate_on_submit():
        conn = get_db()
        # TODO: with conn: の中で INSERT INTO memos する
        conn.close()

        return redirect(url_for('memo_list'))

    return render_template('new_memo.html', form=form)


@app.route('/old-memos')
def old_memos():
    return redirect(url_for('memo_list'))


if __name__ == '__main__':
    app.run(debug=True, port=5032)
