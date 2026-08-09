# 011 Python sqlite3

Python 標準ライブラリの `sqlite3` モジュールを使って、Python から SQLite を操作する方法を学びます。

`010_sql` で学んだ SQL 命令（CREATE / INSERT / SELECT / UPDATE / DELETE）を Python コードの中から実行します。

各章は「機能の学習」と「`000_my_app`を完成させるための機能追加」の2部構成です。前者は`example/`で単体のサンプルとして学び、後者は`challenge/`で`100_bookstore_api`を完成形の参考にしながら取り組みます。

## 前提

- 010_sql の `basic/` を一通り終えていること
- Python 3.x がインストール済みであること

## フォルダ構成

```
011_sqlite/
├── README.md
├── example/
│   ├── 01_connect.py      接続・カーソル・切断
│   ├── 02_create.py       テーブル作成（CREATE TABLE）
│   ├── 03_insert.py       データ追加（execute / executemany）
│   ├── 04_select.py       データ取得（fetchall / fetchone）
│   ├── 05_update.py       データ更新（UPDATE / rowcount）
│   ├── 06_delete.py       データ削除（DELETE / rowcount）
│   ├── 07_row_factory.py  辞書形式での取得（row_factory）
│   └── 08_context.py      コンテキストマネージャー（with 文）
├── question/              練習問題（1問1ファイル）
│   ├── question01.py〜question07.py
│   └── answer/
│       └── answer01.py〜answer07.py
└── challenge/             # 009_formsの続き（000_my_appに組み込む機能の追加分）
    ├── challenge.py
    ├── forms.py           # BookForm（009_formsと同じ）
    ├── books.json         # 初回起動時のシードデータ
    ├── static/
    ├── templates/
    └── answer/
        ├── challenge.py
        ├── forms.py
        ├── books.json
        ├── static/
        └── templates/
```

---

## sqlite3 モジュールとは

`sqlite3` は Python に**最初から組み込まれている**標準ライブラリです。追加のインストールは不要です。

```python
import sqlite3  # これだけで使える
```

### 010 CLI との違い

| | 010（CLI） | 011（Python） |
|---|---|---|
| 操作方法 | ターミナルで `sqlite3` を起動して対話的に SQL を入力 | Python コードの中で SQL 文字列を渡して実行 |
| 用途 | 手動での確認・データ整備 | アプリケーションからの自動操作 |
| Flask との関係 | — | Flask アプリから DB を操作する基礎になる |

---

## 1. 接続とカーソル

> [example/01_connect.py](example/01_connect.py)

```python
import sqlite3

conn = sqlite3.connect('books.db')  # books.db がなければ自動作成
cur  = conn.cursor()                # カーソル（命令の窓口）を作成

print(sqlite3.sqlite_version)       # SQLite のバージョンを確認

conn.close()                        # 必ず閉じる
```

### 用語

| 用語 | 役割 |
|---|---|
| `conn`（Connection） | DB ファイルへの接続。変更を確定（commit）したり切断（close）する |
| `cur`（Cursor） | SQL を実行する窓口。`execute()` や `fetchall()` はカーソルを通して行う |

### `:memory:` — メモリ上の DB

```python
conn = sqlite3.connect(':memory:')  # ファイルを作らず、メモリ上に一時 DB を作る
```

- プロセス終了と同時にデータが消える
- テストやプロトタイプに便利

---

## 2. テーブル作成

> [example/02_create.py](example/02_create.py)

```python
cur.execute("""
    CREATE TABLE IF NOT EXISTS books (
        id     INTEGER PRIMARY KEY AUTOINCREMENT,
        title  TEXT    NOT NULL,
        author TEXT    NOT NULL,
        price  INTEGER NOT NULL
    )
""")
conn.commit()
```

### ポイント

- SQL 文は `cur.execute()` に文字列として渡す
- DDL（CREATE / DROP）の後も **`conn.commit()`** を呼ぶ
- `CREATE TABLE IF NOT EXISTS` — テーブルが既にあってもエラーにならない

---

## 3. データ追加

> [example/03_insert.py](example/03_insert.py)

### プレースホルダー `?`

