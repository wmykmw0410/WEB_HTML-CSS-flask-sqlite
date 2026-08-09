from flask import Flask, redirect, render_template, url_for

app = Flask(__name__)

books = {
    1: {"title": "吾輩は猫である", "author": "夏目漱石", "price": 770, "image": "wagahai_neko.png"},
    2: {"title": "坊っちゃん", "author": "夏目漱石", "price": 660, "image": "bocchan.png"},
    3: {"title": "羅生門", "author": "芥川龍之介", "price": 550, "image": "rashomon.png"},
    4: {"title": "銀河鉄道の夜", "author": "宮沢賢治", "price": 480, "image": "ginga_tetsudo.png"},
    5: {"title": "走れメロス", "author": "太宰治", "price": 440, "image": "hashire_merosu.png"},
}


@app.route('/')
def book_list():
    return render_template('top.html')


@app.route('/books/<int:book_id>')
def book_detail(book_id):
    book = books.get(book_id)

    if book:
        title = book['title']
        author_line = f"著者: {book['author']}"
        price_line = f"¥{book['price']}"
        image = f"/static/img/{book['image']}"
    else:
        title = f'書籍ID {book_id} は見つかりません'
        author_line = ''
        price_line = ''
        image = '/static/img/not_found.png'

    return render_template(
        'detail.html',
        title=title,
        author_line=author_line,
        price_line=price_line,
        image=image,
    )


@app.route('/old-books')
def old_books():
    return redirect(url_for('book_list'))


if __name__ == '__main__':
    app.run(debug=True, port=5010)
