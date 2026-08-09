import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "books.db")

conn = sqlite3.connect(DB_PATH)
cur  = conn.cursor()

# 既存テーブルを削除してから作り直す（クリーンな状態で実行できるように）
cur.execute("DROP TABLE IF EXISTS books")

cur.execute("""
    CREATE TABLE books (
        id     INTEGER PRIMARY KEY AUTOINCREMENT,
        title  TEXT    NOT NULL,
        author TEXT    NOT NULL,
        price  INTEGER NOT NULL
    )
""")

conn.commit()
print("テーブル 'books' を作成しました")

# .schema 相当：sqlite_master からスキーマを確認
cur.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='books'")
schema = cur.fetchone()
print(f"\nスキーマ:\n{schema[0]}")

conn.close()
