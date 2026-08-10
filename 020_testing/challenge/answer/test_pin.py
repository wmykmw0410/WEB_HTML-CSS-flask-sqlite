def test_toggle_pin_requires_login(client, sample_memo):
    """未ログインで toggle-pin にアクセスするとログイン画面にリダイレクトされる"""
    response = client.post(f'/memos/{sample_memo.id}/toggle-pin')
    assert response.status_code == 302


def test_toggle_pin_flips_state(logged_in_client, sample_memo):
    """toggle-pinを呼ぶと is_pinned が反転し、JSONで返ってくる"""
    response = logged_in_client.post(f'/memos/{sample_memo.id}/toggle-pin')
    assert response.status_code == 200
    assert response.get_json()['is_pinned'] is True


def test_toggle_pin_twice_returns_to_original(logged_in_client, sample_memo):
    """toggle-pinを2回呼ぶと元の状態（False）に戻る"""
    logged_in_client.post(f'/memos/{sample_memo.id}/toggle-pin')

    response = logged_in_client.post(f'/memos/{sample_memo.id}/toggle-pin')
    assert response.get_json()['is_pinned'] is False


def test_pinned_memo_appears_first(logged_in_client, sample_memo, app):
    """ピン留めしたメモが一覧の先頭に表示される"""
    from models import Memo, db

    other = Memo(title='あとから追加したメモ', category='仕事', body='本文', user_id=sample_memo.user_id)
    db.session.add(other)
    db.session.commit()

    logged_in_client.post(f'/memos/{sample_memo.id}/toggle-pin')

    response = logged_in_client.get('/memos/')
    text = response.get_data(as_text=True)
    assert text.find(sample_memo.title) < text.find(other.title)
