from typing import Optional

from flask import Blueprint, Response, jsonify, request

api_bp = Blueprint('api', __name__, url_prefix='/api')

# 本来はDBから取得する想定のダミーデータ
books: list[dict[str, int | str]] = [
    {'id': 1, 'title': 'python', 'price': 2000},
    {'id': 2, 'title': 'flask', 'price': 2500},
]


def find_book(book_id: int) -> Optional[dict[str, int | str]]:
    return next((b for b in books if b['id'] == book_id), None)


def validate_book_payload(data: dict) -> Optional[str]:
    """必須項目が欠けていればエラーメッセージを、問題なければ None を返す"""
    if not data.get('title'):
        return 'title is required'
    if not isinstance(data.get('price'), int):
        return 'price must be an integer'
    return None


@api_bp.get('/books')
def get_books() -> Response:
    return jsonify(books)


@api_bp.get('/books/<int:book_id>')
def get_book(book_id: int) -> tuple[Response, int] | Response:
    book = find_book(book_id)
    if book is None:
        return jsonify({'detail': 'Book not found'}), 404
    return jsonify(book)


@api_bp.post('/books')
def create_book() -> tuple[Response, int]:
    data: dict = request.get_json()

    error = validate_book_payload(data)
    if error:
        return jsonify({'detail': error}), 400

    new_book: dict[str, int | str] = {
        'id':    len(books) + 1,
        'title': data['title'],
        'price': data['price'],
    }
    books.append(new_book)
    return jsonify(new_book), 201


@api_bp.put('/books/<int:book_id>')
def update_book(book_id: int) -> tuple[Response, int] | Response:
    book = find_book(book_id)
    if book is None:
        return jsonify({'detail': 'Book not found'}), 404

    data: dict = request.get_json()
    error = validate_book_payload(data)
    if error:
        return jsonify({'detail': error}), 400

    book['title'] = data['title']
    book['price'] = data['price']
    return jsonify(book)


@api_bp.delete('/books/<int:book_id>')
def delete_book(book_id: int) -> tuple[str, int] | tuple[Response, int]:
    global books
    if find_book(book_id) is None:
        return jsonify({'detail': 'Book not found'}), 404
    books = [b for b in books if b['id'] != book_id]
    # 204 No Content はレスポンスボディを持てない
    return '', 204
