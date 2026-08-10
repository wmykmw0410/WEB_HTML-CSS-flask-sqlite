"""
メモ帳アプリ（認証・所有権・ピン留め・フルCRUD API）

実行:
cd challenge
flask db init
flask db migrate -m "create tables"
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
from memos.views import memos_bp
from api.views import api_bp

app = Flask(__name__)
app.config.from_object('config.Config')

db.init_app(app)
Migrate(app, db)
csrf = CSRFProtect(app)  # memos/index.html等でテンプレート内から直接 csrf_token() を呼ぶために必要
csrf.exempt(api_bp)  # JSON APIはフォームのCSRFトークンを持たないクライアントから呼ばれるため対象外にする

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'   # 未ログイン時の転送先

@login_manager.user_loader
def load_user(user_id: str) -> Optional[User]:
    return User.query.get(int(user_id))

app.register_blueprint(auth_bp)
app.register_blueprint(memos_bp)
app.register_blueprint(api_bp)


@app.route('/')
def index() -> Response:
    return redirect(url_for('memos.index'))


if __name__ == '__main__':
    app.run(debug=True, port=5082)
