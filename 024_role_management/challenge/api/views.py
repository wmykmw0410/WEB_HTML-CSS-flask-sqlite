from typing import Optional

from flask import Blueprint, Response, jsonify, request
from flask_login import current_user

from models import Book, db

api_bp = Blueprint('api', __name__, url_prefix='/api')


def book_to_dict(book: Book) -> dict[str, int | str | None]:
    return {
        'id':     book.id,
        'title':  book.title,
        'author': book.author,
        'price':  book.price,
        'genre':  book.genre,
        'image':  book.image,
        'owner':  book.owner.username,
    }


def validate_book_payload(data: dict) -> Optional[str]:
    """必須項目が欠けていればエラーメッセージを、問題なければ None を返す"""
    if not data.get('title'):
        return 'title is required'
    if not data.get('author'):
        return 'author is required'
    if not isinstance(data.get('price'), int):
        return 'price must be an integer'
    return None


@api_bp.get('/books')
def list_books() -> Response:
    author = request.args.get('author')

    query = Book.query
    if author:
        query = query.filter_by(author=author)
    books = query.all()

    return jsonify([book_to_dict(b) for b in books])


@api_bp.get('/books/<int:book_id>')
def get_book(book_id: int) -> tuple[Response, int] | Response:
    book = Book.query.get(book_id)
    if book is None:
        return jsonify({'detail': 'Book not found'}), 404
    return jsonify(book_to_dict(book))


@api_bp.post('/books')
def create_book() -> tuple[Response, int]:
    if not current_user.is_authenticated:
        return jsonify({'detail': 'Login required'}), 401

    data: dict = request.get_json()
    error = validate_book_payload(data)
    if error:
        return jsonify({'detail': error}), 400

    book = Book(
        title=data['title'],
        author=data['author'],
        price=data['price'],
        genre=data.get('genre'),
        user_id=current_user.id,
    )
    db.session.add(book)
    db.session.commit()
    return jsonify(book_to_dict(book)), 201


# ============================================================
# 問題3：所有者 または 管理者だけが更新・削除できるようにする
# ============================================================
@api_bp.put('/books/<int:book_id>')
def update_book(book_id: int) -> tuple[Response, int] | Response:
    if not current_user.is_authenticated:
        return jsonify({'detail': 'Login required'}), 401

    book = Book.query.get(book_id)
    if book is None:
        return jsonify({'detail': 'Book not found'}), 404
    # TODO: book.user_id != current_user.id かつ current_user.is_admin でなければ
    #       jsonify({'detail': 'Forbidden'}), 403 を返す

    data: dict = request.get_json()
    error = validate_book_payload(data)
    if error:
        return jsonify({'detail': error}), 400

    book.title = data['title']
    book.author = data['author']
    book.price = data['price']
    book.genre = data.get('genre')
    db.session.commit()
    return jsonify(book_to_dict(book))


@api_bp.delete('/books/<int:book_id>')
def delete_book(book_id: int) -> tuple[str, int] | tuple[Response, int]:
    if not current_user.is_authenticated:
        return jsonify({'detail': 'Login required'}), 401

    book = Book.query.get(book_id)
    if book is None:
        return jsonify({'detail': 'Book not found'}), 404
    # TODO: book.user_id != current_user.id かつ current_user.is_admin でなければ
    #       jsonify({'detail': 'Forbidden'}), 403 を返す

    db.session.delete(book)
    db.session.commit()
    return '', 204
