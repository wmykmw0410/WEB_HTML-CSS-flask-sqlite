import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "books.db")

# ---- with conn: — トランザクションを自動管理 ----
# 正常終了 → 自動 COMMIT
# 例外発生 → 自動 ROLLBACK
conn = sqlite3.connect(DB_PATH)

print("=== 正常系（COMMIT）===")
try:
    with conn:   # with conn: はトランザクションのみ管理（切断はしない）
        conn.execute(
            "INSERT INTO books (title, author, price) VALUES (?, ?, ?)",
            ("新刊サンプル", "著者A", 3000),
        )
    print("INSERT 成功。COMMIT された")
except sqlite3.Error as e:
    print(f"エラー: {e}")
finally:
    conn.close()

# ---- 例外が起きたら自動 ROLLBACK ----
print("\n=== 例外発生（ROLLBACK）===")
conn2 = sqlite3.connect(DB_PATH)
try:
    with conn2:
        conn2.execute(
            "INSERT INTO books (title, author, price) VALUES (?, ?, ?)",
            ("テスト", "著者B", 999),
        )
        raise ValueError("意図的な例外")  # ← ROLLBACK されて INSERT も取り消される
except ValueError as e:
    print(f"例外をキャッチ: {e}")
except sqlite3.Error as e:
    print(f"DB エラー: {e}")
finally:
    conn2.close()

# ---- INSERT が ROLLBACK されたか確認 ----
conn3 = sqlite3.connect(DB_PATH)
conn3.row_factory = sqlite3.Row
cur = conn3.cursor()
cur.execute("SELECT * FROM books WHERE title IN ('新刊サンプル', 'テスト')")
rows = cur.fetchall()
titles_found = [row['title'] for row in rows]
print("\n確認:")
print(f"  '新刊サンプル' → {'存在する（COMMIT 済み）' if '新刊サンプル' in titles_found else '存在しない'}")
print(f"  'テスト'       → {'存在する' if 'テスト' in titles_found else '存在しない（ROLLBACK で取り消された）'}")
conn3.close()
