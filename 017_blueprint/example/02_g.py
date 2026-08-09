"""
Flask g オブジェクト — リクエスト内でデータを共有する

実行:
    python example/02_g.py
    ブラウザで http://localhost:5000 / /morning / /evening にアクセス
"""
from flask import Flask, g

app = Flask(__name__)


def get_user() -> dict[str, str | int]:
    return {'name': 'Tom', 'age': 20, 'email': 'tom@example.com'}


@app.before_request
def before_request() -> None:
    g.user = get_user()   # リクエスト開始時に一度だけ呼ばれる


@app.route('/')
def do_hello() -> str:
    return f'Hello, {g.user["name"]}'


@app.route('/morning')
def do_morning() -> str:
    return f'Good morning, {g.user["name"]}'


@app.route('/evening')
def do_evening() -> str:
    return f'Good evening, {g.user["name"]}'


if __name__ == '__main__':
    app.run(debug=True, port=5050)
