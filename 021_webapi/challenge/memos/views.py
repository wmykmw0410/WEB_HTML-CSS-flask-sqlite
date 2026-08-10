from typing import Optional

import requests
from flask import Blueprint, Response, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from models import Memo, db
from forms import MemoForm

memos_bp = Blueprint('memos', __name__, url_prefix='/memos')

ZIPCLOUD_URL = 'https://zipcloud.ibsnet.co.jp/api/search'


# ============================================================
# 問題1：郵便番号から住所を取得する
# zipcloud APIを GET で呼び出し、該当住所があればその文字列を、
# 無ければ None を返す。
# タイムアウトを指定すること（021_webapiセクション4）。
# ============================================================
def resolve_address(postal_code: str) -> Optional[str]:
    # TODO: requests.get(ZIPCLOUD_URL, params={'zipcode': postal_code}, timeout=...) を呼ぶ
    # TODO: res.json() の 'results' が None でなければ、
    #       address1 + address2 + address3 を連結した文字列を返す
    # TODO: 'results' が None なら None を返す
    return None


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


# ============================================================
# 問題2・問題3：郵便番号から住所を解決してからメモを保存する
# フォームから postal_code を受け取り、指定されていれば resolve_address() を呼ぶ。
#
# 問題2：住所が見つかった場合は Memo の address に保存する
# 問題3：以下の場合はエラーメッセージを出してフォーム画面に戻す
#        （メモは作成しない。postal_code が未入力の場合は何もせず保存する）
#          - 該当住所が見つからない場合（resolve_address が None を返す）
#          - zipcloud への通信が失敗した場合
#            （requests.exceptions.RequestException：ConnectionError・Timeoutを含む）
# ============================================================
@memos_bp.route('/new', methods=['GET', 'POST'])
@login_required
def create() -> str | Response:
    form = MemoForm()

    if form.validate_on_submit():
        postal_code = form.postal_code.data
        address = None

        # TODO: postal_code が指定されていたら resolve_address(postal_code) を呼ぶ。
        #       requests.exceptions.RequestException が発生したら
        #       flash してフォーム画面（create.html）を再描画する
        # TODO: 住所が None（該当なし）なら flash してフォーム画面を再描画する

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


@memos_bp.route('/<int:memo_id>/edit', methods=['GET', 'POST'])
@login_required
def update(memo_id: int) -> str | Response:
    # id だけでなく user_id も条件に入れる → 他人のメモを指定されても404
    memo: Memo = Memo.query.filter_by(id=memo_id, user_id=current_user.id).first_or_404()
    form = MemoForm(obj=memo)

    if form.validate_on_submit():
        postal_code = form.postal_code.data
        address = memo.address

        # TODO: postal_code が変更されていたら resolve_address(postal_code) を呼び直す
        #       （問題2・3と同じ処理。postal_code が空なら address も None にする）

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
