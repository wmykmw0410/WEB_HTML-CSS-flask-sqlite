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


class Book(db.Model):
    __tablename__ = 'books'
    id     = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title  = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    price  = db.Column(db.Integer, nullable=False)
    image  = db.Column(db.String, nullable=False)


def init_db():
    with app.app_context():
        db.create_all()

        count = Book.query.count()
        if count == 0:
            # 初回起動時のみ books.json から初期データを投入する
            with open(SEED_JSON_PATH, encoding='utf-8') as f:
                books_data = json.load(f)
            db.session.add_all([Book(**data) for data in books_data])
            db.session.commit()


init_db()


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

        new = Book(
            title=form.title.data,
            author=form.author.data,
            price=form.price.data,
            image=image_filename,
        )
        db.session.add(new)
        db.session.commit()

        return redirect(url_for('book_list'))

    return render_template('new_book.html', form=form)


@app.route('/old-books')
def old_books():
    return redirect(url_for('book_list'))


if __name__ == '__main__':
    app.run(debug=True, port=5037)
