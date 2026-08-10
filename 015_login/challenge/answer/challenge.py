import json
import os

from flask import Flask, redirect, render_template, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from forms import MemoForm, RegisterForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

base_dir = os.path.dirname(__file__)
app.config['SQLALCHEMY_DATABASE_URI']        = 'sqlite:///' + os.path.join(base_dir, 'memos.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
SEED_JSON_PATH = os.path.join(base_dir, 'memos.json')

db = SQLAlchemy(app)
Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'ログインしてください。'


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id       = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)

    def set_password(self, raw):
        self.password = generate_password_hash(raw)

    def check_password(self, raw):
        return check_password_hash(self.password, raw)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Memo(db.Model):
    __tablename__ = 'memos'
    id       = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title    = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    body     = db.Column(db.String, nullable=False)
    due_date = db.Column(db.String, nullable=True)


def init_db():
    # テーブル自体は flask db upgrade で作成するため、ここでは
    # db.create_all() を呼ばない
    with app.app_context():
        count = Memo.query.count()
        if count == 0:
            # 初回起動時のみ memos.json から初期データを投入する
            with open(SEED_JSON_PATH, encoding='utf-8') as f:
                memos_data = json.load(f)
            db.session.add_all([Memo(**data) for data in memos_data])
            db.session.commit()


@app.route('/')
def memo_list():
    category = request.args.get('category')

    query = Memo.query
    if category:
        query = query.filter_by(category=category)
    memos = query.all()

    return render_template('top.html', memos=memos)


@app.route('/memos/<int:memo_id>')
def memo_detail(memo_id):
    memo = Memo.query.filter_by(id=memo_id).first()

    if memo:
        title = memo.title
        category = memo.category
        body = memo.body
        due_date_line = f"期限: {memo.due_date}" if memo.due_date else ''
    else:
        title = f'メモID {memo_id} は見つかりません'
        category = ''
        body = ''
        due_date_line = ''

    return render_template(
        'detail.html',
        title=title,
        category=category,
        body=body,
        due_date_line=due_date_line,
    )


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
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash(f'ようこそ、{user.username} さん！')
            return redirect(url_for('memo_list'))
        flash('ユーザー名またはパスワードが正しくありません。')

    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('ログアウトしました。')
    return redirect(url_for('memo_list'))


@app.route('/memos/new', methods=['GET', 'POST'])
@login_required
def new_memo():
    form = MemoForm()

    if form.validate_on_submit():
        new = Memo(
            title=form.title.data,
            category=form.category.data,
            body=form.body.data,
        )
        new.due_date = form.due_date.data
        db.session.add(new)
        db.session.commit()

        return redirect(url_for('memo_list'))

    return render_template('new_memo.html', form=form)


@app.route('/old-memos')
def old_memos():
    return redirect(url_for('memo_list'))


if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5046)
