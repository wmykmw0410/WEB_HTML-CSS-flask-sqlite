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


@app.route('/')
def memo_list():
    category = request.args.get('category')

    conn = get_db()
    if category:
        rows = conn.execute("SELECT * FROM memos WHERE category = ?", (category,)).fetchall()
    else:
        rows = conn.execute("SELECT * FROM memos").fetchall()
    conn.close()

    memo_list_data = [dict(row) for row in rows]

    return render_template('top.html', memos=memo_list_data)


@app.route('/memos/<int:memo_id>')
def memo_detail(memo_id):
    conn = get_db()
    row = conn.execute("SELECT * FROM memos WHERE id = ?", (memo_id,)).fetchone()
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


@app.route('/memos/new', methods=['GET', 'POST'])
def new_memo():
    form = MemoForm()

    if form.validate_on_submit():
        conn = get_db()
        with conn:
            conn.execute(
                "INSERT INTO memos (title, category, body) VALUES (?, ?, ?)",
                (form.title.data, form.category.data, form.body.data),
            )
        conn.close()

        return redirect(url_for('memo_list'))

    return render_template('new_memo.html', form=form)


@app.route('/old-memos')
def old_memos():
    return redirect(url_for('memo_list'))


if __name__ == '__main__':
    app.run(debug=True, port=5033)
