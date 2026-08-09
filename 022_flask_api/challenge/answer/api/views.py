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
