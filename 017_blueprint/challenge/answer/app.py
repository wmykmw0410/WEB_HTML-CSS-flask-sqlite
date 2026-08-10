import json
import os
from datetime import datetime
from typing import Optional

from flask import Flask, g
from flask_migrate import Migrate
from flask_login import LoginManager

from models import db, Memo, User

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

base_dir = os.path.dirname(__file__)
app.config['SQLALCHEMY_DATABASE_URI']        = 'sqlite:///' + os.path.join(base_dir, 'memos.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
SEED_JSON_PATH = os.path.join(base_dir, 'memos.json')

# models.py で db = SQLAlchemy() として作っているので、ここで app と結びつける
# （Blueprint から models.py をimportする際の循環importを避けるため）
db.init_app(app)
Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
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


from application.memos.views import memos_bp
from application.auth.views import auth_bp

app.register_blueprint(memos_bp)
app.register_blueprint(auth_bp)


@app.before_request
def set_access_time() -> None:
    g.access_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def init_db() -> None:
    with app.app_context():
        count = Memo.query.count()
        if count == 0:
            with open(SEED_JSON_PATH, encoding='utf-8') as f:
                memos_data = json.load(f)
            db.session.add_all([Memo(**data) for data in memos_data])
            db.session.commit()


if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5052)
