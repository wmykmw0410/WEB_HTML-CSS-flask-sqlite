from flask import Blueprint, Response, flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required

from models import Book, Order, OrderItem, db

cart_bp = Blueprint('cart', __name__, url_prefix='/cart')


def get_cart_items() -> list[dict]:
    """セッションのカートデータを {book, quantity, subtotal} のリストに変換する"""
    cart: dict[str, int] = session.get('cart', {})
    items = []
    for book_id_str, quantity in cart.items():
        book = Book.query.get(int(book_id_str))
        if book:
            items.append({
                'book':     book,
                'quantity': quantity,
                'subtotal': book.price * quantity,
            })
    return items


@cart_bp.route('/')
@login_required
def index() -> str:
    items = get_cart_items()
    total = sum(item['subtotal'] for item in items)
    return render_template('cart/index.html', items=items, total=total)


@cart_bp.route('/add/<int:book_id>', methods=['POST'])
@login_required
def add(book_id: int) -> Response:
    Book.query.get_or_404(book_id)   # 存在確認

    cart: dict[str, int] = session.get('cart', {})
    key = str(book_id)
    cart[key] = cart.get(key, 0) + 1
    session['cart'] = cart   # 辞書を直接書き換えただけでは保存されない。再代入が必要

    flash('カートに追加しました。')
    return redirect(url_for('books.index'))


# ============================================================
# 問題2：カート内の数量を直接変更できるようにする
# フォームで送られてきた quantity で置き換える。
# quantity が 0 以下なら、そのカートの中身を削除する。
# ============================================================
@cart_bp.route('/update/<int:book_id>', methods=['POST'])
@login_required
def update(book_id: int) -> Response:
    # TODO: request.form.get('quantity', type=int) で新しい数量を取得する
    # TODO: 0以下なら session['cart'] からそのbook_idを削除、それ以外なら数量を上書きする
    return redirect(url_for('cart.index'))


@cart_bp.route('/remove/<int:book_id>', methods=['POST'])
@login_required
def remove(book_id: int) -> Response:
    cart: dict[str, int] = session.get('cart', {})
    cart.pop(str(book_id), None)
    session['cart'] = cart
    return redirect(url_for('cart.index'))


@cart_bp.route('/clear', methods=['POST'])
@login_required
def clear() -> Response:
    session.pop('cart', None)
    flash('カートを空にしました。')
    return redirect(url_for('cart.index'))


# ============================================================
# 問題3：注文を確定する（チェックアウト）
# カートの中身から Order と OrderItem を作成して保存し、
# セッションのカートを空にする。
# OrderItem には Book の現在の title/price を「コピー」して保存すること
# （あとで本の値段が変わっても、注文当時の金額が変わらないようにするため）。
# ============================================================
@cart_bp.route('/checkout', methods=['POST'])
@login_required
def checkout() -> Response:
    items = get_cart_items()
    if not items:
        flash('カートが空です。')
        return redirect(url_for('cart.index'))

    # TODO: Order(user_id=current_user.id) を作る
    # TODO: items をループして OrderItem を作り、order.items に追加する
    #       （book_id・title・price・quantity をそれぞれ設定する）
    # TODO: db.session.add(order) → commit する
    # TODO: session.pop('cart', None) でカートを空にする
    # TODO: flash → redirect(url_for('cart.complete', order_id=order.id)) を返す

    return redirect(url_for('cart.index'))


@cart_bp.route('/complete/<int:order_id>')
@login_required
def complete(order_id: int) -> str:
    order: Order = Order.query.filter_by(id=order_id, user_id=current_user.id).first_or_404()
    return render_template('cart/complete.html', order=order)


@cart_bp.route('/orders')
@login_required
def orders() -> str:
    my_orders: list[Order] = (
        Order.query.filter_by(user_id=current_user.id).order_by(Order.id.desc()).all()
    )
    return render_template('cart/orders.html', orders=my_orders)
