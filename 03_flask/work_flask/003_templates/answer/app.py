from flask import Flask, render_template

app = Flask(__name__)


class Book:
    def __init__(self, id, title, in_stock):
        self.id = id
        self.title = title
        self.in_stock = in_stock


books = [
    Book(1, 'Flask スタートブック', True),
    Book(2, 'Python チュートリアル', False),
    Book(3, 'データベース設計入門', True),
]


@app.route('/')
def index():
    return render_template('top.html')


@app.route('/books')
def book_list():
    return render_template('books.html', books=books)


if __name__ == '__main__':
    app.run(debug=True)
