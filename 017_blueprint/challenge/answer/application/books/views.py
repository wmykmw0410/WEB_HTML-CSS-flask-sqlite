import os

from flask import Blueprint, Response, current_app, redirect, render_template, request, url_for
from flask_login import login_required
from werkzeug.utils import secure_filename

from models import db, Book
from forms import BookForm

books_bp = Blueprint('books', __name__)


@books_bp.route('/')
def book_list() -> str:
    author = request.args.get('author')

    query = Book.query
    if author:
        query = query.filter_by(author=author)
    books = query.all()

    return render_template('top.html', books=books)


@books_bp.route('/books/<int:book_id>')
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


@books_bp.route('/books/new', methods=['GET', 'POST'])
@login_required
def new_book() -> str | Response:
    form = BookForm()

    if form.validate_on_submit():
        image_filename = 'not_found.png'
        if form.image.data and form.image.data.filename:
            image_filename = secure_filename(form.image.data.filename)
            static_img_dir = os.path.join(current_app.root_path, 'static', 'img')
            os.makedirs(static_img_dir, exist_ok=True)
            form.image.data.save(os.path.join(static_img_dir, image_filename))

        new = Book(
            title=form.title.data,
            author=form.author.data,
            price=form.price.data,
            image=image_filename,
        )
        new.genre = form.genre.data
        db.session.add(new)
        db.session.commit()

        return redirect(url_for('books.book_list'))

    return render_template('new_book.html', form=form)


@books_bp.route('/old-books')
def old_books() -> Response:
    return redirect(url_for('books.book_list'))
