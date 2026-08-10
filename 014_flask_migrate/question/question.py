"""
練習問題：メモアプリに Flask-Migrate を組み込もう

以下の TODO コメントの箇所にコードを書いて完成させてください。

実行手順:
cd question
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


# ============================================================
# ステップ1：Memo モデルを定義する（初回マイグレーション対象）
# カラム: id / title / body
# ============================================================
class Memo(db.Model):
    __tablename__ = 'memos'
    pass  # ← ここを実装
    # ステップ3：追加後に flask db migrate → upgrade
    # created_at = db.Column(db.String(20))

    def __str__(self):
        return f'Memo(id={self.id}, title={self.title})'


# ============================================================
# ステップ2：2件の Memo を追加して全件表示する
# （テーブル自体は flask db upgrade で作成済みであること）
# ============================================================
def run():
    with app.app_context():
        print('=== INSERT ===')
        # TODO: Memo を2件作成して db.session.add_all() → commit する

        print('=== SELECT ===')
        # TODO: Memo.query.all() で全件取得して表示する


if __name__ == '__main__':
    run()
