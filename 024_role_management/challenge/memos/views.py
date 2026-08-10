from typing import Optional

import requests
from flask import Blueprint, Response, abort, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from models import Memo, db
from forms import MemoForm

memos_bp = Blueprint('memos', __name__, url_prefix='/memos')

ZIPCLOUD_URL = 'https://zipcloud.ibsnet.co.jp/api/search'


def resolve_address(postal_code: str) -> Optional[str]:
    res = requests.get(ZIPCLOUD_URL, params={'zipcode': postal_code}, timeout=5)
    data = res.json()
    if data['results'] is None:
        return None
    result = data['results'][0]
    return f"{result['address1']}{result['address2']}{result['address3']}"


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
        postal_code = form.postal_code.data
        address = None

        if postal_code:
            try:
                address = resolve_address(postal_code)
            except requests.exceptions.RequestException:
                flash('住所の取得に失敗しました。通信状況を確認してください。')
                return render_template('memos/create.html', form=form)

            if address is None:
                flash('該当する住所が見つかりませんでした。郵便番号を確認してください。')
                return render_template('memos/create.html', form=form)

        memo = Memo(
            title=form.title.data,
            category=form.category.data,
            body=form.body.data,
            due_date=form.due_date.data,
            postal_code=postal_code or None,
            address=address,
            user_id=current_user.id,   # ← 追加したユーザーを記録
        )
        db.session.add(memo)
        db.session.commit()
        flash('メモを追加しました。')
        return redirect(url_for('memos.detail', memo_id=memo.id))

    return render_template('memos/create.html', form=form)


# ============================================================
# 問題2：所有者 または 管理者だけが編集・削除できるようにする
#
# これまでは user_id で絞り込んで「他人のメモなら404」にしていたが、
# 管理者は所有者でなくても操作できる必要があるため、
# 「メモを取得する」ことと「権限があるか確認する」ことを分ける。
# ============================================================
@memos_bp.route('/<int:memo_id>/edit', methods=['GET', 'POST'])
@login_required
def update(memo_id: int) -> str | Response:
    memo: Memo = Memo.query.get_or_404(memo_id)
    # TODO: memo.user_id != current_user.id かつ current_user.is_admin でなければ
    #       abort(403) する

    form = MemoForm(obj=memo)

    if form.validate_on_submit():
        postal_code = form.postal_code.data
        address = None

        if postal_code:
            try:
                address = resolve_address(postal_code)
            except requests.exceptions.RequestException:
                flash('住所の取得に失敗しました。通信状況を確認してください。')
                return render_template('memos/update.html', form=form, memo=memo)

            if address is None:
                flash('該当する住所が見つかりませんでした。郵便番号を確認してください。')
                return render_template('memos/update.html', form=form, memo=memo)

        memo.title       = form.title.data
        memo.category    = form.category.data
        memo.body        = form.body.data
        memo.due_date    = form.due_date.data
        memo.postal_code = postal_code or None
        memo.address     = address
        db.session.commit()
        flash('メモを更新しました。')
        return redirect(url_for('memos.detail', memo_id=memo.id))

    return render_template('memos/update.html', form=form, memo=memo)


@memos_bp.route('/<int:memo_id>/delete', methods=['POST'])
@login_required
def delete(memo_id: int) -> Response:
    memo: Memo = Memo.query.get_or_404(memo_id)
    # TODO: memo.user_id != current_user.id かつ current_user.is_admin でなければ
    #       abort(403) する

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
