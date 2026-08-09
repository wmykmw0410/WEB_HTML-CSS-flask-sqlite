"""
練習問題：書籍データをbooks.jsonから読み込むようにしよう

006_jinja2で作った書籍一覧・詳細ページ・リダイレクトはそのまま使います。
これまでハードコードしていた books 辞書を、100_bookstore_api/example/flask_app/seed.py
と同じやり方（with open() + os.path + json.load()）で books.json から読み込むように変更します。

以下の TODO コメントの箇所にコードを書いて完成させてください。
実行方法: python practice/practice.py
"""
from flask import Flask, redirect, render_template, url_for

app = Flask(__name__)

# ============================================================
# 問題：books.json を読み込んで books 辞書を作る
#
# 1. os.path.join(os.path.dirname(__file__), 'books.json') でパスを組み立てる
# 2. with open(パス, encoding='utf-8') as f: で開く
# 3. json.load(f) でリストとして読み込む（[{"title": ..., "author": ...}, ...]）
# 4. {i + 1: book for i, book in enumerate(リスト)} で
#    これまでと同じ「idをキーにした辞書」に変換する
# ============================================================
# TODO: 上のヒントに沿って books を作る（下の1行を置き換える）
books = {}


@app.route('/')
def book_list():
    book_list_data = [{"id": book_id, **book} for book_id, book in books.items()]
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
    app.run(debug=True, port=5016)
