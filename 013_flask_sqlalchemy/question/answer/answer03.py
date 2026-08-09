"""
練習問題3：Memo.query.all() で全件取得して表示する — 解答
"""
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
base_dir = os.path.dirname(__file__)
app.config['SQLALCHEMY_DATABASE_URI']        = 'sqlite:///' + os.path.join(base_dir, 'answer03.sqlite')
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
    memo1 = Memo(title='買い物リスト', body='牛乳・卵・パン')
    memo2 = Memo(title='アイデアメモ',  body='新機能のアイデア')
    memo3 = Memo(title='TODO',         body='請求書を送る')
    db.session.add_all([memo1, memo2, memo3])
    db.session.commit()

print("問題3: 全件一覧")
with app.app_context():
    memos = Memo.query.all()
    for memo in memos:
        print(f"  id={memo.id}  {memo.title}  {memo.body}")

# クリーンアップ
db_path = os.path.join(base_dir, 'answer03.sqlite')
if os.path.exists(db_path):
    os.remove(db_path)
