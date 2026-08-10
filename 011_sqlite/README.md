# 011 Python sqlite3

Python 標準ライブラリの `sqlite3` モジュールを使って、Python から SQLite を操作する方法を学びます。

`010_sql` で学んだ SQL 命令（CREATE / INSERT / SELECT / UPDATE / DELETE）を Python コードの中から実行します。

各章は「機能の学習」と「`000_my_app`を完成させるための機能追加」の2部構成です。前者は`example/`で単体のサンプルとして学び、後者は`challenge/`でメモ帳アプリを組み立てながら取り組みます。

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
    ├── forms.py           # MemoForm（009_formsと同じ）
    ├── memos.json         # 初回起動時のシードデータ
    ├── static/
    ├── templates/
    └── answer/
        ├── challenge.py
        ├── forms.py
        ├── memos.json
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

### 動作確認：プレースホルダーがSQLインジェクションを防ぐことを確認する

```bash
python 011_sqlite/example/03_insert.py
```

| 確認する操作 | 確認したいこと |
|---|---|
| スクリプトを実行し`SELECT * FROM books`で確認する | 1件目（`Python入門`）と`executemany`で追加した2件（`Flask入門`・`SQLite実践`）、合計3件が登録されている |
| `print(f"最後に追加した id: {cur.lastrowid}")`の出力を見る | `3`と表示される（3件目に追加した`SQLite実践`のid） |
| 試しに`title`の値を`"'; DROP TABLE books; --"`のような文字列にして`?`プレースホルダー経由で`INSERT`する | エラーにならず、その**文字列がそのままtitleの値として1件追加される**だけで、テーブルは破壊されない（`?`に渡した値はSQLの一部として解釈されないため） |
| （比較用、実行非推奨）同じ値をf文字列で`f"INSERT INTO books (title, ...) VALUES ('{title}', ...)"`のように直接埋め込んで実行した場合 | `books`テーブルが削除されてしまう（SQLインジェクション）。**危険なので実際に試すのは避け、`?`を使う理由として理解するだけにとどめる** |

**正常な状態の見分け方**：どんな文字列を値として渡しても、`?`プレースホルダー経由であれば「ただのデータ」として扱われ、SQLの構造が変わることはありません。SQL文字列を`f"..."`や`+`で組み立てている箇所を見つけたら、`?`への置き換えを検討してください。

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

### 動作確認：row_factory設定の前後で取得結果の型が変わることを確認する

```bash
python 011_sqlite/example/07_row_factory.py
```

| 確認する操作 | 確認したいこと |
|---|---|
| `conn.row_factory = sqlite3.Row`を設定する**前**に`cur.fetchall()`した結果を`print()`する | `[(1, 'Python入門', '山田太郎', 2800), ...]`のような**タプルのリスト**が出力される |
| `conn.row_factory = sqlite3.Row`を設定した**後**に同じSELECTをして`print(rows[0])`する | `<sqlite3.Row object at ...>`のように表示され、タプルのまま見た目は変わらないが、`row['title']`で値を取り出せるようになる |
| `print(row['title'], row['price'])`を実行する | `Python入門 2800`のように、インデックス番号ではなくカラム名で値を取得できる |
| `print(row[0], row[1])`（`row_factory`設定後）も試す | インデックスでも引き続きアクセスでき、`row['title']`と`row[1]`が同じ値を指す（後方互換） |

**正常な状態の見分け方**：`row_factory`を設定する前は`row['title']`のようなアクセスをすると`TypeError: tuple indices must be integers`のようなエラーになります。このエラーが出た場合は、`conn.row_factory = sqlite3.Row`を**カーソル作成前**に設定しているか確認してください。

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

### 動作確認：withブロックの自動COMMIT・エラー時の挙動を確認する

```bash
python 011_sqlite/example/08_context.py
```

| 確認する操作 | 確認したいこと |
|---|---|
| スクリプトを実行後、`sqlite3 books.db "SELECT * FROM books;"`で確認する | `with sqlite3.connect(...) as conn:`ブロックの中で追加した「新刊」が**`commit()`を明示的に呼ばなくても**保存されている |
| `try / except`のブロックで、`title`を`NULL`にして`INSERT`を試す（`NOT NULL`制約に違反させる） | 例外が発生せずにプログラムが落ちる代わりに、`except sqlite3.IntegrityError as e:`で捕まえられ、「制約エラー: ...」が表示される |
| そのエラー発生後に`SELECT * FROM books`で確認する | 制約違反した行は追加されておらず、`conn.rollback()`によってそれ以前の状態が保たれている |

**正常な状態の見分け方**：`with conn:`ブロックが例外無く終わればデータは保存され、例外が起きればそのブロック内の変更は保存されません。制約違反なのにデータが保存されてしまう場合は、`except`で捕まえた後に誤って`conn.commit()`を呼んでいないか確認してください。

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

### 動作確認：各問題を実行した結果

