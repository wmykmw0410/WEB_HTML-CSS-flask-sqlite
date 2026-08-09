import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "books.db")

# ---- デフォルト（タプル）----
conn = sqlite3.connect(DB_PATH)
cur  = conn.cursor()
cur.execute("SELECT * FROM books LIMIT 2")
rows = cur.fetchall()
print("=== デフォルト（タプル）===")
for row in rows:
    print(row)              # (1, 'Python入門', '山田太郎', 2800)
    print(row[1])           # インデックスでしかアクセスできない
conn.close()

# ---- sqlite3.Row を設定（カラム名でアクセス）----
print("\n=== sqlite3.Row ===")
conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row   # カーソル作成前に設定する

cur = conn.cursor()
cur.execute("SELECT * FROM books")
rows = cur.fetchall()

for row in rows:
    print(f"id={row['id']}  タイトル={row['title']}  著者={row['author']}  価格={row['price']}円")

# keys() でカラム名一覧を取得
print("\nカラム名:", rows[0].keys())

conn.close()

# ---- Flask との関係 ----
# テンプレート（Jinja2）では {{ book.title }} のように
# 属性アクセスしたい場合が多い。
# sqlite3.Row は book['title'] も book[0] も両方使えるので
# Flask で DB を直接扱うときは row_factory の設定が推奨される。
