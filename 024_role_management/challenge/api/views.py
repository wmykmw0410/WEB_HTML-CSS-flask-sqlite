from typing import Optional

from flask import Blueprint, Response, jsonify, request
from flask_login import current_user

from models import Memo, db

api_bp = Blueprint('api', __name__, url_prefix='/api')


def memo_to_dict(memo: Memo) -> dict[str, int | str | bool | None]:
    return {
        'id':          memo.id,
        'title':       memo.title,
        'category':    memo.category,
        'body':        memo.body,
        'due_date':    memo.due_date,
        'is_pinned':   memo.is_pinned,
        'owner':       memo.owner.username,
    }


def validate_memo_payload(data: dict) -> Optional[str]:
    """必須項目が欠けていればエラーメッセージを、問題なければ None を返す"""
    if not data.get('title'):
        return 'title is required'
    if not data.get('category'):
        return 'category is required'
    if not data.get('body'):
        return 'body is required'
    return None


@api_bp.get('/memos')
def list_memos() -> Response:
    category = request.args.get('category')

    query = Memo.query
    if category:
        query = query.filter_by(category=category)
    memos = query.all()

    return jsonify([memo_to_dict(m) for m in memos])


@api_bp.get('/memos/<int:memo_id>')
def get_memo(memo_id: int) -> tuple[Response, int] | Response:
    memo = Memo.query.get(memo_id)
    if memo is None:
        return jsonify({'detail': 'Memo not found'}), 404
    return jsonify(memo_to_dict(memo))


@api_bp.post('/memos')
def create_memo() -> tuple[Response, int]:
    if not current_user.is_authenticated:
        return jsonify({'detail': 'Login required'}), 401

    data: dict = request.get_json()
    error = validate_memo_payload(data)
    if error:
        return jsonify({'detail': error}), 400

    memo = Memo(
        title=data['title'],
        category=data['category'],
        body=data['body'],
        due_date=data.get('due_date'),
        user_id=current_user.id,
    )
    db.session.add(memo)
    db.session.commit()
    return jsonify(memo_to_dict(memo)), 201


# ============================================================
# 問題3：所有者 または 管理者だけが更新・削除できるようにする
# ============================================================
@api_bp.put('/memos/<int:memo_id>')
def update_memo(memo_id: int) -> tuple[Response, int] | Response:
    if not current_user.is_authenticated:
        return jsonify({'detail': 'Login required'}), 401

    memo = Memo.query.get(memo_id)
    if memo is None:
        return jsonify({'detail': 'Memo not found'}), 404
    # TODO: memo.user_id != current_user.id かつ current_user.is_admin でなければ
    #       jsonify({'detail': 'Forbidden'}), 403 を返す

    data: dict = request.get_json()
    error = validate_memo_payload(data)
    if error:
        return jsonify({'detail': error}), 400

    memo.title = data['title']
    memo.category = data['category']
    memo.body = data['body']
    memo.due_date = data.get('due_date')
    db.session.commit()
    return jsonify(memo_to_dict(memo))


@api_bp.delete('/memos/<int:memo_id>')
def delete_memo(memo_id: int) -> tuple[str, int] | tuple[Response, int]:
    if not current_user.is_authenticated:
        return jsonify({'detail': 'Login required'}), 401

    memo = Memo.query.get(memo_id)
    if memo is None:
        return jsonify({'detail': 'Memo not found'}), 404
    # TODO: memo.user_id != current_user.id かつ current_user.is_admin でなければ
    #       jsonify({'detail': 'Forbidden'}), 403 を返す

    db.session.delete(memo)
    db.session.commit()
    return '', 204
