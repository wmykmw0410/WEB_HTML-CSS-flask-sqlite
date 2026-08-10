"""
練習問題：メモデータの管理にログイン機能を組み込もう

014_flask_migrateで作ったメモ一覧・詳細・追加フォーム・リダイレクトの見た目や機能はそのままです。
ここに Flask-Login を組み込み、ログインしたユーザーだけがメモを追加できるようにします。

以下の TODO コメントの箇所にコードを書いて完成させてください。

実行手順:
cd challenge

# 問題1：User モデルと LoginManager を用意したら、
# マイグレーションで users テーブルを追加する
flask --app challenge db migrate -m "create users table"
flask --app challenge db upgrade
python challenge.py

# 問題2〜4を実装したら、ブラウザで新規登録→ログイン→メモ追加を確認
"""
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


# ============================================================
# 問題1：User モデルを定義して user_loader を登録する
# カラムは id / username / password
# set_password / check_password は werkzeug.security の
# generate_password_hash / check_password_hash を使う
# ============================================================
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    pass  # ← ここを実装


@login_manager.user_loader
def load_user(user_id):
    # TODO: User.query.get(int(user_id)) を返す
    return None


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


# ============================================================
# 問題2：新規登録ルートを実装する
# RegisterForm を使い、User を作成して保存したら /login にリダイレクトする
# ============================================================
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        # TODO: User(username=...) を作って set_password → db.session.add → commit する
        # TODO: flash() でメッセージを表示してから redirect(url_for('login')) する
        pass

    return render_template('register.html', form=form)


# ============================================================
# 問題3：ログイン・ログアウトルートを実装する
# LoginForm を使って認証し、成功したら login_user() する
# ============================================================
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        # TODO: User.query.filter_by(username=...).first() でユーザーを取得する
        # TODO: user と check_password の結果を見て login_user() → redirect(url_for('memo_list'))
        # TODO: 認証失敗時は flash() でメッセージを表示する
        pass

    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    # TODO: logout_user() を呼んで redirect(url_for('memo_list')) する
    return redirect(url_for('memo_list'))


# ============================================================
# 問題4：メモ追加ルートをログイン必須にする
# TODO: @login_required デコレーターを追加する
# ============================================================
@app.route('/memos/new', methods=['GET', 'POST'])
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
    app.run(debug=True, port=5045)
