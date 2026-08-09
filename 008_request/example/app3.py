from flask import Flask, jsonify

app = Flask(__name__)

# ユーザーデータ（本来は DB から取得する想定）
users = {
    1: "Tom",
    2: "Ken",
    3: "John",
}

# パスパラメータでユーザーを1件取得。存在しなければ404
@app.route('/users/<int:user_id>')
def get_user(user_id):
    username = users.get(user_id)

    if username is None:
        return jsonify({"detail": "User not found"}), 404

    return jsonify({"user_id": user_id, "username": username})

if __name__ == '__main__':
    app.run(debug=True, port=5020)
