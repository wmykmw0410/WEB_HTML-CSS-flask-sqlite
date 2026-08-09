"""
練習問題：メモアプリに Flask-Migrate を組み込もう — 解答

実行手順:
    cd question/answer
    flask --app question db init
    flask --app question db migrate -m "create memos table"
    flask --app question db upgrade
    python question.py

カラム追加後（ステップ3）:
    flask --app question db migrate -m "add created_at column"
    flask --app question db upgrade
"""
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

base_dir = os.path.dirname(__file__)
app.config['SECRET_KEY']                  = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI']     = 'sqlite:///' + os.path.join(base_dir, 'memos.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)


# ステップ1：Memo モデルを定義（初回マイグレーション対象）
class Memo(db.Model):
    __tablename__ = 'memos'

    id    = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    body  = db.Column(db.String(500))
    # ステップ3：追加後に flask db migrate → upgrade
    # created_at = db.Column(db.String(20))

    def __str__(self):
        return f'Memo(id={self.id}, title={self.title})'


def run():
    with app.app_context():
        print('=== INSERT ===')
        memo1 = Memo(title='買い物リスト', body='牛乳・卵')
        memo2 = Memo(title='アイデア',     body='新機能のメモ')
        db.session.add_all([memo1, memo2])
        db.session.commit()

        print('=== SELECT ===')
        for memo in Memo.query.all():
            print(f'  {memo}')


if __name__ == '__main__':
    run()
