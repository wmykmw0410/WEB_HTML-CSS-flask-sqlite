import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "books.db")

conn = sqlite3.connect(DB_PATH)
cur  = conn.cursor()

# ---- fetchall：全件取得 ----
print("=== fetchall（全件）===")
cur.execute("SELECT * FROM books")
rows = cur.fetchall()      # list[tuple]
for row in rows:
    print(row)             # (1, 'Python入門', '山田太郎', 2800)

# ---- fetchone：1件取得 ----
print("\n=== fetchone（id=1）===")
cur.execute("SELECT * FROM books WHERE id = ?", (1,))
row = cur.fetchone()       # tuple（なければ None）
if row:
    print(row)
else:
    print("見つかりませんでした")

# ---- WHERE 条件で絞り込み ----
print("\n=== WHERE price > 2000 ===")
cur.execute("SELECT title, price FROM books WHERE price > ?", (2000,))
rows = cur.fetchall()
for title, price in rows:  # タプルのアンパック
    print(f"  {title}: {price}円")

# ---- ORDER BY / LIMIT ----
print("\n=== ORDER BY price DESC LIMIT 3 ===")
cur.execute("SELECT title, price FROM books ORDER BY price DESC LIMIT 3")
rows = cur.fetchall()
for row in rows:
    print(row)

# ---- fetchmany：n 件ずつ取得 ----
print("\n=== fetchmany(2)：2件ずつ取得 ===")
cur.execute("SELECT * FROM books")
chunk = cur.fetchmany(2)
while chunk:
    print(chunk)
    chunk = cur.fetchmany(2)

conn.close()
