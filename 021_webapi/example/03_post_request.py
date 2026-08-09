import requests

url: str = "https://jsonplaceholder.typicode.com/posts"

payload: dict[str, str | int] = {
    "title": "Flask学習",
    "body": "requestsモジュールでPOSTする例",
    "userId": 1,
}

# json= を使うと、辞書を自動でJSON文字列に変換し
# Content-Type: application/json も自動で付与してくれる
res: requests.Response = requests.post(url, json=payload)

print("status_code:", res.status_code)   # 201 Created
print("response:", res.json())
