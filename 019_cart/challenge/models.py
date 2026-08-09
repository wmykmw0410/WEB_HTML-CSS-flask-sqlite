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


# ============================================================
# 問題1：Order・OrderItem モデルを定義する
#
# Order（注文）:
#   id, user_id（誰の注文か）, created_at
# OrderItem（注文明細。1つの注文に複数のOrderItemがぶら下がる）:
#   id, order_id, book_id
#   title, price（注文時点の書籍タイトル・価格を「コピー」して保存する）
#   quantity
#
# なぜ book_id だけでなく title/price もコピーして持つのか？
# → Book は後から値段が変わったり削除されたりする。OrderItem に
#   注文当時のtitle/priceを保存しておかないと、過去の注文履歴の
#   金額が「今の価格」に書き換わって見えてしまう（削除されたら
#   参照エラーにもなる）。注文履歴は「その時の記録」を残すのが原則。
# ============================================================
class Order(db.Model):
    __tablename__ = 'orders'
    pass  # ← ここを実装


class OrderItem(db.Model):
    __tablename__ = 'order_items'
    pass  # ← ここを実装
