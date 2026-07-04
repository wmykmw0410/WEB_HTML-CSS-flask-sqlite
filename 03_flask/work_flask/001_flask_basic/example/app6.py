from flask import Flask, abort

# Create instance
app = Flask(__name__)


# Top Page
@app.route('/')
def index():
    return '<h1>Top Page</h1>'


# abort : 意図的にエラーを発生させる
@app.route('/admin')
def admin():
    abort(403)


# 404 エラーハンドラ
@app.errorhandler(404)
def not_found(e):
    return '<h1>404 - ページが見つかりません</h1>', 404


# 403 エラーハンドラ
@app.errorhandler(403)
def forbidden(e):
    return '<h1>403 - アクセス権限がありません</h1>', 403


# 500 エラーハンドラ
@app.errorhandler(500)
def internal_server_error(e):
    return '<h1>500 - サーバーエラーが発生しました</h1>', 500


# Run
if __name__ == '__main__':
    app.run(debug=True, port=5006)
