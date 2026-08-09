from typing import Optional
from flask import Blueprint, jsonify, request, Response

api_bp = Blueprint('api', __name__, url_prefix='/api')

# 本来はDBから取得する想定のダミーデータ
books: list[dict[str, int | str]] = [
    {"id": 1, "title": "python"},
    {"id": 2, "title": "flask"},
]


@api_bp.get('/books')
def get_books() -> Response:
    return jsonify(books)


@api_bp.get('/books/<int:book_id>')
def get_book(book_id: int) -> tuple[Response, int] | Response:
    book: Optional[dict[str, int | str]] = next((b for b in books if b["id"] == book_id), None)
    if book is None:
        return jsonify({"detail": "Book not found"}), 404
    return jsonify(book)


@api_bp.post('/books')
def create_book() -> tuple[Response, int]:
    data: dict = request.get_json()
    new_book: dict[str, int | str] = {"id": len(books) + 1, "title": data.get("title")}
    books.append(new_book)
    return jsonify(new_book), 201


@api_bp.delete('/books/<int:book_id>')
def delete_book(book_id: int) -> tuple[str, int] | tuple[Response, int]:
    global books
    if not any(b["id"] == book_id for b in books):
        return jsonify({"detail": "Book not found"}), 404
    books = [b for b in books if b["id"] != book_id]
    # 204 No Content はレスポンスボディを持てない
    return '', 204


# 地図表示用のダミーデータ（緯度・経度を持つ地点情報）
shops: list[dict[str, int | str | float]] = [
    {"id": 1, "name": "本店（東京駅）", "lat": 35.681236, "lng": 139.767125},
    {"id": 2, "name": "支店A（東京タワー）", "lat": 35.658581, "lng": 139.745433},
    {"id": 3, "name": "支店B（東京スカイツリー）", "lat": 35.710063, "lng": 139.810700},
]


@api_bp.get('/shops')
def get_shops() -> Response:
    return jsonify(shops)
