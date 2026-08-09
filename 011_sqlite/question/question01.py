"""
練習問題1：テーブルを作成してください

テーブル名: library
カラム:
  id      INTEGER  PRIMARY KEY AUTOINCREMENT
  title   TEXT     NOT NULL
  author  TEXT     NOT NULL
  genre   TEXT
  price   INTEGER  NOT NULL
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "library.db")

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS library")

# TODO: CREATE TABLE 文を書いてください
cur.execute("""

""")
conn.commit()
print("問題1: テーブル作成完了")

conn.close()

# クリーンアップ
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)
