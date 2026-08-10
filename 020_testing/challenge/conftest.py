import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(__file__))

from app import app as flask_app
from models import Memo, User, db


@pytest.fixture
def app():
    flask_app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI='sqlite:///:memory:',
        WTF_CSRF_ENABLED=False,   # テストではフォームのCSRFトークンのやり取りを省略する
    )
    with flask_app.app_context():
        db.create_all()
        yield flask_app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def sample_user(app):
    """テスト用のユーザーを1件作成する"""
    user = User(username='alice')
    user.set_password('pass1234')
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture
def sample_memo(app, sample_user):
    """sample_user が追加したメモを1件作成する"""
    memo = Memo(title='買い物リスト', category='家事', body='牛乳、卵、パン', user_id=sample_user.id)
    db.session.add(memo)
    db.session.commit()
    return memo


@pytest.fixture
def logged_in_client(client, sample_user):
    """sample_user でログイン済みの client"""
    client.post('/auth/login', data={'username': 'alice', 'password': 'pass1234'})
    return client
