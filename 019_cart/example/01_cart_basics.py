"""
セッションを使ったカートの基本（DB不使用の最小サンプル）

実行:
    python example/01_cart_basics.py
    ブラウザで http://localhost:5000 にアクセス
"""
from flask import Flask, redirect, session, url_for, request

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

BOOKS = {
    1: {'title': '吾輩は猫である', 'price': 770},
    2: {'title': '坊っちゃん', 'price': 660},
    3: {'title': '羅生門', 'price': 550},
}


@app.route('/')
def index() -> str:
    html = '<h1>書籍一覧</h1><ul>'
    for book_id, book in BOOKS.items():
        html += f'''
        <li>{book["title"]}（¥{book["price"]}）
            <form method="post" action="{url_for('add_to_cart', book_id=book_id)}" style="display:inline">
                <button type="submit">カートに追加</button>
            </form>
        </li>'''
    html += '</ul><p><a href="/cart">カートを見る</a></p>'
    return html


@app.route('/cart/add/<int:book_id>', methods=['POST'])
def add_to_cart(book_id: int):
    cart: dict[str, int] = session.get('cart', {})
    key = str(book_id)
    cart[key] = cart.get(key, 0) + 1
    session['cart'] = cart   # 辞書を直接書き換えただけでは保存されない。再代入が必要
    return redirect(url_for('index'))


@app.route('/cart')
def cart_view() -> str:
    cart: dict[str, int] = session.get('cart', {})
    total = 0
    html = '<h1>カート</h1><ul>'
    for book_id_str, quantity in cart.items():
        book = BOOKS[int(book_id_str)]
        subtotal = book['price'] * quantity
        total += subtotal
        html += f'<li>{book["title"]} × {quantity} = ¥{subtotal}</li>'
    html += f'</ul><p>合計: ¥{total}</p>'
    html += f'''
    <form method="post" action="{url_for('checkout')}">
        <button type="submit">注文を確定する</button>
    </form>'''
    html += '<p><a href="/">← 一覧に戻る</a></p>'
    return html


@app.route('/cart/checkout', methods=['POST'])
def checkout() -> str:
    session.pop('cart', None)   # 注文確定したのでカートを空にする
    return '<h1>注文が完了しました</h1><p><a href="/">← 一覧に戻る</a></p>'


if __name__ == '__main__':
    app.run(debug=True, port=5056)
