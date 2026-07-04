from flask import Flask, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>書籍管理アプリ</h1>'

@app.route('/books', methods=['GET'])
def book_list():
    return '<h1>書籍一覧</h1>'

@app.route('/books/<int:book_id>', methods=['GET'])
def book_detail(book_id):
    return f'<h1>書籍 {book_id} の詳細</h1>'

@app.route('/books', methods=['POST'])
def book_create():
    return '<h1>書籍を登録しました</h1>'

@app.route('/old-books')
def old_books():
    return redirect(url_for('book_list'))

@app.errorhandler(404)
def not_found(e):
    return '<h1>404 - ページが見つかりません</h1>', 404

if __name__ == '__main__':
    app.run(debug=True)
