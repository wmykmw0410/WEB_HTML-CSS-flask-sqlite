"""
練習問題 解答アプリ

問題1: RegisterForm にパスワード確認欄（confirm フィールド）を追加
問題2: ログイン成功時に flash メッセージを表示
問題3: ログイン済みユーザーが /login に来たらトップにリダイレクト
問題4: 重複ユーザー名での登録をブロック（forms.py の validate_username）

実行:
    cd question/answer/02_app
    flask db init
    flask db migrate -m "create users table"
    flask db upgrade
    python app.py
"""
import os
from flask import Flask, render_template, redirect, url_for, flash
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

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
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
def login():
    # 問題3：ログイン済みならトップへ
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash(f'ようこそ、{user.username} さん！')   # 問題2
            return redirect(url_for('mypage'))
        flash('ユーザー名またはパスワードが正しくありません。')
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('ログアウトしました。')
    return redirect(url_for('index'))


@app.route('/mypage')
@login_required
def mypage():
    return render_template('mypage.html')


if __name__ == '__main__':
    app.run(debug=True, port=5044)
