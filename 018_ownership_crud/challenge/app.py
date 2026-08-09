"""
練習問題：書籍データ管理アプリに所有権とCRUDのフルセットを実装しよう

017_blueprintで作ったブックストアの書籍一覧・詳細・追加・認証の機能はそのままです。
これに「所有権」（誰が追加した本か）を記録する仕組みと、
CRUDのフルセット（編集・削除）を追加します。

models.py・books/views.py の TODO コメントの箇所にコードを書いて
完成させてください。

実行手順:
    cd challenge
    flask db init
    flask db migrate -m "create users and books tables"
    flask db upgrade
    python app.py
"""
from typing import Optional
from flask import Flask, Response, redirect, url_for
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

from models import db, User
from auth.views import auth_bp
from books.views import books_bp

app = Flask(__name__)
app.config.from_object('config.Config')

db.init_app(app)
Migrate(app, db)
CSRFProtect(app)  # books/index.html等でテンプレート内から直接 csrf_token() を呼ぶために必要

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'   # 未ログイン時の転送先

@login_manager.user_loader
def load_user(user_id: str) -> Optional[User]:
    return User.query.get(int(user_id))

app.register_blueprint(auth_bp)
app.register_blueprint(books_bp)


@app.route('/')
def index() -> Response:
    return redirect(url_for('books.index'))


if __name__ == '__main__':
    app.run(debug=True, port=5054)
