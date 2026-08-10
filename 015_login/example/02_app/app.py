"""
ログイン機能付き最小アプリ

実行:
cd example/02_app
flask db init
flask db migrate -m "create users table"
flask db upgrade
python app.py
ブラウザで http://localhost:5000 にアクセス
"""
import os
from typing import Optional
from flask import Flask, Response, render_template, redirect, url_for, flash
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from models import db, User
from forms import LoginForm, RegisterForm

app = Flask(__name__)

base_dir = os.path.dirname(__file__)
app.config['SECRET_KEY']                     = 'dev-secret-key'
app.config['SQLALCHEMY_DATABASE_URI']        = 'sqlite:///' + os.path.join(base_dir, 'users.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
Migrate(app, db)

# --------------------------------------------------
# Flask-Login のセットアップ
# --------------------------------------------------
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'           # 未ログイン時のリダイレクト先

@login_manager.user_loader
def load_user(user_id: str) -> Optional[User]:
    return User.query.get(int(user_id))


# --------------------------------------------------
# ルート
# --------------------------------------------------
@app.route('/')
def index() -> str:
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register() -> str | Response:
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('登録が完了しました。ログインしてください。')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login() -> str | Response:
    form = LoginForm()
    if form.validate_on_submit():
        user: Optional[User] = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('mypage'))
        flash('ユーザー名またはパスワードが正しくありません。')
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout() -> Response:
    logout_user()
    return redirect(url_for('index'))


@app.route('/mypage')
@login_required
def mypage() -> str:
    return render_template('mypage.html')


if __name__ == '__main__':
    app.run(debug=True, port=5042)
