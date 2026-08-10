from flask import Blueprint, Response, flash, redirect, render_template, url_for
from flask_login import login_user, logout_user, login_required

from models import db, User
from forms import RegisterForm, LoginForm

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register() -> str | Response:
    """
    新規ユーザーを登録する

    フォームのバリデーションに成功したら User を作成してパスワードを
    ハッシュ化して保存し、ログインページにリダイレクトする。
    それ以外は登録フォームを再表示する。

    Returns:
        リダイレクト先の Response、またはフォームを表示する HTML 文字列
    """
    form = RegisterForm()

    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('登録が完了しました。ログインしてください。')
        return redirect(url_for('auth.login'))

    return render_template('register.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login() -> str | Response:
    """
    ユーザー名とパスワードでログインする

    該当ユーザーが存在し、かつパスワードが一致すればログイン状態にして
    メモ一覧にリダイレクトする。それ以外はエラーメッセージ付きで
    ログインフォームを再表示する。

    Returns:
        リダイレクト先の Response、またはフォームを表示する HTML 文字列
    """
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash(f'ようこそ、{user.username} さん！')
            return redirect(url_for('memos.memo_list'))
        flash('ユーザー名またはパスワードが正しくありません。')

    return render_template('login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout() -> Response:
    logout_user()
    flash('ログアウトしました。')
    return redirect(url_for('memos.memo_list'))
