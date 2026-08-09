from typing import Optional
from flask import Blueprint, render_template, redirect, url_for, flash, Response
from flask_login import login_user, logout_user, login_required
from models import db, User
from forms import LoginForm, RegisterForm

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login() -> str | Response:
    form = LoginForm()
    if form.validate_on_submit():
        user: Optional[User] = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('books.index'))
        flash('ユーザー名またはパスワードが正しくありません。')
    return render_template('auth/login.html', form=form)


# ============================================================
# 問題1：最初に登録したユーザーを自動的に管理者にする
#
# RegisterForm には is_admin の項目を「あえて」含めていない。
# 誰でも登録時に管理者を名乗れてしまう（権限昇格）のを防ぐため。
# その代わり、開発初期に管理者を1人も作れないと困るので、
# 「最初の1人だけは自動的に管理者にする」というブートストラップの
# 仕組みを用意する。
# ============================================================
@auth_bp.route('/register', methods=['GET', 'POST'])
def register() -> str | Response:
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        # TODO: User.query.count() == 0 なら user.is_admin = True にする
        db.session.add(user)
        db.session.commit()
        flash('登録が完了しました。ログインしてください。')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout() -> Response:
    logout_user()
    return redirect(url_for('auth.login'))
