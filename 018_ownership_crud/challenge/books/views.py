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
            # TODO: 問題2 user_id=current_user.id を追加して追加したユーザーを記録する
        )
        db.session.add(book)
        db.session.commit()
        flash('書籍を追加しました。')
        return redirect(url_for('books.detail', book_id=book.id))

    return render_template('books/create.html', form=form)


# ============================================================
# 問題3：書籍編集ルートを実装する
# 自分が追加した書籍だけ編集できるようにする（他人の本は404）。
# BookForm(obj=book) で既存の値をフォームに事前入力できる。
# ============================================================
@books_bp.route('/<int:book_id>/edit', methods=['GET', 'POST'])
@login_required
def update(book_id: int) -> str | Response:
    # TODO: id だけでなく user_id も条件に入れて取得する
    #       （filter_by(id=book_id, user_id=current_user.id).first_or_404()）
    # TODO: BookForm(obj=book) でフォームを作る
    # TODO: form.validate_on_submit() が成功したら、title/author/price/genre を
    #       book に反映してcommit()し、books.detail にリダイレクトする
    # TODO: 画像は isinstance(form.image.data, FileStorage) のときだけ _save_image() する
    # TODO: 上記を実装したら、下の1行は削除する
    flash('未実装です（問題3を実装してください）。')
    return redirect(url_for('books.detail', book_id=book_id))


# ============================================================
# 問題4：書籍削除ルートを実装する
# 自分が追加した書籍だけ削除できるようにする（他人の本は404）。
# ============================================================
@books_bp.route('/<int:book_id>/delete', methods=['POST'])
@login_required
def delete(book_id: int) -> Response:
    # TODO: id だけでなく user_id も条件に入れて取得する
    # TODO: db.session.delete(book) → commit() し、flash してbooks.indexにリダイレクトする
    return redirect(url_for('books.index'))
