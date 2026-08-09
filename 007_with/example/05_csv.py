import csv
import os

base_dir = os.path.dirname(__file__)
path     = os.path.join(base_dir, 'items.csv')

# ---- 書き込み ----
print("=== CSV 書き込み ===")
with open(path, 'w', encoding='utf-8', newline='') as f:
    # newline='' を指定しないと Windows で改行が二重になる
    writer = csv.writer(f)
    writer.writerow(['id', 'name', 'price'])        # ヘッダー行
    writer.writerows([                               # 複数行をまとめて書き込む
        [1, 'りんご',   150],
        [2, 'バナナ',   120],
        [3, 'みかん',    80],
        [4, 'ぶどう',   300],
    ])
print(f"{path} を作成しました")

# ---- 読み込み（リスト形式）----
print("\n=== csv.reader（リスト形式）===")
with open(path, encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)   # ['id', 'name', 'price'] / ['1', 'りんご', '150'] ...

# ---- 読み込み（辞書形式）----
print("\n=== csv.DictReader（辞書形式）===")
with open(path, encoding='utf-8') as f:
    reader = csv.DictReader(f)  # 1行目をヘッダーとして自動認識
    for row in reader:
        print(f"  id={row['id']}  {row['name']}  {row['price']}円")

# ---- 書き込み（辞書形式）----
print("\n=== csv.DictWriter（辞書形式）===")
path2   = os.path.join(base_dir, 'items2.csv')
fields  = ['id', 'name', 'price']
records = [
    {'id': 1, 'name': 'コーヒー', 'price': 200},
    {'id': 2, 'name': '紅茶',     'price': 180},
]
with open(path2, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()       # ヘッダー行を書き込む
    writer.writerows(records)

with open(path2, encoding='utf-8') as f:
    print(f.read())

# クリーンアップ
os.remove(path)
os.remove(path2)