SQL 文字列に値を直接埋め込むと **SQL インジェクション** の危険があります。
`?` を使い、値は別に渡すのが正しい書き方です。

```python
# 1件追加
cur.execute(
    "INSERT INTO books (title, author, price) VALUES (?, ?, ?)",
    ('Python入門', '山田太郎', 2800)   # タプルで渡す
)

# 複数件まとめて追加
books_data = [
    ('Flask入門',  '鈴木花子', 3200),
    ('SQLite実践', '佐藤次郎', 1980),
]
cur.executemany(
    "INSERT INTO books (title, author, price) VALUES (?, ?, ?)",
    books_data
)

conn.commit()
print(f"最後に追加した id: {cur.lastrowid}")
```

| メソッド | 用途 |
|---|---|
| `cur.execute(sql, params)` | 1件の SQL を実行 |
| `cur.executemany(sql, data)` | 同じ SQL を複数回まとめて実行 |
| `cur.lastrowid` | 最後に INSERT したレコードの id |

---

## 4. データ取得

> [example/04_select.py](example/04_select.py)

```python
# 全件取得
cur.execute("SELECT * FROM books")
rows = cur.fetchall()     # → [(1, 'Python入門', '山田太郎', 2800), ...]

# 1件取得
cur.execute("SELECT * FROM books WHERE id = ?", (1,))
row = cur.fetchone()      # → (1, 'Python入門', '山田太郎', 2800)

# 条件で絞り込み
cur.execute("SELECT * FROM books WHERE price > ?", (2000,))
rows = cur.fetchall()
for row in rows:
    print(row)
```

| メソッド | 戻り値 | 用途 |
|---|---|---|
| `cur.fetchall()` | `list[tuple]` | 全件取得 |
| `cur.fetchone()` | `tuple` または `None` | 1件取得。なければ `None` |
| `cur.fetchmany(n)` | `list[tuple]` | 最大 n 件取得 |

---

## 5. データ更新

> [example/05_update.py](example/05_update.py)

```python
cur.execute(
    "UPDATE books SET price = ? WHERE id = ?",
    (2500, 1)
)
conn.commit()
print(f"更新件数: {cur.rowcount}")  # 実際に変更されたレコード数
```

- `cur.rowcount` — 直前の `execute()` で変更されたレコード数

---

## 6. データ削除

> [example/06_delete.py](example/06_delete.py)

```python
cur.execute("DELETE FROM books WHERE id = ?", (3,))
conn.commit()
print(f"削除件数: {cur.rowcount}")
```

---

## 7. 辞書形式での取得（row_factory）

> [example/07_row_factory.py](example/07_row_factory.py)

デフォルトでは取得した行は**タプル** `(1, 'Python入門', ...)` です。
`conn.row_factory` を設定するとカラム名でアクセスできるようになります。

```python
conn.row_factory = sqlite3.Row   # 接続直後に設定（カーソル作成前）

cur = conn.cursor()
cur.execute("SELECT * FROM books")
rows = cur.fetchall()

for row in rows:
    print(row['title'], row['price'])  # カラム名でアクセス
    # row[0], row[1] でもアクセス可能（後方互換あり）
```

### Flask との関係

Flask のテンプレートで `{{ book.title }}` のように辞書アクセスしたい場合に必須です。

---

## 8. コンテキストマネージャー（with 文）

> [example/08_context.py](example/08_context.py)

`with conn:` を使うとトランザクション管理が簡単になります。

```python
with sqlite3.connect('books.db') as conn:
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO books (title, author, price) VALUES (?, ?, ?)",
        ('新刊', '著者名', 3000)
    )
    # ブロックを正常終了 → 自動 COMMIT
    # 例外が発生      → 自動 ROLLBACK

conn.close()  # with 文はトランザクションのみ管理。切断は明示的に行う
```

### `try / except` でのエラーハンドリング

```python
try:
    cur.execute("INSERT INTO books (title, author, price) VALUES (?, ?, ?)",
                ('重複タイトル', '著者', 3000))
    conn.commit()
except sqlite3.IntegrityError as e:
    print(f"制約エラー: {e}")
    conn.rollback()
finally:
    conn.close()
```

