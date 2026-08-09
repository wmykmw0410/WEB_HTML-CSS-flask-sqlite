from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id       = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)

    def set_password(self, raw: str) -> None:
        self.password = generate_password_hash(raw)

    def check_password(self, raw: str) -> bool:
        return check_password_hash(self.password, raw)


class Book(db.Model):
    __tablename__ = 'books'
    id     = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title  = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    price  = db.Column(db.Integer, nullable=False)
    image  = db.Column(db.String, nullable=False)
    genre  = db.Column(db.String, nullable=True)
