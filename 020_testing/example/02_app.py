"""
テスト対象の最小Flaskアプリ（DB不使用）

実行:
    python example/02_app.py
"""
from flask import Flask, jsonify, request

app = Flask(__name__)

TASKS = [
    {'id': 1, 'title': '買い物'},
    {'id': 2, 'title': '掃除'},
]


@app.get('/')
def index() -> str:
    return '<h1>タスク管理</h1>'


@app.get('/tasks')
def list_tasks():
    return jsonify(TASKS)


@app.get('/tasks/<int:task_id>')
def get_task(task_id: int):
    task = next((t for t in TASKS if t['id'] == task_id), None)
    if task is None:
        return jsonify({'detail': 'Task not found'}), 404
    return jsonify(task)


@app.post('/tasks')
def create_task():
    data = request.get_json()
    new_task = {'id': len(TASKS) + 1, 'title': data.get('title')}
    TASKS.append(new_task)
    return jsonify(new_task), 201


if __name__ == '__main__':
    app.run(debug=True, port=5059)
