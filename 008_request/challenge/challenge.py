"""
練習問題：書籍一覧ページに、著者名で絞り込むクエリパラメータを追加しよう

007_withで作った書籍一覧・詳細ページ・リダイレクトはそのまま使います。
以下の TODO コメントの箇所にコードを書いて完成させてください。
実行方法: python challenge/challenge.py
"""
import json
import os

from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

BOOKS_PATH = os.path.join(os.path.dirname(__file__), 'books.json')

with open(BOOKS_PATH, encoding='utf-8') as f:
    books_list = json.load(f)

books = {i + 1: book for i, book in enumerate(books_list)}


# ============================================================
# 問題：著者名で絞り込むクエリパラメータを追加する
# GET / で、クエリパラメータ author が指定されていれば
# その著者の書籍だけに絞り込んで top.html を描画してください
# （例: /?author=夏目漱石 で夏目漱石の本だけ表示）
# 指定が無ければ全件を表示すること
# ============================================================
@app.route('/')
def book_list():
    author = request.args.get('author')

    book_list_data = [{"id": book_id, **book} for book_id, book in books.items()]

    # TODO: author が指定されていたら、book_list_data を著者名で絞り込む

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


@app.route('/old-books')
def old_books():
    return redirect(url_for('book_list'))


if __name__ == '__main__':
    app.run(debug=True, port=5021)
