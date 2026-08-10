from flask import Blueprint, Response, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from models import Memo, db
from forms import MemoForm

memos_bp = Blueprint('memos', __name__, url_prefix='/memos')


@memos_bp.route('/')
def index() -> str:
    category = request.args.get('category')

    query = Memo.query
    if category:
        query = query.filter_by(category=category)
    memos = query.all()

    return render_template('memos/index.html', memos=memos)


@memos_bp.route('/<int:memo_id>')
def detail(memo_id: int) -> str:
    memo = Memo.query.get_or_404(memo_id)
    return render_template('memos/detail.html', memo=memo)


@memos_bp.route('/new', methods=['GET', 'POST'])
@login_required
def create() -> str | Response:
    form = MemoForm()

    if form.validate_on_submit():
        memo = Memo(
            title=form.title.data,
            category=form.category.data,
            body=form.body.data,
            due_date=form.due_date.data,
            # TODO: 問題2 user_id=current_user.id を追加して追加したユーザーを記録する
        )
        db.session.add(memo)
        db.session.commit()
        flash('メモを追加しました。')
        return redirect(url_for('memos.detail', memo_id=memo.id))

    return render_template('memos/create.html', form=form)


# ============================================================
# 問題3：メモ編集ルートを実装する
# 自分が追加したメモだけ編集できるようにする（他人のメモは404）。
# MemoForm(obj=memo) で既存の値をフォームに事前入力できる。
# ============================================================
@memos_bp.route('/<int:memo_id>/edit', methods=['GET', 'POST'])
@login_required
def update(memo_id: int) -> str | Response:
    # TODO: id だけでなく user_id も条件に入れて取得する
    #       （filter_by(id=memo_id, user_id=current_user.id).first_or_404()）
    # TODO: MemoForm(obj=memo) でフォームを作る
    # TODO: form.validate_on_submit() が成功したら、title/category/body/due_date を
    #       memo に反映してcommit()し、memos.detail にリダイレクトする
    # TODO: 上記を実装したら、下の1行は削除する
    flash('未実装です（問題3を実装してください）。')
    return redirect(url_for('memos.detail', memo_id=memo_id))


# ============================================================
# 問題4：メモ削除ルートを実装する
# 自分が追加したメモだけ削除できるようにする（他人のメモは404）。
# ============================================================
@memos_bp.route('/<int:memo_id>/delete', methods=['POST'])
@login_required
def delete(memo_id: int) -> Response:
    # TODO: id だけでなく user_id も条件に入れて取得する
    # TODO: db.session.delete(memo) → commit() し、flash してmemos.indexにリダイレクトする
    return redirect(url_for('memos.index'))
