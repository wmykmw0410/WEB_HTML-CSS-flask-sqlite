"""
練習問題：書籍データの管理に Flask-Migrate を組み込もう

013_flask_sqlalchemyで作った書籍一覧・詳細・追加フォーム・リダイレクトの見た目や機能はそのままです。
これまでは db.create_all() でテーブルが無ければ作るだけでしたが、
Flask-Migrate を組み込んで「flask db」コマンドでスキーマを管理する方式に変更し、
既存テーブルに genre（ジャンル）カラムを追加します。

以下の TODO コメントの箇所にコードを書いて完成させてください。

実行手順:
    cd challenge

    # 問題1：Migrate(app, db) を追加したら、まず既存のテーブルを
    # マイグレーション管理下に置く
    flask --app challenge db init
    flask --app challenge db migrate -m "create books table"
    flask --app challenge db upgrade
    python challenge.py   # これまで通り動くことを確認

    # 問題2：Book モデルに genre カラムを追加したら、再度マイグレーション
    flask --app challenge db migrate -m "add genre column"
    flask --app challenge db upgrade

    # 問題3：ルートを genre 対応にしたら、書籍追加フォームで動作確認
    python challenge.py
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
# TODO: 問題1 Migrate(app, db) でマイグレーションを有効にする


class Book(db.Model):
    __tablename__ = 'books'
    id     = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title  = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    price  = db.Column(db.Integer, nullable=False)
    image  = db.Column(db.String, nullable=False)
    # TODO: 問題2 genre カラムを追加する（既存データが壊れないよう nullable にする）


def init_db():
    # テーブル自体は flask db upgrade で作成するため、ここでは
    # db.create_all() を呼ばない
    with app.app_context():
        count = Book.query.count()
        if count == 0:
            # 初回起動時のみ books.json から初期データを投入する
            with open(SEED_JSON_PATH, encoding='utf-8') as f:
                books_data = json.load(f)
            db.session.add_all([Book(**data) for data in books_data])
            db.session.commit()


@app.route('/')
def book_list():
    author = request.args.get('author')

    query = Book.query
    if author:
        query = query.filter_by(author=author)
    books = query.all()

    return render_template('top.html', books=books)


@app.route('/books/<int:book_id>')
def book_detail(book_id):
    book = Book.query.filter_by(id=book_id).first()

    if book:
        title = book.title
        author_line = f"著者: {book.author}"
        price_line = f"¥{book.price}"
        image = f"/static/img/{book.image}"
        # TODO: 問題3 book.genre を使って genre_line を作る（未設定なら空文字）
        genre_line = ''
    else:
        title = f'書籍ID {book_id} は見つかりません'
        author_line = ''
        price_line = ''
        image = '/static/img/not_found.png'
        genre_line = ''

    return render_template(
        'detail.html',
        title=title,
        author_line=author_line,
        price_line=price_line,
        image=image,
        genre_line=genre_line,
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

        new = Book(
            title=form.title.data,
            author=form.author.data,
            price=form.price.data,
            image=image_filename,
        )
        # TODO: 問題3 new.genre = form.genre.data を設定する
        db.session.add(new)
        db.session.commit()

        return redirect(url_for('book_list'))

    return render_template('new_book.html', form=form)


@app.route('/old-books')
def old_books():
    return redirect(url_for('book_list'))


if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5039)
