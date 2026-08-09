import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "books.db")

conn = sqlite3.connect(DB_PATH)
cur  = conn.cursor()

# 更新前の確認
cur.execute("SELECT id, title, price FROM books WHERE id = ?", (1,))
print("更新前:", cur.fetchone())

# ---- 1件更新 ----
cur.execute(
    "UPDATE books SET price = ? WHERE id = ?",
    (2500, 1),
)
conn.commit()
print(f"更新件数: {cur.rowcount}")   # 実際に変更されたレコード数

# 更新後の確認
cur.execute("SELECT id, title, price FROM books WHERE id = ?", (1,))
print("更新後:", cur.fetchone())

# ---- 複数件更新 ----
cur.execute(
    "UPDATE books SET price = price + 100 WHERE price < ?",
    (2000,),
)
conn.commit()
print(f"\n2000円未満の本を +100 円。更新件数: {cur.rowcount}")

cur.execute("SELECT title, price FROM books")
for row in cur.fetchall():
    print(row)

conn.close()
