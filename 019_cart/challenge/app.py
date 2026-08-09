"""
練習問題：ブックストアにカート機能と注文確定（チェックアウト）を実装しよう

018_ownership_crudで作った書籍一覧・詳細・追加・編集・削除の機能はそのままです。
ここに「カートに入れる」→「数量を調整する」→「注文を確定する」という
一連の購入フローを追加します。

以下の TODO コメントの箇所にコードを書いて完成させてください。

実行手順:
    cd challenge
    flask db init
    flask db migrate -m "create orders and order_items tables"
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
from cart.views import cart_bp

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
app.register_blueprint(cart_bp)


@app.route('/')
def index() -> Response:
    return redirect(url_for('books.index'))


if __name__ == '__main__':
    app.run(debug=True, port=5057)