| 例外クラス | 発生する場面 |
|---|---|
| `sqlite3.IntegrityError` | NOT NULL / UNIQUE 制約違反 |
| `sqlite3.OperationalError` | テーブルが存在しない、SQL 構文エラーなど |
| `sqlite3.Error` | 上記すべての親クラス |

---

## 9. 練習問題

> [question/](question/) — 問題（1問1ファイル） ｜ [question/answer/](question/answer/) — 解答

### 問題：図書管理システムを作ろう

`question/questionN.py` を開き、コメントの指示に従って Python コードを完成させてください。各ファイルは独立して実行できるように、必要なテーブル・データをファイル内で作り直してから、そのファイル自身の問題に取り組む構成になっています。

```bash
python 011_sqlite/question/question01.py
```

#### テーブル仕様（library）

| カラム名 | 型 | 制約 |
|---|---|---|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT |
| `title` | TEXT | NOT NULL |
| `author` | TEXT | NOT NULL |
| `genre` | TEXT | |
| `price` | INTEGER | NOT NULL |

#### 問題一覧

| 問題 | 内容 | 使うメソッド | 解答 |
|---|---|---|---|
| 1 | テーブルを作成する | `execute()` / `commit()` | [question/answer/answer01.py](question/answer/answer01.py) |
| 2 | 5件まとめてデータを追加する | `executemany()` | [question/answer/answer02.py](question/answer/answer02.py) |
| 3 | 全件取得して表示する | `fetchall()` | [question/answer/answer03.py](question/answer/answer03.py) |
| 4 | 特定 id のレコードを1件取得する | `fetchone()` | [question/answer/answer04.py](question/answer/answer04.py) |
| 5 | 価格を更新し `rowcount` を表示する | `rowcount` | [question/answer/answer05.py](question/answer/answer05.py) |
| 6 | `row_factory` で辞書形式に変換する | `row_factory` | [question/answer/answer06.py](question/answer/answer06.py) |
| 7 | `with conn:` で安全に INSERT する | コンテキストマネージャー | [question/answer/answer07.py](question/answer/answer07.py) |

---

## 10. 練習問題：書籍データをSQLiteに保存しよう

> [challenge/challenge.py](challenge/challenge.py) — 問題 ｜ [challenge/answer/challenge.py](challenge/answer/challenge.py) — 解答

### 問題：書籍データの保存先を books.json から SQLite に変更しよう

`009_forms`で作った書籍一覧・詳細・書籍追加フォーム・リダイレクト（`challenge/challenge.py`にすでに実装済み）は、これまで`books.json`を`with open() + json.load()`で読み込み、Python辞書として保持していました。これを`sqlite3`モジュールで操作する`books.db`に置き換えます。

`get_db()`（接続の取得）・`init_db()`（テーブル作成と初回シード投入）はすでに実装済みです。`books.json`は初回起動時にだけ`books`テーブルへ投入するために使われます。

```bash
python 011_sqlite/challenge/challenge.py
```

#### 仕様

| エンドポイント | メソッド | 処理 |
|---|---|---|
| `/` | GET | `books`テーブルから`SELECT`する（`author`指定時は`WHERE author = ?`で絞り込み） |
| `/books/<int:book_id>` | GET | `WHERE id = ?`で1件`SELECT`する |
| `/books/new` | POST（バリデーション成功時） | `with conn:`を使って`INSERT INTO books`する |

#### ヒント

- `conn.execute(sql, params).fetchall()` / `.fetchone()`で結果を取得する（本章セクション4）
- `get_db()`は`conn.row_factory = sqlite3.Row`を設定済みなので、`row['title']`のようにカラム名でアクセスできる（セクション7）
- `dict(row)`で`sqlite3.Row`を辞書に変換できる（テンプレート側の`book.title`のような書き方のため）
- `/books/new`では`with conn:`のブロックの中で`conn.execute("INSERT INTO books (...) VALUES (...)", (...))`を呼ぶ（セクション8）。`with conn:`を使うと、ブロックを正常に抜けたときに自動で`commit()`される
- 見た目やCSRF・ファイルアップロードの仕組みは`009_forms`から変更不要
