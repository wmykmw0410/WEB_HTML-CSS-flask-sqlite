"""
練習問題3：全件を fetchall で取得して1件ずつ表示してください
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "library.db")

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# 準備：library テーブルを作成してデータを入れておく
cur.execute("DROP TABLE IF EXISTS library")
cur.execute("""
    CREATE TABLE library (
        id     INTEGER PRIMARY KEY AUTOINCREMENT,
        title  TEXT    NOT NULL,
        author TEXT    NOT NULL,
        genre  TEXT,
        price  INTEGER NOT NULL
    )
""")
books_data = [
    ("Python入門",   "山田太郎", "技術",   2800),
    ("Flask開発",    "鈴木花子", "技術",   3200),
    ("料理の基本",   "田中一郎", "実用",   1500),
    ("旅行記",       "佐藤二郎", None,     1800),
    ("SQLite実践",   "山田太郎", "技術",   1980),
]
cur.executemany(
    "INSERT INTO library (title, author, genre, price) VALUES (?, ?, ?, ?)",
    books_data,
)
conn.commit()

print("問題3: 全件一覧")
# TODO: SELECT * FROM library して fetchall で表示


conn.close()

# クリーンアップ
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)
