"""
練習問題5：id=2 の Memo を削除してください
"""
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
base_dir = os.path.dirname(__file__)
app.config['SQLALCHEMY_DATABASE_URI']        = 'sqlite:///' + os.path.join(base_dir, 'question05.sqlite')
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

# 準備：3件追加して id=1 を更新しておく
with app.app_context():
    memo1 = Memo(title='買い物リスト', body='牛乳・卵・パン')
    memo2 = Memo(title='アイデアメモ',  body='新機能のアイデア')
    memo3 = Memo(title='TODO',         body='請求書を送る')
    db.session.add_all([memo1, memo2, memo3])
    db.session.commit()

with app.app_context():
    memo = Memo.query.filter_by(id=1).first()
    memo.title = '（更新済み）買い物リスト'
    db.session.add(memo)
    db.session.commit()

with app.app_context():
    pass  # TODO: filter_by(id=2) → delete → commit

print("問題5: id=2 を削除")

# クリーンアップ
db_path = os.path.join(base_dir, 'question05.sqlite')
if os.path.exists(db_path):
    os.remove(db_path)
