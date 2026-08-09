import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(__file__))

from app import app as flask_app
from models import Book, User, db


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
def sample_book(app, sample_user):
    """sample_user が追加した書籍を1件作成する"""
    book = Book(title='吾輩は猫である', author='夏目漱石', price=770, user_id=sample_user.id)
    db.session.add(book)
    db.session.commit()
    return book


@pytest.fixture
def logged_in_client(client, sample_user):
    """sample_user でログイン済みの client"""
    client.post('/auth/login', data={'username': 'alice', 'password': 'pass1234'})
    return client
