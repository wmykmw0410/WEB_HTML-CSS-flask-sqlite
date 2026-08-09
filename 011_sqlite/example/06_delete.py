import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "books.db")

conn = sqlite3.connect(DB_PATH)
cur  = conn.cursor()

# 削除前の確認
cur.execute("SELECT * FROM books")
print("削除前:")
for row in cur.fetchall():
    print(" ", row)

# ---- 1件削除 ----
cur.execute("DELETE FROM books WHERE id = ?", (5,))
conn.commit()
print(f"\nid=5 を削除。削除件数: {cur.rowcount}")

# ---- 条件で複数削除 ----
cur.execute("DELETE FROM books WHERE price < ?", (2000,))
conn.commit()
print(f"2000円未満を削除。削除件数: {cur.rowcount}")

# 削除後の確認
cur.execute("SELECT * FROM books")
print("\n削除後:")
for row in cur.fetchall():
    print(" ", row)

conn.close()
