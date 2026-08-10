"""
書籍APIのフルCRUD化（サンプルアプリ）

実行:
python example/app.py
"""
from flask import Flask
from api.views import api_bp

app = Flask(__name__)
app.register_blueprint(api_bp)


if __name__ == '__main__':
    app.run(debug=True, port=5067)
