"""
練習問題：書籍データの管理アプリをBlueprintで分割しよう

016_typehintsで作った書籍一覧・詳細・追加フォーム・新規登録・ログイン・ログアウトの
機能はそのままです（新しい機能は追加しません）。
1ファイルにまとまっていたルートを、books（書籍関連）とauth（認証関連）の
2つのBlueprintに分割し、gオブジェクトの使い方も練習します。

以下の TODO コメントの箇所にコードを書いて完成させてください。

実行手順:
    cd challenge
    flask db init
    flask db migrate -m "create books and users tables"
    flask db upgrade
    python app.py
"""
import json
import os
from datetime import datetime
from typing import Optional

from flask import Flask, g
from flask_migrate import Migrate
from flask_login import LoginManager

from models import db, Book, User

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

base_dir = os.path.dirname(__file__)
app.config['SQLALCHEMY_DATABASE_URI']        = 'sqlite:///' + os.path.join(base_dir, 'books.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
SEED_JSON_PATH = os.path.join(base_dir, 'books.json')

# models.py で db = SQLAlchemy() として作っているので、ここで app と結びつける
# （Blueprint から models.py をimportする際の循環importを避けるため）
db.init_app(app)
Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
# TODO: 問題2 'login' を Blueprint 形式のエンドポイント名に書き換える
login_manager.login_view = 'login'
login_manager.login_message = 'ログインしてください。'


@login_manager.user_loader
def load_user(user_id: str) -> Optional[User]:
    """
    セッションに保存された id からユーザーを復元する

    Args:
        user_id: セッションに保存されているユーザー id（文字列）

    Returns:
        該当する User。存在しなければ None
    """
    return User.query.get(int(user_id))


from application.books.views import books_bp
from application.auth.views import auth_bp

# TODO: 問題1 books_bp と auth_bp を app.register_blueprint() で登録する


# ============================================================
# 問題4：g オブジェクトにアクセス時刻をセットする
# before_request で g.access_time に現在時刻の文字列をセットし、
# templates/base.html のフッターで表示する
# ============================================================
@app.before_request
def set_access_time() -> None:
    pass  # ← ここを実装


def init_db() -> None:
    with app.app_context():
        count = Book.query.count()
        if count == 0:
            with open(SEED_JSON_PATH, encoding='utf-8') as f:
                books_data = json.load(f)
            db.session.add_all([Book(**data) for data in books_data])
            db.session.commit()


if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5051)
