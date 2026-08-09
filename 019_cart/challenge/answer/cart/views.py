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


@cart_bp.route('/update/<int:book_id>', methods=['POST'])
@login_required
def update(book_id: int) -> Response:
    quantity = request.form.get('quantity', type=int)
    cart: dict[str, int] = session.get('cart', {})
    key = str(book_id)

    if quantity is None or quantity <= 0:
        cart.pop(key, None)
    else:
        cart[key] = quantity
    session['cart'] = cart

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


@cart_bp.route('/checkout', methods=['POST'])
@login_required
def checkout() -> Response:
    items = get_cart_items()
    if not items:
        flash('カートが空です。')
        return redirect(url_for('cart.index'))

    order = Order(user_id=current_user.id)
    for item in items:
        order.items.append(OrderItem(
            book_id=item['book'].id,
            title=item['book'].title,
            price=item['book'].price,
            quantity=item['quantity'],
        ))
    db.session.add(order)
    db.session.commit()

    session.pop('cart', None)
    flash('注文が確定しました。')
    return redirect(url_for('cart.complete', order_id=order.id))


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
