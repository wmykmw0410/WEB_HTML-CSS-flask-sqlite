"""
練習問題7：with conn: を使って新しい本を1件 INSERT してください
title="新しい本"、author="著者X"、genre="小説"、price=2000
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
conn.close()

print("問題7: with conn: で INSERT")
conn3 = sqlite3.connect(DB_PATH)
try:
    with conn3:
        pass  # TODO: INSERT 文を書く
    print("INSERT 成功")
except sqlite3.Error as e:
    print(f"エラー: {e}")
finally:
    conn3.close()

# 最終確認
conn4 = sqlite3.connect(DB_PATH)
conn4.row_factory = sqlite3.Row
cur4 = conn4.cursor()
cur4.execute("SELECT id, title, price FROM library ORDER BY id")
print("最終データ:")
for row in cur4.fetchall():
    print(f"  id={row['id']}  {row['title']}  {row['price']}円")
conn4.close()

# クリーンアップ
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)
