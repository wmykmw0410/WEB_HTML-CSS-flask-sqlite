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


# ============================================================
# 問題1：メモ一覧をJSONで返す
# memos.index と同様、?category= が指定されていれば絞り込む
# ============================================================
@api_bp.get('/memos')
def list_memos() -> Response:
    # TODO: Memo.query を使って memos を取得する（?category= があれば filter_by）
    # TODO: memo_to_dict() で変換したリストを jsonify() で返す
    return jsonify([])


# ============================================================
# 問題2：メモを1件JSONで返す
# 見つからなければ {"detail": "Memo not found"} を404で返す
# ============================================================
@api_bp.get('/memos/<int:memo_id>')
def get_memo(memo_id: int) -> tuple[Response, int] | Response:
    # TODO: Memo.query.get(memo_id) で取得する
    # TODO: None なら jsonify({'detail': 'Memo not found'}), 404 を返す
    # TODO: 見つかれば jsonify(memo_to_dict(memo)) を返す
    return jsonify({'detail': 'Memo not found'}), 404
