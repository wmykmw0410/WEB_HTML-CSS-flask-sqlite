import json
import os

base_dir = os.path.dirname(__file__)
path     = os.path.join(base_dir, 'data.json')

# ---- dict → JSON ファイルに書き込む（json.dump）----
print("=== json.dump（ファイルに書き込む）===")
data = {
    'name':   '山田太郎',
    'age':    30,
    'skills': ['Python', 'Flask', 'SQLite'],
    'address': {'city': '東京', 'zip': '100-0001'},
}
with open(path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
    # ensure_ascii=False : 日本語をそのまま出力（True だと 山... になる）
    # indent=2           : 読みやすいようにインデント

with open(path, encoding='utf-8') as f:
    print(f.read())

# ---- JSON ファイル → dict に読み込む（json.load）----
print("=== json.load（ファイルから読み込む）===")
with open(path, encoding='utf-8') as f:
    loaded = json.load(f)

print(f"name   : {loaded['name']}")
print(f"skills : {loaded['skills']}")
print(f"city   : {loaded['address']['city']}")

# ---- dict ↔ JSON 文字列（ファイルを介さない変換）----
print("\n=== json.dumps / json.loads（文字列と dict の変換）===")

# dict → JSON 文字列
json_str = json.dumps(data, ensure_ascii=False)
print("json.dumps:", json_str[:50], '...')

# JSON 文字列 → dict
parsed = json.loads(json_str)
print("json.loads:", parsed['name'])

# クリーンアップ
os.remove(path)
