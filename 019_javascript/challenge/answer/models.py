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
    memos    = relationship('Memo', back_populates='owner')

    def set_password(self, raw: str) -> None:
        self.password = generate_password_hash(raw)

    def check_password(self, raw: str) -> bool:
        return check_password_hash(self.password, raw)


class Memo(db.Model):
    __tablename__ = 'memos'

    id       = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title    = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    body     = db.Column(db.String(500), nullable=False)
    due_date = db.Column(db.String(50))
    is_pinned = db.Column(db.Boolean, nullable=False, default=False)   # ピン留め（fetch()で切り替える）
    user_id  = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)   # 誰が追加したか
    owner    = relationship('User', back_populates='memos')
