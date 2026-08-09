from flask import Blueprint, Response, jsonify, request

from models import Book

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


# ============================================================
# 問題1：書籍一覧をJSONで返す
# books.index と同様、?author= が指定されていれば絞り込む
# ============================================================
@api_bp.get('/books')
def list_books() -> Response:
    # TODO: Book.query を使って books を取得する（?author= があれば filter_by）
    # TODO: book_to_dict() で変換したリストを jsonify() で返す
    return jsonify([])


# ============================================================
# 問題2：書籍を1件JSONで返す
# 見つからなければ {"detail": "Book not found"} を404で返す
# ============================================================
@api_bp.get('/books/<int:book_id>')
def get_book(book_id: int) -> tuple[Response, int] | Response:
    # TODO: Book.query.get(book_id) で取得する
    # TODO: None なら jsonify({'detail': 'Book not found'}), 404 を返す
    # TODO: 見つかれば jsonify(book_to_dict(book)) を返す
    return jsonify({'detail': 'Book not found'}), 404
