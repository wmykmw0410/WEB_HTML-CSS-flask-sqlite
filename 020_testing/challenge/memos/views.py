from flask import Blueprint, Response, flash, jsonify, redirect, render_template, request, url_for
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
    memos = query.order_by(Memo.is_pinned.desc(), Memo.id.desc()).all()

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
            user_id=current_user.id,   # ← 追加したユーザーを記録
        )
        db.session.add(memo)
        db.session.commit()
        flash('メモを追加しました。')
        return redirect(url_for('memos.detail', memo_id=memo.id))

    return render_template('memos/create.html', form=form)


@memos_bp.route('/<int:memo_id>/edit', methods=['GET', 'POST'])
@login_required
def update(memo_id: int) -> str | Response:
    # id だけでなく user_id も条件に入れる → 他人のメモを指定されても404
    memo: Memo = Memo.query.filter_by(id=memo_id, user_id=current_user.id).first_or_404()
    form = MemoForm(obj=memo)

    if form.validate_on_submit():
        memo.title    = form.title.data
        memo.category = form.category.data
        memo.body     = form.body.data
        memo.due_date = form.due_date.data
        db.session.commit()
        flash('メモを更新しました。')
        return redirect(url_for('memos.detail', memo_id=memo.id))

    return render_template('memos/update.html', form=form, memo=memo)


@memos_bp.route('/<int:memo_id>/delete', methods=['POST'])
@login_required
def delete(memo_id: int) -> Response:
    memo: Memo = Memo.query.filter_by(id=memo_id, user_id=current_user.id).first_or_404()
    db.session.delete(memo)
    db.session.commit()
    flash('メモを削除しました。')
    return redirect(url_for('memos.index'))


@memos_bp.route('/<int:memo_id>/toggle-pin', methods=['POST'])
@login_required
def toggle_pin(memo_id: int) -> Response:
    """
    メモのピン留めをON/OFF切り替え、JSONで結果を返す

    JavaScript側のfetch()から呼ばれるAPI用ルート。画面用のルートと違い、
    処理後にリダイレクトするのではなくjsonify()で最新の状態を返す。
    """
    memo: Memo = Memo.query.get_or_404(memo_id)
    memo.is_pinned = not memo.is_pinned
    db.session.commit()
    return jsonify({'id': memo.id, 'is_pinned': memo.is_pinned})
