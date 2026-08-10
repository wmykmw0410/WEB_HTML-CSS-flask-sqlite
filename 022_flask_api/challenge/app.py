"""
練習問題：メモデータを参照するJSON APIを追加しよう

021_webapiで作ったメモ一覧・詳細・追加・編集・削除・ピン留めの機能はそのままです。
これに加えて、画面用のBlueprintとは別に、メモデータをJSONで返すAPI用の
Blueprint（api_bp）を追加します。

以下の TODO コメントの箇所にコードを書いて完成させてください。

実行手順:
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
CSRFProtect(app)  # memos/index.html等でテンプレート内から直接 csrf_token() を呼ぶために必要

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'   # 未ログイン時の転送先

@login_manager.user_loader
def load_user(user_id: str) -> Optional[User]:
    return User.query.get(int(user_id))

app.register_blueprint(auth_bp)
app.register_blueprint(memos_bp)

# ============================================================
# 問題3：api_bp を登録する
# ============================================================
# TODO: app.register_blueprint(api_bp) を追加する


@app.route('/')
def index() -> Response:
    return redirect(url_for('memos.index'))


if __name__ == '__main__':
    app.run(debug=True, port=5080)
