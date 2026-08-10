def test_memo_list_shows_title(client, sample_memo):
    """未ログインでもメモ一覧にタイトルが表示される"""
    response = client.get('/memos/')
    assert response.status_code == 200
    assert sample_memo.title.encode('utf-8') in response.data


def test_memo_detail_shows_owner(client, sample_memo, sample_user):
    """メモ詳細ページに追加したユーザー名が表示される"""
    response = client.get(f'/memos/{sample_memo.id}')
    assert response.status_code == 200
    assert sample_user.username.encode('utf-8') in response.data


def test_new_memo_requires_login(client):
    """未ログインで /memos/new にアクセスするとログイン画面にリダイレクトされる"""
    response = client.get('/memos/new', follow_redirects=True)
    assert 'ログイン'.encode('utf-8') in response.data


def test_other_user_cannot_edit_memo(client, sample_memo):
    """自分以外が追加したメモの編集ページは404になる"""
    from models import User, db

    bob = User(username='bob')
    bob.set_password('pass5678')
    db.session.add(bob)
    db.session.commit()
    client.post('/auth/login', data={'username': 'bob', 'password': 'pass5678'})

    response = client.get(f'/memos/{sample_memo.id}/edit')
    assert response.status_code == 404
