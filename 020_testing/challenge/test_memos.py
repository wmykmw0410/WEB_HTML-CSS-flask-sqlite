"""
練習問題：メモ関連のルートにテストを書こう

以下の TODO コメントの箇所にコードを書いて、テストを完成させてください。
（`pytest.fail(...)` の行は目印です。実装できたら削除してください。
 何も書かずに `pass` のままにすると、アサーションが1つも実行されず
 テストが「成功」してしまう点に注意してください。）

実行方法: pytest test_memos.py -v
"""
import pytest


def test_memo_list_shows_title(client, sample_memo):
    """未ログインでもメモ一覧にタイトルが表示される"""
    # TODO: client.get('/memos/') でレスポンスを取得する
    # TODO: ステータスコードが200であることを確認する
    # TODO: sample_memo.title がレスポンス本文（response.data）に含まれることを確認する
    #       文字列はエンコードしてから比較する: sample_memo.title.encode('utf-8')
    pytest.fail('TODO: 実装してください')


def test_memo_detail_shows_owner(client, sample_memo, sample_user):
    """メモ詳細ページに追加したユーザー名が表示される"""
    # TODO: client.get(f'/memos/{sample_memo.id}') でレスポンスを取得する
    # TODO: ステータスコードが200であることを確認する
    # TODO: sample_user.username がレスポンス本文に含まれることを確認する
    pytest.fail('TODO: 実装してください')


def test_new_memo_requires_login(client):
    """未ログインで /memos/new にアクセスするとログイン画面にリダイレクトされる"""
    # TODO: client.get('/memos/new', follow_redirects=True) でレスポンスを取得する
    # TODO: 'ログイン' という文字列がレスポンス本文に含まれることを確認する
    #       （login_manager.login_view の設定によりログイン画面に転送される）
    pytest.fail('TODO: 実装してください')


def test_other_user_cannot_edit_memo(client, sample_memo):
    """自分以外が追加したメモの編集ページは404になる"""
    from models import User, db

    # bob という別のユーザーを作ってログインする
    bob = User(username='bob')
    bob.set_password('pass5678')
    db.session.add(bob)
    db.session.commit()
    client.post('/auth/login', data={'username': 'bob', 'password': 'pass5678'})

    # TODO: client.get(f'/memos/{sample_memo.id}/edit') でレスポンスを取得する
    # TODO: ステータスコードが404であることを確認する
    pytest.fail('TODO: 実装してください')
