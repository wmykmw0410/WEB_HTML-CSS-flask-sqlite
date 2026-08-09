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

    def set_password(self, raw: str) -> None:
        self.password = generate_password_hash(raw)

    def check_password(self, raw: str) -> bool:
        return check_password_hash(self.password, raw)


@login_manager.user_loader
def load_user(user_id: str) -> Optional[User]:
    """
    セッションに保存された id からユーザーを復元する

    Args:
        user_id: セッションに保存されているユーザー id（文字列）

    Returns:
        該当する User。存在しなければ None
    """
    return User.query.get(int(user_id))


class Book(db.Model):
    __tablename__ = 'books'
    id     = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title  = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    price  = db.Column(db.Integer, nullable=False)
    image  = db.Column(db.String, nullable=False)
    genre  = db.Column(db.String, nullable=True)


def init_db() -> None:
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
def book_list() -> str:
    author = request.args.get('author')

    query = Book.query
    if author:
        query = query.filter_by(author=author)
    books = query.all()

    return render_template('top.html', books=books)


@app.route('/books/<int:book_id>')
def book_detail(book_id: int) -> str:
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


@app.route('/register', methods=['GET', 'POST'])
def register() -> str | Response:
    """
    新規ユーザーを登録する

    フォームのバリデーションに成功したら User を作成してパスワードを
    ハッシュ化して保存し、/login にリダイレクトする。
    それ以外は登録フォームを再表示する。

    Returns:
        リダイレクト先の Response、またはフォームを表示する HTML 文字列
    """
    form = RegisterForm()

    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('登録が完了しました。ログインしてください。')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login() -> str | Response:
    """
    ユーザー名とパスワードでログインする

    該当ユーザーが存在し、かつパスワードが一致すればログイン状態にして
    書籍一覧にリダイレクトする。それ以外はエラーメッセージ付きで
    ログインフォームを再表示する。

    Returns:
        リダイレクト先の Response、またはフォームを表示する HTML 文字列
    """
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash(f'ようこそ、{user.username} さん！')
            return redirect(url_for('book_list'))
        flash('ユーザー名またはパスワードが正しくありません。')

    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout() -> Response:
    logout_user()
    flash('ログアウトしました。')
    return redirect(url_for('book_list'))


@app.route('/books/new', methods=['GET', 'POST'])
@login_required
def new_book() -> str | Response:
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


@app.route('/old-books')
def old_books() -> Response:
    return redirect(url_for('book_list'))


if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5048)
