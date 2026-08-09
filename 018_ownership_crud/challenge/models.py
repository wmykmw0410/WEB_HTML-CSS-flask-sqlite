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
    # TODO: 問題1 Book への1対多リレーション（books）を追加する

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
    # TODO: 問題1 user_id（ForeignKey('users.id')）と owner リレーションを追加する
