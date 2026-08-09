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


@app.route('/')
def book_list():
    author = request.args.get('author')

    conn = get_db()
    if author:
        rows = conn.execute("SELECT * FROM books WHERE author = ?", (author,)).fetchall()
    else:
        rows = conn.execute("SELECT * FROM books").fetchall()
    conn.close()

    book_list_data = [dict(row) for row in rows]

    return render_template('top.html', books=book_list_data)


@app.route('/books/<int:book_id>')
def book_detail(book_id):
    conn = get_db()
    row = conn.execute("SELECT * FROM books WHERE id = ?", (book_id,)).fetchone()
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
        with conn:
            conn.execute(
                "INSERT INTO books (title, author, price, image) VALUES (?, ?, ?, ?)",
                (form.title.data, form.author.data, form.price.data, image_filename),
            )
        conn.close()

        return redirect(url_for('book_list'))

    return render_template('new_book.html', form=form)


@app.route('/old-books')
def old_books():
    return redirect(url_for('book_list'))


if __name__ == '__main__':
    app.run(debug=True, port=5033)
