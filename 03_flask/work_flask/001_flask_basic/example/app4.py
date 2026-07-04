from flask import Flask, request

# Create instance
app = Flask(__name__)


# GET only
@app.route('/items', methods=['GET'])
def get_items():
    return '<h1>GET: アイテム一覧を取得</h1>'


# POST
@app.route('/items', methods=['POST'])
def create_item():
    return '<h1>POST: アイテムを新規作成</h1>'


# PUT
@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    return f'<h1>PUT: アイテム {item_id} を更新（全体置換）</h1>'


# DELETE
@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    return f'<h1>DELETE: アイテム {item_id} を削除</h1>'


# メソッド判定の例
@app.route('/method-check', methods=['GET', 'POST', 'PUT', 'DELETE'])
def method_check():
    return f'<h1>リクエストメソッド: {request.method}</h1>'


# Run
if __name__ == '__main__':
    app.run(debug=True, port=5004)
