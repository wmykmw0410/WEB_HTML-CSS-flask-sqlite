"""
練習問題：書籍データの保存先を books.json から SQLite（books.db）に変更しよう

009_formsで作った書籍一覧・詳細・追加フォーム・リダイレクトの見た目や機能はそのままです。
データの持ち方だけを、Pythonの辞書（books.json読み込み）から
sqlite3モジュールで操作するデータベース（books.db）に置き換えます。

以下の TODO コメントの箇所にコードを書いて完成させてください。
実行方法: python challenge/challenge.py
"""
import json
import os
import sqlite3

from flask import Flask, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename

from forms import BookForm

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

DB_PATH = os.path.join(os.path.dirname(__file__), 'books.db')
SEED_JSON_PATH = os.path.join(os.path.dirname(__file__), 'books.json')
STATIC_IMG_DIR = os.path.join(os.path.dirname(__file__), 'static', 'img')


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id     INTEGER PRIMARY KEY AUTOINCREMENT,
            title  TEXT    NOT NULL,
            author TEXT    NOT NULL,
            price  INTEGER NOT NULL,
            image  TEXT    NOT NULL
        )
    """)

    count = conn.execute("SELECT COUNT(*) FROM books").fetchone()[0]
    if count == 0:
        # 初回起動時のみ books.json から初期データを投入する
        with open(SEED_JSON_PATH, encoding='utf-8') as f:
            books_data = json.load(f)

        with conn:
            conn.executemany(
                "INSERT INTO books (title, author, price, image) VALUES (:title, :author, :price, :image)",
                books_data,
            )

    conn.close()


init_db()


# ============================================================
# 問題1：書籍一覧を SELECT で取得する
# author が指定されていれば WHERE author = ? で絞り込み、
# 指定が無ければ全件取得すること
# ============================================================
@app.route('/')
def book_list():
    author = request.args.get('author')

    conn = get_db()
    # TODO: conn.execute(...).fetchall() で rows を取得する
    rows = []
    conn.close()

    book_list_data = [dict(row) for row in rows]

    return render_template('top.html', books=book_list_data)


# ============================================================
# 問題2：id を指定して書籍を1件 SELECT する
# 見つからない場合の表示（title/author_line/price_line/image）は
# これまでと同じ
# ============================================================
@app.route('/books/<int:book_id>')
def book_detail(book_id):
    conn = get_db()
    # TODO: conn.execute(...).fetchone() で row を取得する
    row = None
    conn.close()

    if row:
        title = row['title']
        author_line = f"著者: {row['author']}"
        price_line = f"¥{row['price']}"
        image = f"/static/img/{row['image']}"
    else:
        title = f'書籍ID {book_id} は見つかりません'
        author_line = ''
        price_line = ''
        image = '/static/img/not_found.png'

    return render_template(
        'detail.html',
        title=title,
        author_line=author_line,
        price_line=price_line,
        image=image,
    )


# ============================================================
# 問題3：新しい書籍を INSERT する
# with conn: を使って安全に書き込むこと（007_with・本章セクション8）
# ============================================================
@app.route('/books/new', methods=['GET', 'POST'])
def new_book():
    form = BookForm()

    if form.validate_on_submit():
        image_filename = 'not_found.png'
        if form.image.data and form.image.data.filename:
            image_filename = secure_filename(form.image.data.filename)
            os.makedirs(STATIC_IMG_DIR, exist_ok=True)
            form.image.data.save(os.path.join(STATIC_IMG_DIR, image_filename))

        conn = get_db()
        # TODO: with conn: の中で INSERT INTO books する
        conn.close()

        return redirect(url_for('book_list'))

    return render_template('new_book.html', form=form)


@app.route('/old-books')
def old_books():
    return redirect(url_for('book_list'))


if __name__ == '__main__':
    app.run(debug=True, port=5032)
