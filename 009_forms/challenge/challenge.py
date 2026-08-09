"""
練習問題：書籍を追加するフォームを作ろう

008_requestで作った書籍一覧・詳細ページ・リダイレクトはそのまま使います。
以下の TODO コメントの箇所にコードを書いて完成させてください。
実行方法: python challenge/challenge.py
"""
import json
import os

from flask import Flask, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename

from forms import BookForm

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

BOOKS_PATH = os.path.join(os.path.dirname(__file__), 'books.json')
STATIC_IMG_DIR = os.path.join(os.path.dirname(__file__), 'static', 'img')

with open(BOOKS_PATH, encoding='utf-8') as f:
    books_list = json.load(f)

books = {i + 1: book for i, book in enumerate(books_list)}


@app.route('/')
def book_list():
    author = request.args.get('author')

    book_list_data = [{"id": book_id, **book} for book_id, book in books.items()]

    if author:
        book_list_data = [b for b in book_list_data if b["author"] == author]

    return render_template('top.html', books=book_list_data)


@app.route('/books/<int:book_id>')
def book_detail(book_id):
    book = books.get(book_id)

    if book:
        title = book['title']
        author_line = f"著者: {book['author']}"
        price_line = f"¥{book['price']}"
        image = f"/static/img/{book['image']}"
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
# 問題：書籍を追加するフォームを作る
# GET  /books/new : new_book.html を描画する（form を渡す）
# POST /books/new : バリデーション成功時、以下を行ってから書籍一覧にリダイレクトする
#   1. アップロードされた画像があれば secure_filename() で安全なファイル名にし、
#      static/img/ に保存する（無ければ 'not_found.png' を使う）
#   2. 新しい書籍データ（title/author/price/image）を books_list に追加する
#   3. books（idをキーにした辞書）にも追加する
#   4. books_list を books.json に書き戻す（with open(..., 'w') + json.dump）
# バリデーション失敗時・GET時は new_book.html を再描画する
# ============================================================
@app.route('/books/new', methods=['GET', 'POST'])
def new_book():
    form = BookForm()

    # TODO: form.validate_on_submit() が True のときの処理を書く

    return render_template('new_book.html', form=form)


@app.route('/old-books')
def old_books():
    return redirect(url_for('book_list'))


if __name__ == '__main__':
    app.run(debug=True, port=5030)