| 問題 | 実行コマンド | 確認したいこと |
|---|---|---|
| 1 | `python question/question01.py` | エラーなく終了する。同じフォルダで`sqlite3 <対象db> ".schema library"`を実行すると定義が表示される |
| 2 | `python question/question02.py` | 実行後に全件取得すると5件のデータが入っている |
| 3 | `python question/question03.py` | 5件分のタプルが標準出力に表示される |
| 4 | `python question/question04.py` | 指定した`id`のレコード1件だけが表示される。存在しない`id`を指定すると`None`が表示される |
| 5 | `python question/question05.py` | 更新件数（`rowcount`）が`1`と表示され、該当レコードの価格が変わっている |
| 6 | `python question/question06.py` | `row['title']`のようにカラム名でアクセスした結果が表示される（タプルのインデックスではない） |
| 7 | `python question/question07.py` | `with conn:`のブロックを抜けた後、追加した行が保存されている |

**正常な状態の見分け方**：各`questionN.py`はファイル内で必要なテーブル・データを作り直してから問題に取り組む構成です。前の問題の実行結果が残っていなくても、それぞれ単独で正しい結果が出れば正常です。

---

## 10. 練習問題：メモデータをSQLiteに保存しよう

> [challenge/challenge.py](challenge/challenge.py) — 問題 ｜ [challenge/answer/challenge.py](challenge/answer/challenge.py) — 解答

### 問題：メモデータの保存先を memos.json から SQLite に変更しよう

`009_forms`で作ったメモ一覧・詳細・メモ追加フォーム・リダイレクト（`challenge/challenge.py`にすでに実装済み）は、これまで`memos.json`を`with open() + json.load()`で読み込み、Python辞書として保持していました。これを`sqlite3`モジュールで操作する`memos.db`に置き換えます。

`get_db()`（接続の取得）・`init_db()`（テーブル作成と初回シード投入）はすでに実装済みです。`memos.json`は初回起動時にだけ`memos`テーブルへ投入するために使われます。

```bash
python 011_sqlite/challenge/challenge.py
```

#### 仕様

| エンドポイント | メソッド | 処理 |
|---|---|---|
| `/` | GET | `memos`テーブルから`SELECT`する（`category`指定時は`WHERE category = ?`で絞り込み） |
| `/memos/<int:memo_id>` | GET | `WHERE id = ?`で1件`SELECT`する |
| `/memos/new` | POST（バリデーション成功時） | `with conn:`を使って`INSERT INTO memos`する |

#### ヒント

- `conn.execute(sql, params).fetchall()` / `.fetchone()`で結果を取得する（本章セクション4）
- `get_db()`は`conn.row_factory = sqlite3.Row`を設定済みなので、`row['title']`のようにカラム名でアクセスできる（セクション7）
- `dict(row)`で`sqlite3.Row`を辞書に変換できる（テンプレート側の`memo.title`のような書き方のため）
- `/memos/new`では`with conn:`のブロックの中で`conn.execute("INSERT INTO memos (...) VALUES (...)", (...))`を呼ぶ（セクション8）。`with conn:`を使うと、ブロックを正常に抜けたときに自動で`commit()`される
- 見た目やCSRFの仕組みは`009_forms`から変更不要

### 動作確認：memos.jsonからmemos.dbに置き換わっても同じ見た目で動くか

```bash
cd 011_sqlite/challenge
python challenge.py
```

| 確認する操作 | 確認したいこと |
|---|---|
| 初回起動後、フォルダに`memos.db`が作成されているか確認する | `init_db()`によって`memos.db`ファイルが新規作成され、`memos.json`の内容がシードデータとして投入されている |
| `http://127.0.0.1:5032/`にアクセスする | `memos.json`を読み込んでいた`009_forms`のときと**見た目が変わらず**メモ一覧が表示される（データの取得元がJSONからSQLiteに変わっただけ） |
| `?category=仕事`のようにカテゴリを指定してアクセスする | `WHERE category = ?`で絞り込んだ結果が表示される（`008_request`のクエリパラメータ絞り込みと同じ見た目） |
| メモ詳細ページ（`/memos/<id>`）にアクセスする | `WHERE id = ?`で1件だけ取得した内容が表示される。存在しない`id`を指定すると404になる |
| 新しいメモを`/memos/new`から追加する | 追加後、一覧に反映される。`sqlite3 memos.db "SELECT * FROM memos;"`をターミナルで実行しても、追加したメモが実際にDBに保存されていることを確認できる |
| アプリを再起動する | `memos.json`は初回起動時にしか使われないため、再起動しても`memos.json`の内容で上書きされず、DBに保存した内容がそのまま残っている |

**正常な状態の見分け方**：`009_forms`のときと画面の見た目・動作が変わらないのが正しい状態です。裏側のデータ保存先がJSONファイルからSQLiteに変わったことが、`sqlite3 memos.db`コマンドで中身を覗いたときにだけ確認できれば成功です。
