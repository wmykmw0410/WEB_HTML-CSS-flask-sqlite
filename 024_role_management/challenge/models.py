from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship

db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id       = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    books    = relationship('Book', back_populates='owner')
    orders   = relationship('Order', back_populates='user')

    def set_password(self, raw: str) -> None:
        self.password = generate_password_hash(raw)

    def check_password(self, raw: str) -> bool:
        return check_password_hash(self.password, raw)


class Book(db.Model):
    __tablename__ = 'books'

    id      = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title   = db.Column(db.String(100), nullable=False)
    author  = db.Column(db.String(100), nullable=False)
    price   = db.Column(db.Integer, nullable=False)
    genre   = db.Column(db.String(50))
    image   = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)   # 誰が追加したか
    owner   = relationship('User', back_populates='books')


class Order(db.Model):
    __tablename__ = 'orders'

    id          = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id     = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at  = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    postal_code = db.Column(db.String(10))   # 配送先の郵便番号
    address     = db.Column(db.String(200))  # zipcloud APIで解決した住所
    user        = relationship('User', back_populates='orders')
    items       = relationship('OrderItem', back_populates='order')

    @property
    def total(self) -> int:
        return sum(item.subtotal for item in self.items)


class OrderItem(db.Model):
    __tablename__ = 'order_items'

    id       = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    book_id  = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    title    = db.Column(db.String(100), nullable=False)   # 注文時点の書籍タイトルを保存
    price    = db.Column(db.Integer, nullable=False)        # 注文時点の価格を保存
    quantity = db.Column(db.Integer, nullable=False, default=1)
    order    = relationship('Order', back_populates='items')

    @property
    def subtotal(self) -> int:
        return self.price * self.quantity
