"""
練習問題：書籍データの保存先を SQLAlchemy（生）から Flask-SQLAlchemy に変更しよう

012_sqlalchemyで作った書籍一覧・詳細・追加フォーム・リダイレクトの見た目や機能はそのままです。
データの持ち方だけを、engine / Session を自分で管理する書き方から
Flask-SQLAlchemy（db.Model / db.session / app_context）に置き換えます。

以下の TODO コメントの箇所にコードを書いて完成させてください。
実行方法: python challenge/challenge.py
"""
import json
import os

from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

from forms import BookForm

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

base_dir = os.path.dirname(__file__)
app.config['SQLALCHEMY_DATABASE_URI']        = 'sqlite:///' + os.path.join(base_dir, 'books.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
SEED_JSON_PATH = os.path.join(base_dir, 'books.json')
STATIC_IMG_DIR = os.path.join(base_dir, 'static', 'img')

db = SQLAlchemy(app)


# ============================================================
# 問題1：Book モデルを db.Model で定義してテーブルを作成する
# カラムは id / title / author / price / image（012_sqlalchemyと同じ）
# ============================================================
class Book(db.Model):
    __tablename__ = 'books'
    pass  # ← ここを実装


def init_db():
    with app.app_context():
        # TODO: db.create_all() でテーブルを作成する

        count = Book.query.count()
        if count == 0:
            # 初回起動時のみ books.json から初期データを投入する
            with open(SEED_JSON_PATH, encoding='utf-8') as f:
                books_data = json.load(f)
            db.session.add_all([Book(**data) for data in books_data])
            db.session.commit()


init_db()


# ============================================================
# 問題2：書籍一覧を取得する
# author が指定されていれば filter_by(author=author) で絞り込み、
# 指定が無ければ全件取得すること
# @app.route の中は Flask がコンテキストを自動で用意するので
# with app.app_context(): は不要
# ============================================================
@app.route('/')
def book_list():
    author = request.args.get('author')

    # TODO: Book.query を使って books を取得する
    books = []

    return render_template('top.html', books=books)


# ============================================================
# 問題3：id を指定して書籍を1件取得する
# 見つからない場合の表示（title/author_line/price_line/image）は
# これまでと同じ
# ============================================================
@app.route('/books/<int:book_id>')
def book_detail(book_id):
    # TODO: Book.query.filter_by(id=book_id).first() で book を取得する
    book = None

    if book:
        title = book.title
        author_line = f"著者: {book.author}"
        price_line = f"¥{book.price}"
        image = f"/static/img/{book.image}"
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
# 問題4：新しい書籍を追加する
# Book インスタンスを作って db.session.add() → db.session.commit() すること
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

        # TODO: Book(...) を作って db.session.add() → db.session.commit() する

        return redirect(url_for('book_list'))

    return render_template('new_book.html', form=form)


@app.route('/old-books')
def old_books():
    return redirect(url_for('book_list'))


if __name__ == '__main__':
    app.run(debug=True, port=5036)
