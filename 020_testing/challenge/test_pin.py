"""
練習問題：ピン留め機能（JSON API）のテストを書こう

019_javascriptで追加した /memos/<id>/toggle-pin は、画面ではなくJSONを返す
ルートです。以下の TODO コメントの箇所にコードを書いて、テストを完成させてください。
（`pytest.fail(...)` の行は目印です。実装できたら削除してください。
 何も書かずに `pass` のままにすると、アサーションが1つも実行されず
 テストが「成功」してしまう点に注意してください。）

実行方法: pytest test_pin.py -v
"""
import pytest


def test_toggle_pin_requires_login(client, sample_memo):
    """未ログインで toggle-pin にアクセスするとログイン画面にリダイレクトされる"""
    # TODO: client.post(f'/memos/{sample_memo.id}/toggle-pin') でレスポンスを取得する
    # TODO: ステータスコードが302（リダイレクト）であることを確認する
    pytest.fail('TODO: 実装してください')


def test_toggle_pin_flips_state(logged_in_client, sample_memo):
    """toggle-pinを呼ぶと is_pinned が反転し、JSONで返ってくる"""
    # sample_memo.is_pinned は作成直後は False
    # TODO: logged_in_client.post(f'/memos/{sample_memo.id}/toggle-pin') でレスポンスを取得する
    # TODO: ステータスコードが200であることを確認する
    # TODO: response.get_json() の 'is_pinned' が True であることを確認する
    pytest.fail('TODO: 実装してください')


def test_toggle_pin_twice_returns_to_original(logged_in_client, sample_memo):
    """toggle-pinを2回呼ぶと元の状態（False）に戻る"""
    logged_in_client.post(f'/memos/{sample_memo.id}/toggle-pin')   # 1回目：True になる

    # TODO: もう一度 toggle-pin を呼ぶ
    # TODO: response.get_json() の 'is_pinned' が False であることを確認する
    pytest.fail('TODO: 実装してください')


def test_pinned_memo_appears_first(logged_in_client, sample_memo, app):
    """ピン留めしたメモが一覧の先頭に表示される"""
    from models import Memo, db

    # sample_memo とは別の、後から作られたメモ（通常なら一覧の先頭に来る）
    other = Memo(title='あとから追加したメモ', category='仕事', body='本文', user_id=sample_memo.user_id)
    db.session.add(other)
    db.session.commit()

    # sample_memo（先に作られた方）をピン留めする
    logged_in_client.post(f'/memos/{sample_memo.id}/toggle-pin')

    # TODO: logged_in_client.get('/memos/') でメモ一覧を取得する
    # TODO: レスポンス本文（文字列にデコードしたもの）の中で、
    #       sample_memo.title が other.title より前に出現することを確認する
    #       ヒント: text.find(sample_memo.title) < text.find(other.title)
    pytest.fail('TODO: 実装してください')
