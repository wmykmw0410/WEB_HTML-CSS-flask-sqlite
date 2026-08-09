import sqlite3

# ファイルを指定（なければ自動で作成される）
conn = sqlite3.connect("books.db")

# カーソルを作成（SQL を実行する窓口）
cur = conn.cursor()

print(f"接続成功")
print(f"SQLite バージョン: {sqlite3.sqlite_version}")

# 切断
conn.close()
print("接続を閉じました")

# ---- メモリ上の DB（ファイルを作らない）----
print("\n--- :memory: ---")
conn_mem = sqlite3.connect(":memory:")
print("メモリ DB 接続成功（プロセス終了で消える）")
conn_mem.close()
