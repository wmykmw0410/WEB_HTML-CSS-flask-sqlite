def test_book_list_shows_title(client, sample_book):
    """未ログインでも書籍一覧に書籍タイトルが表示される"""
    res = client.get('/books/')
    assert res.status_code == 200
    assert sample_book.title.encode('utf-8') in res.data


def test_book_detail_shows_owner(client, sample_book, sample_user):
    """書籍詳細ページに追加したユーザー名が表示される"""
    res = client.get(f'/books/{sample_book.id}')
    assert res.status_code == 200
    assert sample_user.username.encode('utf-8') in res.data


def test_new_book_requires_login(client):
    """未ログインで /books/new にアクセスするとログイン画面にリダイレクトされる"""
    res = client.get('/books/new', follow_redirects=True)
    assert 'ログイン'.encode('utf-8') in res.data


def test_other_user_cannot_edit_book(client, sample_book):
    """自分以外が追加した書籍の編集ページは404になる"""
    from models import User, db

    bob = User(username='bob')
    bob.set_password('pass5678')
    db.session.add(bob)
    db.session.commit()
    client.post('/auth/login', data={'username': 'bob', 'password': 'pass5678'})

    res = client.get(f'/books/{sample_book.id}/edit')
    assert res.status_code == 404
