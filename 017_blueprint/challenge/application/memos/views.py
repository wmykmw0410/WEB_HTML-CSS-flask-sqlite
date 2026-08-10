from flask import Blueprint, Response, redirect, render_template, request, url_for
from flask_login import login_required

from models import db, Memo
from forms import MemoForm

memos_bp = Blueprint('memos', __name__)


@memos_bp.route('/')
def memo_list() -> str:
    category = request.args.get('category')

    query = Memo.query
    if category:
        query = query.filter_by(category=category)
    memos = query.all()

    return render_template('top.html', memos=memos)


@memos_bp.route('/memos/<int:memo_id>')
def memo_detail(memo_id: int) -> str:
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


@memos_bp.route('/memos/new', methods=['GET', 'POST'])
@login_required
def new_memo() -> str | Response:
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

        # TODO: 問題2 'memo_list' を Blueprint 形式のエンドポイント名に書き換える
        return redirect(url_for('memo_list'))

    return render_template('new_memo.html', form=form)


@memos_bp.route('/old-memos')
def old_memos() -> Response:
    # TODO: 問題2 'memo_list' を Blueprint 形式のエンドポイント名に書き換える
    return redirect(url_for('memo_list'))
