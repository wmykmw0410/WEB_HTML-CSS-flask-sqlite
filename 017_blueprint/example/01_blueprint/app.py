"""
Blueprint の基本

実行:
    python example/01_blueprint/app.py
    ブラウザで http://localhost:5000 にアクセス
"""
from flask import Flask, render_template

app = Flask(__name__)

# Blueprint を登録
from application.one.views import one_bp
from application.two.views import two_bp

app.register_blueprint(one_bp)
app.register_blueprint(two_bp)


@app.route('/')
def show_home() -> str:
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True, port=5049)
