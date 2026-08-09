import requests

# 1. 接続エラー(存在しないドメインなど)
try:
    requests.get("https://this-domain-does-not-exist-abc123xyz.com", timeout=3)
except requests.exceptions.ConnectionError:
    print("接続エラーが発生しました")

# 2. ステータスコードが400/500番台でも例外は起きない
res: requests.Response = requests.get("https://jsonplaceholder.typicode.com/posts/99999")
print("status_code:", res.status_code)  # 404

# raise_for_status() を呼ぶと、400/500番台のときだけ例外を送出してくれる
try:
    res.raise_for_status()
except requests.exceptions.HTTPError as e:
    print("HTTPエラーが発生しました:", e)

# 3. タイムアウトの指定(応答が遅いサーバーへの対策)
try:
    requests.get("https://jsonplaceholder.typicode.com/posts", timeout=0.001)
except requests.exceptions.Timeout:
    print("タイムアウトしました")
