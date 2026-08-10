from flask import Blueprint, Response, jsonify, request

from models import Memo

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
