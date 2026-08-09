import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "books.db")

conn = sqlite3.connect(DB_PATH)
cur  = conn.cursor()

# ---- 1件追加（execute + プレースホルダー ?）----
# NG: f"INSERT ... VALUES ('{title}', ...)"  ← SQL インジェクションの危険
# OK: ? を使い、値は別のタプルで渡す
cur.execute(
    "INSERT INTO books (title, author, price) VALUES (?, ?, ?)",
    ("Python入門", "山田太郎", 2800),
)
print(f"1件追加。追加した id: {cur.lastrowid}")

# ---- 複数件追加（executemany）----
books_data = [
    ("Flask入門",    "鈴木花子", 3200),
    ("SQLite実践",   "佐藤次郎", 1980),
    ("Python応用",   "山田太郎", 3500),
    ("Web開発入門",  "田中一郎", 2500),
]
cur.executemany(
    "INSERT INTO books (title, author, price) VALUES (?, ?, ?)",
    books_data,
)
print(f"{len(books_data)} 件を追加。最後の id: {cur.lastrowid}")

conn.commit()
print("コミット完了")

conn.close()
