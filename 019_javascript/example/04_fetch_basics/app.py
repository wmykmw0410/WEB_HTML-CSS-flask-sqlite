"""
fetch()の基本：ページを再読み込みせずにサーバーとJSONをやり取りする

実行方法: python app.py
"""
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

items = [
    {"id": 1, "name": "コーヒー", "liked": False},
    {"id": 2, "name": "紅茶", "liked": True},
    {"id": 3, "name": "ジュース", "liked": False},
]


@app.route('/')
def index():
    return render_template('index.html', items=items)


@app.route('/api/items/<int:item_id>/toggle-like', methods=['POST'])
def toggle_like(item_id):
    item = next((i for i in items if i['id'] == item_id), None)
    if item is None:
        return jsonify({'detail': 'item not found'}), 404

    item['liked'] = not item['liked']
    return jsonify(item)


if __name__ == '__main__':
    app.run(debug=True, port=5073)
