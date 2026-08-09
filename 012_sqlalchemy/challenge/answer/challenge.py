import json
import os

from flask import Flask, redirect, render_template, request, url_for
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
from werkzeug.utils import secure_filename

from forms import BookForm

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

base_dir = os.path.dirname(__file__)
DB_PATH = os.path.join(base_dir, 'books.db')
SEED_JSON_PATH = os.path.join(base_dir, 'books.json')
STATIC_IMG_DIR = os.path.join(base_dir, 'static', 'img')

engine = create_engine('sqlite:///' + DB_PATH)
Base = declarative_base()
Session = sessionmaker(bind=engine)


class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    image = Column(String, nullable=False)


def init_db():
    Base.metadata.create_all(engine)

    session = Session()
    count = session.query(Book).count()
    if count == 0:
        # 初回起動時のみ books.json から初期データを投入する
        with open(SEED_JSON_PATH, encoding='utf-8') as f:
            books_data = json.load(f)
        session.add_all([Book(**data) for data in books_data])
        session.commit()
    session.close()


init_db()


@app.route('/')
def book_list():
    author = request.args.get('author')

    session = Session()
    query = session.query(Book)
    if author:
        query = query.filter_by(author=author)
    books = query.all()
    session.close()

    return render_template('top.html', books=books)


@app.route('/books/<int:book_id>')
def book_detail(book_id):
    session = Session()
    book = session.query(Book).filter_by(id=book_id).first()
    session.close()

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

        session = Session()
        new = Book(
            title=form.title.data,
            author=form.author.data,
            price=form.price.data,
            image=image_filename,
        )
        session.add(new)
        session.commit()
        session.close()

        return redirect(url_for('book_list'))

    return render_template('new_book.html', form=form)


@app.route('/old-books')
def old_books():
    return redirect(url_for('book_list'))


if __name__ == '__main__':
    app.run(debug=True, port=5035)
