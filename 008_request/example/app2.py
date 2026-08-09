from flask import Flask, request, jsonify

app = Flask(__name__)

# 書籍データ（本来は DB から取得する想定）
books = [
    {"id": "1", "title": "python", "category": "technical"},
    {"id": "2", "title": "はじめてのプログラミング", "category": "technical"},
    {"id": "3", "title": "進撃の巨人", "category": "comics"},
    {"id": "4", "title": "DBおやじ", "category": "comics"},
    {"id": "5", "title": "週刊ダイヤモンド", "category": "magazine"},
    {"id": "6", "title": "ザ・社長", "category": "magazine"},
]

# クエリパラメータ category で絞り込み。未指定なら全件返す
@app.route('/books/')
def get_books():
    category = request.args.get('category')

    if category is None:
        result = books
    else:
        result = [book for book in books if book["category"] == category]

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5019)
