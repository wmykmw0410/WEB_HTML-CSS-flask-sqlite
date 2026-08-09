import requests

url: str = "https://jsonplaceholder.typicode.com/posts/1"
res: requests.Response = requests.get(url)

print("status_code:", res.status_code)          # 200
print("ok:", res.ok)                            # 200番台ならTrue
print("headers:", res.headers["Content-Type"])  # レスポンスヘッダーを辞書のように参照
print("text:", res.text[:50], "...")            # 文字列としての本文
print("json:", res.json())                      # json.loads(res.text) と同じ結果を得るショートカット
