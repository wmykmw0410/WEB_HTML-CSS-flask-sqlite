"""
Flaskのtest_clientの基本

実行方法:
    pytest example/test_02_flask_client.py -v
"""
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

import pytest
from importlib import import_module

# ファイル名が数字始まり（02_app.py）だと import 文でそのまま書けないため、
# importlib.import_module を使う
app_module = import_module('02_app')


# ------------------------------------------------------------
# 1. client フィクスチャ — app.test_client() を毎回新しく作る
#    フィクスチャにしておくと、各テスト関数が独立したclientを使える
#
# 注意：02_app.py の TASKS はモジュールレベルのただのリストなので、
# 何もしないとテスト間で状態が共有されてしまう（あるテストで作った
# タスクが、別のテストの実行結果に紛れ込む）。autouse=True の
# フィクスチャで、各テストの前に必ずリセットしている。
# ------------------------------------------------------------
@pytest.fixture(autouse=True)
def reset_tasks():
    app_module.TASKS.clear()
    app_module.TASKS.extend([
        {'id': 1, 'title': '買い物'},
        {'id': 2, 'title': '掃除'},
    ])


@pytest.fixture
def client():
    app_module.app.config['TESTING'] = True
    return app_module.app.test_client()


# ------------------------------------------------------------
# 2. GET リクエストのテスト
# ------------------------------------------------------------
def test_index(client):
    res = client.get('/')
    assert res.status_code == 200
    assert 'タスク管理'.encode('utf-8') in res.data


def test_list_tasks(client):
    res = client.get('/tasks')
    assert res.status_code == 200
    assert res.get_json() == [
        {'id': 1, 'title': '買い物'},
        {'id': 2, 'title': '掃除'},
    ]


def test_get_task_not_found(client):
    res = client.get('/tasks/999')
    assert res.status_code == 404
    assert res.get_json() == {'detail': 'Task not found'}


# ------------------------------------------------------------
# 3. POST リクエストのテスト（json= でJSONボディを送る）
# ------------------------------------------------------------
def test_create_task(client):
    res = client.post('/tasks', json={'title': '読書'})
    assert res.status_code == 201
    assert res.get_json()['title'] == '読書'

    # 追加した結果が一覧にも反映されていることを確認する
    res2 = client.get('/tasks')
    titles = [t['title'] for t in res2.get_json()]
    assert '読書' in titles
