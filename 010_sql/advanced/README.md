# 応用 — SELECT応用・ALTER TABLE・トランザクション・バックアップ

`basic/` を終えた後に進んでください。

## 目次

1. [SELECT 応用](#1-select-応用) — IN / BETWEEN / IS NULL
2. [ALTER TABLE](#2-alter-table) — テーブルの変更
3. [トランザクション](#3-トランザクション) — BEGIN / COMMIT / ROLLBACK
4. [バックアップ](#4-バックアップ) — .dump / .backup / ファイルコピー
5. [練習問題](#5-練習問題)

## フォルダ構成

```
advanced/
├── README.md
├── example/
│   ├── 01_select_advanced.sql  SELECT 応用（IN / BETWEEN / IS NULL）
│   ├── 02_alter.sql            ALTER TABLE
│   └── 03_transaction.sql      トランザクション
└── question/                   練習問題（1問1ファイル）
    ├── setup.sql                共通セットアップ（productsテーブル作成・データ投入）
    ├── question01.sql〜question06.sql
    └── answer/
        └── answer01.sql〜answer06.sql
```

---

## 1. SELECT 応用

> [example/01_select_advanced.sql](example/01_select_advanced.sql)

`basic/` で学んだ WHERE 演算子の追加パターンです。

### WHERE 演算子の追加

| 演算子 | 意味 | 例 |
|---|---|---|
| `IN (値1, 値2, ...)` | いずれかに一致 | `WHERE author IN ('山田太郎', '鈴木花子')` |
| `BETWEEN A AND B` | 範囲内（A 以上 B 以下） | `WHERE price BETWEEN 2000 AND 3500` |
| `IS NULL` | NULL である | `WHERE price IS NULL` |
| `IS NOT NULL` | NULL でない | `WHERE price IS NOT NULL` |

```sql
-- IN
SELECT * FROM books WHERE author IN ('山田太郎', '鈴木花子');

-- BETWEEN
SELECT * FROM books WHERE price BETWEEN 2000 AND 3500;

-- IS NULL / IS NOT NULL
SELECT * FROM books WHERE price IS NULL;
SELECT * FROM books WHERE price IS NOT NULL;
```

### 練習問題

1. 著者が '山田太郎' または '鈴木花子' の本を `IN` で取得してください
2. `price` が 2000 以上 3500 以下の本を `BETWEEN` で取得してください
3. `price` が NULL の本を `IS NULL` で取得してください

---

## 2. ALTER TABLE

> [example/02_alter.sql](example/02_alter.sql)

既存のテーブルにカラムを追加します。

```sql
-- カラムを追加
ALTER TABLE books ADD COLUMN publisher TEXT;

-- デフォルト値を指定して追加
ALTER TABLE books ADD COLUMN in_stock INTEGER DEFAULT 1;
```

> **注意**: SQLite の `ALTER TABLE` は `ADD COLUMN`（カラムの追加）のみサポートします。カラム名の変更や削除は SQLite では直接できません。

### 練習問題

`products` テーブルに `description` カラム（`TEXT`）を追加してください。
`.schema products` で定義を確認してください。

---

## 3. トランザクション

> [example/03_transaction.sql](example/03_transaction.sql)

複数の SQL 命令をひとまとまりとして扱い、全て成功したときだけ確定します。途中でエラーが起きた場合は全て取り消せます。

| 命令 | 役割 |
|---|---|
| `BEGIN` | トランザクション開始 |
| `COMMIT` | 変更を確定して保存 |
| `ROLLBACK` | 変更を全て取り消す |

```sql
BEGIN;

INSERT INTO books (title, author, price) VALUES ('新刊A', '山田太郎', 2000);
INSERT INTO books (title, author, price) VALUES ('新刊B', '鈴木花子', 2500);

COMMIT;   -- ここで初めてデータが確定する
```

```sql
BEGIN;

DELETE FROM books WHERE id = 1;

ROLLBACK;  -- BEGIN 以降の変更がすべて取り消される
```

**トランザクションが必要な場面**

- 複数テーブルを同時に更新する（両方成功しないと意味がない）
- 大量データの一括 INSERT（速度向上にも効果あり）
- 誤操作のリスクが高い UPDATE / DELETE の前の安全網として

### 練習問題

1. `BEGIN` / `COMMIT` を使って、2件の INSERT をひとまとまりで確定してください
2. `BEGIN` の後に `DELETE FROM books WHERE id = 1;` を実行し、`ROLLBACK` で取り消してください

---

## 4. バックアップ

データベースファイルを保全する方法は3通りあります。

### .dump — SQL テキストとして出力

```bash
sqlite3 books.db .dump > books_backup.sql
```

**復元**

```bash
sqlite3 books_new.db < books_backup.sql
```

### .backup — バイナリコピー

```sql
sqlite> .backup books_backup.db
```

### ファイルをコピー

```bash
cp books.db books_backup.db
```

> **注意**: 書き込み中にコピーするとデータが壊れる可能性があります。必ずアプリを停止するか `.backup` コマンドを使ってください。

| 方法 | 特徴 |
|---|---|
| `.dump` | SQL テキストで出力。可読性が高く、他の DB への移行にも使える |
| `.backup` | バイナリコピー。高速。CLI 実行中でも使える |
| ファイルコピー | シンプル。DB 停止中のみ安全 |

### 練習問題

1. `.dump` を使って `books.db` を `books_backup.sql` に保存してください
2. `books_backup.sql` から `books_restore.db` として復元し、`.tables` と `SELECT * FROM books;` で内容を確認してください

---

## 5. 練習問題

> [question/](question/) — 問題（1問1ファイル） ｜ [question/answer/](question/answer/) — 解答

### 問題：商品テーブルを操作しよう

`question/questionN.sql` を開き、コメントの指示に従って SQL を完成させてください。まず `setup.sql` で共通のテーブルとデータを用意してから、同じセッションの中で各問題を実行します（問題同士は独立しているので、実行順序は自由です）。

```bash
sqlite3 products.db
sqlite> .read advanced/question/setup.sql
sqlite> .read advanced/question/question01.sql
```

#### テーブル仕様（products）

| カラム名 | 型 | 制約 |
|---|---|---|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT |
| `name` | TEXT | NOT NULL |
| `price` | INTEGER | NOT NULL |
| `category` | TEXT | |
| `stock` | INTEGER | |

#### 問題一覧

| 問題 | 内容 | 使う構文 | 解答 |
|---|---|---|---|
| 1 | 特定カテゴリの商品を取得 | IN | [question/answer/answer01.sql](question/answer/answer01.sql) |
| 2 | 価格帯で絞り込み | BETWEEN | [question/answer/answer02.sql](question/answer/answer02.sql) |
| 3 | 在庫未登録の商品を取得 | IS NULL | [question/answer/answer03.sql](question/answer/answer03.sql) |
| 4 | カラムを追加 | ALTER TABLE | [question/answer/answer04.sql](question/answer/answer04.sql) |
| 5 | 複数件をまとめて追加 | BEGIN / COMMIT | [question/answer/answer05.sql](question/answer/answer05.sql) |
| 6 | 削除を取り消す | BEGIN / ROLLBACK | [question/answer/answer06.sql](question/answer/answer06.sql) |
