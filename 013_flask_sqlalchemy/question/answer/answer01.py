"""
練習問題1：Memo モデルを定義してテーブルを作成する — 解答
"""
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
base_dir = os.path.dirname(__file__)
app.config['SQLALCHEMY_DATABASE_URI']        = 'sqlite:///' + os.path.join(base_dir, 'answer01.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Memo(db.Model):
    __tablename__ = 'memos'
    id    = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    body  = db.Column(db.String(500))

    def __str__(self):
        return f"id={self.id}  {self.title}  {self.body}"


with app.app_context():
    db.drop_all()
    db.create_all()
print("問題1: テーブル作成完了")

# クリーンアップ
db_path = os.path.join(base_dir, 'answer01.sqlite')
if os.path.exists(db_path):
    os.remove(db_path)
