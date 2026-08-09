"""
練習問題2：3件の Memo を db.session.add_all() で追加してください

データ例:
  title='買い物リスト', body='牛乳・卵・パン'
  title='アイデアメモ',  body='新機能のアイデア'
  title='TODO',         body='請求書を送る'
"""
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
base_dir = os.path.dirname(__file__)
app.config['SQLALCHEMY_DATABASE_URI']        = 'sqlite:///' + os.path.join(base_dir, 'question02.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Memo(db.Model):
    __tablename__ = 'memos'
    id    = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    body  = db.Column(db.String(500))


with app.app_context():
    db.drop_all()
    db.create_all()

with app.app_context():
    pass  # TODO: Memo を3件作成して add_all → commit

print("問題2: 3件追加完了")

# クリーンアップ
db_path = os.path.join(base_dir, 'question02.sqlite')
if os.path.exists(db_path):
    os.remove(db_path)
