import os

from flask import Blueprint, Response, current_app, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from models import Book, db
from forms import BookForm

books_bp = Blueprint('books', __name__, url_prefix='/books')


@books_bp.route('/')
def index() -> str:
    author = request.args.get('author')

    query = Book.query
    if author:
        query = query.filter_by(author=author)
    books = query.all()

    return render_template('books/index.html', books=books)


@books_bp.route('/<int:book_id>')
def detail(book_id: int) -> str:
    book = Book.query.get_or_404(book_id)
    return render_template('books/detail.html', book=book)


def _save_image(form: BookForm) -> str:
    image_filename = secure_filename(form.image.data.filename)
    static_img_dir = os.path.join(current_app.root_path, 'static', 'img')
    os.makedirs(static_img_dir, exist_ok=True)
    form.image.data.save(os.path.join(static_img_dir, image_filename))
    return image_filename


@books_bp.route('/new', methods=['GET', 'POST'])
@login_required
def create() -> str | Response:
    form = BookForm()

    if form.validate_on_submit():
        image_filename = 'not_found.png'
        if form.image.data and form.image.data.filename:
            image_filename = _save_image(form)

        book = Book(
            title=form.title.data,
            author=form.author.data,
            price=form.price.data,
            genre=form.genre.data,
            image=image_filename,
            user_id=current_user.id,   # ← 追加したユーザーを記録
        )
        db.session.add(book)
        db.session.commit()
        flash('書籍を追加しました。')
        return redirect(url_for('books.detail', book_id=book.id))

    return render_template('books/create.html', form=form)


@books_bp.route('/<int:book_id>/edit', methods=['GET', 'POST'])
@login_required
def update(book_id: int) -> str | Response:
    # id だけでなく user_id も条件に入れる → 他人の本を指定されても404
    book: Book = Book.query.filter_by(id=book_id, user_id=current_user.id).first_or_404()
    form = BookForm(obj=book)

    if form.validate_on_submit():
        book.title  = form.title.data
        book.author = form.author.data
        book.price  = form.price.data
        book.genre  = form.genre.data
        # obj=book によって image に既存のファイル名（str）が入っているため、
        # 実際にファイルが選択された（FileStorage）ときだけ保存し直す
        if isinstance(form.image.data, FileStorage) and form.image.data.filename:
            book.image = _save_image(form)
        db.session.commit()
        flash('書籍を更新しました。')
        return redirect(url_for('books.detail', book_id=book.id))

    return render_template('books/update.html', form=form, book=book)


@books_bp.route('/<int:book_id>/delete', methods=['POST'])
@login_required
def delete(book_id: int) -> Response:
    book: Book = Book.query.filter_by(id=book_id, user_id=current_user.id).first_or_404()
    db.session.delete(book)
    db.session.commit()
    flash('書籍を削除しました。')
    return redirect(url_for('books.index'))
