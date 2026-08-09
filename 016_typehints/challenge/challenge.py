"""
練習問題：書籍データの管理コードに型ヒントとdocstringを付けよう

015_loginで作った書籍一覧・詳細・追加フォーム・新規登録・ログイン・ログアウトの
機能はそのままです（新しい機能は追加しません）。
このチャプターで学んだ型ヒント（Optional・Union）とdocstringを、
既存のコードに後付けする練習です。

以下の TODO コメントの箇所に型ヒント・docstringを追加してください。
実行手順:
    cd challenge
    flask --app challenge db init
    flask --app challenge db migrate -m "create books and users tables"
    flask --app challenge db upgrade
    python challenge.py
"""
import json
import os
from typing import Optional

from flask import Flask, Response, redirect, render_template, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from forms import BookForm, RegisterForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

base_dir = os.path.dirname(__file__)
app.config['SQLALCHEMY_DATABASE_URI']        = 'sqlite:///' + os.path.join(base_dir, 'books.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
SEED_JSON_PATH = os.path.join(base_dir, 'books.json')
STATIC_IMG_DIR = os.path.join(base_dir, 'static', 'img')

db = SQLAlchemy(app)
Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'ログインしてください。'


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id       = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)

    # TODO: 問題1 set_password / check_password に型ヒントを付ける
    def set_password(self, raw):
        self.password = generate_password_hash(raw)

    def check_password(self, raw):
        return check_password_hash(self.password, raw)


# TODO: 問題2 load_user に型ヒントを付ける（Optional[User] を使う）
# TODO: 問題4 load_user にGoogle形式のdocstringを追加する
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Book(db.Model):
    __tablename__ = 'books'
    id     = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title  = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    price  = db.Column(db.Integer, nullable=False)
    image  = db.Column(db.String, nullable=False)
    genre  = db.Column(db.String, nullable=True)


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


# TODO: 問題3 book_list に戻り値の型ヒントを付ける
@app.route('/')
def book_list():
    author = request.args.get('author')

    query = Book.query
    if author:
        query = query.filter_by(author=author)
    books = query.all()

    return render_template('top.html', books=books)


# TODO: 問題3 book_detail に引数・戻り値の型ヒントを付ける
@app.route('/books/<int:book_id>')
def book_detail(book_id):
    book = Book.query.filter_by(id=book_id).first()

    if book:
        title = book.title
        author_line = f"著者: {book.author}"
        price_line = f"¥{book.price}"
        image = f"/static/img/{book.image}"
        genre_line = f"ジャンル: {book.genre}" if book.genre else ''
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


# TODO: 問題3 register に戻り値の型ヒントを付ける（str | Response）
# TODO: 問題4 register にGoogle形式のdocstringを追加する
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('登録が完了しました。ログインしてください。')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


# TODO: 問題3 login に戻り値の型ヒントを付ける（str | Response）
# TODO: 問題4 login にGoogle形式のdocstringを追加する
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash(f'ようこそ、{user.username} さん！')
            return redirect(url_for('book_list'))
        flash('ユーザー名またはパスワードが正しくありません。')

    return render_template('login.html', form=form)


# TODO: 問題3 logout に戻り値の型ヒントを付ける（Response）
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('ログアウトしました。')
    return redirect(url_for('book_list'))


# TODO: 問題3 new_book に戻り値の型ヒントを付ける（str | Response）
@app.route('/books/new', methods=['GET', 'POST'])
@login_required
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
        new.genre = form.genre.data
        db.session.add(new)
        db.session.commit()

        return redirect(url_for('book_list'))

    return render_template('new_book.html', form=form)


# TODO: 問題3 old_books に戻り値の型ヒントを付ける（Response）
@app.route('/old-books')
def old_books():
    return redirect(url_for('book_list'))


if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5047)
