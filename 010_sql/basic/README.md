# 基礎 — CRUD 基本操作

Flask で簡単な EC サイトを作るために必要な SQL の基本を学びます。

## 目次

1. [SQLite CLI の使い方](#1-sqlite-cli-の使い方) — 起動・メタコマンド・基本操作
2. [CREATE TABLE](#2-create-table) — テーブルの定義
3. [INSERT](#3-insert) — データの追加
4. [SELECT](#4-select) — データの取得・集計
5. [UPDATE](#5-update) — データの更新
6. [DELETE](#6-delete) — データの削除
7. [テーブルの結合（JOIN）](#7-テーブルの結合join) — INNER JOIN / LEFT JOIN
8. [データファイルへの出力](#8-データファイルへの出力) — CSV / JSON
9. [練習問題](#9-練習問題)

## フォルダ構成

```
basic/
├── README.md
├── example/
│   ├── 01_create.sql   CREATE TABLE
│   ├── 02_insert.sql   INSERT
│   ├── 03_select.sql   SELECT（条件・並び替え・集計・DISTINCT・GROUP BY）
│   ├── 04_update.sql   UPDATE
│   ├── 05_delete.sql   DELETE
│   ├── 06_join.sql     JOIN（テーブルの結合）
│   └── 07_output.sql   データファイルへの出力
└── question/           練習問題（1問1ファイル）
    ├── question01.sql〜question06.sql
    └── answer/
        └── answer01.sql〜answer06.sql
```

---

## 1. SQLite CLI の使い方

### 起動と終了

```bash
# DB ファイルを指定して起動（なければ新規作成）
sqlite3 books.db

# 終了
sqlite> .quit
```

### .sql ファイルをまとめて実行

```bash
sqlite3 books.db < 01_create.sql
```

### CLI 内でファイルを読み込む

```sql
sqlite> .read 01_create.sql
```

### メタコマンド一覧

| コマンド | 説明 |
|---|---|
| `.tables` | テーブル一覧を表示 |
| `.schema テーブル名` | テーブルの定義を表示 |
| `.headers on` | SELECT 結果にカラム名を表示 |
| `.mode column` | 結果を列幅で整形して表示 |
| `.read ファイル名` | SQL ファイルを読み込んで実行 |
| `.quit` | 終了 |

### 見やすくするおすすめ設定

```sql
.headers on
.mode column
```

### 練習問題

1. `shop.db` という名前の DB ファイルを作成して CLI を起動してください
2. `.headers on` と `.mode column` を設定してください
3. `.tables` を実行してテーブル一覧を確認してください（まだ何も表示されない）
4. `.quit` で終了してください

---

## 2. CREATE TABLE

> [example/01_create.sql](example/01_create.sql)

テーブルの構造（カラム名・データ型・制約）を定義します。

```sql
CREATE TABLE IF NOT EXISTS books (
    id     INTEGER PRIMARY KEY AUTOINCREMENT,
    title  TEXT    NOT NULL,
    author TEXT    NOT NULL,
    price  INTEGER
);
```

### データ型

| 型 | 説明 | 使いどころ | 例 |
|---|---|---|---|
| `INTEGER` | 整数 | ID・数量・年齢など | `1`, `42`, `-5` |
| `TEXT` | 文字列（長さ制限なし） | 名前・タイトル・メールアドレスなど | `'Python入門'` |
| `REAL` | 浮動小数点数 | 価格（小数あり）・評価値など | `3.14`, `99.9` |
| `BLOB` | バイナリデータ | 画像・ファイルの生データ | — |

**DATE 型について**

SQLite には `DATE` 型が存在しません。日付は `TEXT` で ISO 8601 形式（`'YYYY-MM-DD'`）を使うのが一般的です。

```sql
CREATE TABLE events (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    title      TEXT NOT NULL,
    event_date TEXT,                          -- 'YYYY-MM-DD'
    created_at TEXT DEFAULT (date('now'))     -- 今日の日付を自動入力
);
```

### 制約

| 制約 | 説明 | 使いどころ |
|---|---|---|
| `PRIMARY KEY` | 主キー。重複・NULL 不可 | 必ず `id` カラムに設定する |
| `AUTOINCREMENT` | INSERT のたびに自動で採番（1, 2, 3, ...） | `PRIMARY KEY` と組み合わせて使う |
| `NOT NULL` | NULL（未入力）を禁止 | 必須入力のカラムに設定する |
| `UNIQUE` | 重複した値を禁止 | メールアドレス・ユーザー名など |
| `DEFAULT 値` | 値を省略したときに使われるデフォルト値 | `created_at` に現在日付など |
| `CHECK (条件)` | 指定した条件を満たさない値を禁止 | `price >= 0`（負の価格を禁止）など |

```sql
CREATE TABLE IF NOT EXISTS users (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    name       TEXT    NOT NULL,
    email      TEXT    NOT NULL UNIQUE,
    age        INTEGER CHECK (age >= 0),
    role       TEXT    DEFAULT 'user',
    created_at TEXT    DEFAULT (date('now'))
);
```

### テーブルの削除

```sql
DROP TABLE IF EXISTS books;
```

### 練習問題

以下の仕様で `products` テーブルを作成してください。

| カラム名 | 型 | 制約 |
|---|---|---|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT |
| `name` | TEXT | NOT NULL |
| `price` | INTEGER | CHECK (price >= 0) |
| `category` | TEXT | DEFAULT 'その他' |

作成後、`.schema products` で定義を確認してください。

### 動作確認：制約が実際に効いているか

```bash
sqlite3 practice.db
```

| 確認する操作 | 確認したいこと |
|---|---|
| `.schema products` | 各カラムの型・`NOT NULL`・`CHECK`・`DEFAULT`が定義通りに表示される |
| `INSERT INTO products (name, price) VALUES ('ノート', 100);` | 成功する。`category`を指定していないので`DEFAULT`の`'その他'`が入る |
| `SELECT * FROM products;` | 追加した行の`category`が`その他`になっている |
| `INSERT INTO products (price) VALUES (100);`（`name`を省略） | `NOT NULL constraint failed: products.name`というエラーになる |
| `INSERT INTO products (name, price) VALUES ('赤字商品', -100);` | `CHECK constraint failed: products`というエラーになり、追加されない |

**正常な状態の見分け方**：制約に違反する`INSERT`は必ずエラーメッセージが表示されて**追加されない**のが正しい状態です。エラーが出ずに追加できてしまう場合は、`CREATE TABLE`の制約の書き方（`NOT NULL`や`CHECK`のスペルミスなど）を疑ってください。

---

## 3. INSERT

> [example/02_insert.sql](example/02_insert.sql)

テーブルにデータを追加します。

```sql
-- 1件追加
INSERT INTO books (title, author, price) VALUES ('Python入門', '山田太郎', 2800);

-- 複数件追加（1 文ずつ書く）
INSERT INTO books (title, author, price) VALUES ('Flask入門',  '鈴木花子', 3200);
INSERT INTO books (title, author, price) VALUES ('SQLite実践', '佐藤次郎', 1980);
```

### ポイント

- カラム名と VALUES の順番・数が一致している必要がある
- `AUTOINCREMENT` の `id` は省略すると自動で採番される
- 文字列は `'` シングルクォートで囲む

### 練習問題

セクション 2 で作成した `products` テーブルに以下の4件を INSERT してください。

| name | price | category |
|---|---|---|
| リンゴ | 150 | 果物 |
| バナナ | 200 | 果物 |
| にんじん | 100 | 野菜 |
| キャベツ | 250 | 野菜 |

INSERT 後に `SELECT * FROM products;` で確認してください。

---

## 4. SELECT

> [example/03_select.sql](example/03_select.sql)

テーブルからデータを取得します。

### 句の記載順

```sql
SELECT   カラム名
FROM     テーブル名
WHERE    条件
GROUP BY グループ化するカラム
HAVING   グループに対する条件
ORDER BY カラム名 ASC|DESC
LIMIT    件数;
```

| 句 | 役割 | 省略 |
|---|---|---|
| `SELECT` | 取得するカラムを指定 | 不可 |
| `FROM` | 対象テーブルを指定 | 不可 |
| `WHERE` | 絞り込み条件（GROUP BY 前） | 可（省略で全件） |
| `GROUP BY` | グループ化 | 可 |
| `HAVING` | グループに対する条件（GROUP BY 後） | 可 |
| `ORDER BY` | 並び替え | 可 |
| `LIMIT` | 取得件数の上限 | 可 |

### 基本

```sql
SELECT * FROM books;
SELECT title, price FROM books;
```

### DISTINCT — 重複を除外

```sql
SELECT DISTINCT author FROM books;
```

### WHERE — 絞り込み

```sql
SELECT * FROM books WHERE price > 2500;
SELECT * FROM books WHERE price >= 2000 AND price <= 3500;
SELECT * FROM books WHERE author = '山田太郎' OR author = '鈴木花子';

-- LIKE：部分一致（% は任意の文字列）
SELECT * FROM books WHERE title LIKE '%入門%';
```

### ORDER BY — 並び替え

```sql
SELECT * FROM books ORDER BY price ASC;   -- 昇順
SELECT * FROM books ORDER BY price DESC;  -- 降順
```

### LIMIT — 件数制限

```sql
SELECT * FROM books ORDER BY price DESC LIMIT 3;
```

### 集計関数

```sql
SELECT COUNT(*) AS 件数 FROM books;
SELECT AVG(price) AS 平均 FROM books;
SELECT MAX(price) AS 最高 FROM books;
SELECT MIN(price) AS 最低 FROM books;
SELECT SUM(price) AS 合計 FROM books;
```

### GROUP BY — グループ集計

カラムの値でレコードをグループ化し、グループごとに集計できます。

```sql
SELECT author, COUNT(*) AS 件数       FROM books GROUP BY author;
SELECT author, AVG(price) AS 平均価格  FROM books GROUP BY author;
```

### HAVING — グループに対する条件

`WHERE` は個々のレコードへの条件、`HAVING` は `GROUP BY` 後のグループへの条件です。

```sql
SELECT author, COUNT(*) AS 件数
FROM books
GROUP BY author
HAVING COUNT(*) >= 2;
```

| 句 | 対象 | タイミング |
|---|---|---|
| `WHERE` | 個々のレコード | GROUP BY の**前**に絞り込む |
| `HAVING` | グループ集計結果 | GROUP BY の**後**に絞り込む |

### WHERE の演算子まとめ

| 演算子 | 意味 | 例 |
|---|---|---|
| `=` | 等しい | `WHERE id = 1` |
| `!=` | 等しくない | `WHERE price != 0` |
| `>` / `<` | より大きい / 小さい | `WHERE price > 2000` |
| `>=` / `<=` | 以上 / 以下 | `WHERE price >= 2000` |
| `AND` | かつ | `WHERE price > 2000 AND price < 4000` |
| `OR` | または | `WHERE author = 'A' OR author = 'B'` |
| `LIKE '%text%'` | 部分一致 | `WHERE title LIKE '%入門%'` |

### 練習問題

`books` テーブル（id / title / author / price）を対象に以下を書いてください。

1. `price` が 2500 以上の本を取得してください
2. タイトルに「入門」を含む本を `price` の昇順で取得してください
3. 著者の一覧を重複なしで取得してください（DISTINCT）
4. 著者ごとの書籍数を取得してください（GROUP BY）
5. 書籍数が 2 件以上の著者だけ取得してください（HAVING）

### 動作確認：クエリの結果件数で正しさを判断する

`example/02_insert.sql`まで実行済み（6件のデータが入っている状態）であることを前提にした、各問題の期待結果です。

| 問題 | 実行するSQL | 確認したいこと |
|---|---|---|
| 1 | `SELECT * FROM books WHERE price >= 2500;` | **4件**取得できる（Python入門2800・Flask入門3200・データベース設計4500・Python応用3500） |
| 2 | `SELECT * FROM books WHERE title LIKE '%入門%' ORDER BY price ASC;` | **3件**、価格の低い順（HTML & CSS入門2200 → Python入門2800 → Flask入門3200）に並ぶ |
| 3 | `SELECT DISTINCT author FROM books;` | **5件**（山田太郎は2冊登録されているが、DISTINCTにより1回だけ表示される） |
| 4 | `SELECT author, COUNT(*) FROM books GROUP BY author;` | **5行**、山田太郎の行だけ`COUNT(*)`が`2`、他は`1` |
| 5 | `SELECT author, COUNT(*) FROM books GROUP BY author HAVING COUNT(*) >= 2;` | **1件**（山田太郎のみ）。問題4の結果から2冊以上の著者だけに絞り込まれている |

**正常な状態の見分け方**：件数が期待と違う場合、`WHERE`と`HAVING`を取り違えている（`HAVING`はGROUP BY後の集計結果にしか使えない）か、`LIKE`のワイルドカード`%`の位置を間違えている可能性が高いです。

---

## 5. UPDATE

> [example/04_update.sql](example/04_update.sql)

既存のデータを更新します。

```sql
UPDATE books SET price = 2500 WHERE id = 1;
UPDATE books SET title = 'Python完全入門', price = 3000 WHERE id = 1;
```

**WHERE を忘れると全件が更新されます。** 実行前に SELECT で対象を確認する習慣をつけましょう。

```sql
SELECT * FROM books WHERE id = 1;
UPDATE books SET price = 2500 WHERE id = 1;
```

### 練習問題

1. id が 2 の本の `price` を 3500 に更新してください（先に SELECT で確認すること）
2. `price` が 2000 未満の本の `price` を一律 2000 に更新してください

---

## 6. DELETE

> [example/05_delete.sql](example/05_delete.sql)

データを削除します。

```sql
DELETE FROM books WHERE id = 5;
DELETE FROM books WHERE price < 2000;
```

**WHERE を忘れると全件が削除されます。** 実行前に SELECT で確認しましょう。

```sql
SELECT * FROM books WHERE price < 2000;
DELETE FROM books WHERE price < 2000;
```

### 練習問題

1. id が 3 のレコードを削除してください（先に SELECT で確認すること）
2. `price` が 3000 を超えるレコードを全て削除してください

---

## 7. テーブルの結合（JOIN）

> [example/06_join.sql](example/06_join.sql)

複数のテーブルを関連するカラムで結合して、まとめて取得します。

### 外部キー（FOREIGN KEY）

**外部キー**は、別テーブルの主キーを参照するカラムです。

```sql
CREATE TABLE authors (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    name    TEXT NOT NULL
);

CREATE TABLE books (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    title     TEXT NOT NULL,
    author_id INTEGER,
    price     INTEGER,
    FOREIGN KEY (author_id) REFERENCES authors(id)
);
```

SQLite はデフォルトで外部キー制約を**無効**にしています。有効にするには起動後に以下を実行します。

```sql
PRAGMA foreign_keys = ON;
```

### なぜ結合が必要か

1つのテーブルに全データを詰め込むと同じ値が重複します。テーブルを分けて `id` で関連付けると重複をなくせます。

```
authors テーブル          books テーブル
| id | name   | country | | id | title      | author_id | price |
|----|--------|---------|  |----|------------|-----------|-------|
|  1 | 山田太郎 | 日本   |  |  1 | Python入門  |     1     |  2800 |
|  2 | 鈴木花子 | 日本   |  |  2 | Flask入門   |     2     |  3200 |
                           |  3 | SQLite実践  |     1     |  1980 |
```

### INNER JOIN — 両方に一致するレコードだけ取得

```sql
SELECT books.title, authors.name AS author, books.price
FROM books
INNER JOIN authors ON books.author_id = authors.id;
```

`author_id` が NULL のレコードは結果に**含まれません**。

### LEFT JOIN — 左テーブルの全件 + 一致する右テーブルの値

```sql
SELECT books.title, authors.name AS author, books.price
FROM books
LEFT JOIN authors ON books.author_id = authors.id;
```

`author_id` が NULL のレコードも結果に含まれ、著者列は `NULL` になります。

### テーブル名を別名（AS）で短縮

```sql
SELECT b.title, a.name AS author, b.price
FROM books AS b
INNER JOIN authors AS a ON b.author_id = a.id
ORDER BY b.price DESC;
```

| JOIN の種類 | 結果に含まれるレコード |
|---|---|
| `INNER JOIN` | 両テーブルに一致するレコードのみ |
| `LEFT JOIN` | 左テーブルの全件（右に一致なければ `NULL`） |

### 練習問題

`06_join.sql` の `authors`（id / name / country）と `books`（id / title / author_id / price）テーブルを使ってください。

1. INNER JOIN で書籍タイトルと著者名・国を一覧表示してください
2. LEFT JOIN で著者不明の本も含めて表示し、著者列が NULL になることを確認してください
3. INNER JOIN と GROUP BY を組み合わせて、著者ごとの書籍数と平均価格を取得してください

### 動作確認：INNER JOINとLEFT JOINで件数が変わることを確認する

`06_join.sql`は`books`に4件（うち1件は`author_id`が`NULL`の「著者不明の本」）、`authors`に3件のデータを用意しています。

```bash
sqlite3 join.db < example/06_join.sql
```

| 確認する操作 | 確認したいこと |
|---|---|
| 1つ目のSELECT（INNER JOIN）の結果件数を数える | **3件**（「著者不明の本」は`author_id`が`NULL`で`authors`側に一致するレコードが無いため、結果から除外される） |
| 2つ目のSELECT（LEFT JOIN）の結果件数を数える | **4件**（`books`の全件が含まれる）。「著者不明の本」の行だけ`author`と`country`が`NULL`（表示上は空欄）になっている |
| 3つ目のSELECT（別名 AS + ORDER BY）の結果を見る | `INNER JOIN`なので3件のみ、価格の高い順（Flask Webアプリ開発3200 → Python入門2800 → SQLite実践1980）に並ぶ |

**正常な状態の見分け方**：`INNER JOIN`と`LEFT JOIN`で件数が同じになってしまう場合、そもそも結合条件に一致しないレコード（今回は「著者不明の本」）が無いデータで試している可能性があります。件数の差（3件 vs 4件）こそが2つのJOINの違いです。

---

## 8. データファイルへの出力

> [example/07_output.sql](example/07_output.sql)

SELECT 結果をファイルに書き出します。`.mode` で形式を、`.output` で出力先を指定します。

### CSV ファイルへ出力

```sql
.mode csv
.headers on
.output result.csv
SELECT * FROM books;
.output stdout
.mode column
```

### JSON ファイルへ出力

```sql
.mode json
.output result.json
SELECT * FROM books;
.output stdout
.mode column
```

### シェルから直接出力

```bash
sqlite3 -csv -header books.db "SELECT * FROM books;" > result.csv
sqlite3 -json books.db "SELECT * FROM books;" > result.json
```

### 練習問題

1. `books` テーブルの全データを `books_export.csv` として出力してください
2. `books` テーブルの全データを `books_export.json` として出力してください

---

## 9. 練習問題

> [question/](question/) — 問題（1問1ファイル） ｜ [question/answer/](question/answer/) — 解答

### 問題：メンバー管理テーブルを操作しよう

`question/questionN.sql` を開き、コメントの指示に従って SQL を完成させてください。問題1〜5は同じ`members`テーブルを使うため、1つの`sqlite3`セッションの中で番号順に実行します。

```bash
sqlite3 practice.db
sqlite> .read basic/question/question01.sql
sqlite> .read basic/question/question02.sql
sqlite> .read basic/question/question03.sql
sqlite> .read basic/question/question04.sql
sqlite> .read basic/question/question05.sql
```

#### テーブル仕様（members）

| カラム名 | 型 | 制約 |
|---|---|---|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT |
| `name` | TEXT | NOT NULL |
| `department` | TEXT | NOT NULL |
| `salary` | INTEGER | |

#### 問題一覧

| 問題 | 内容 | 解答 |
|---|---|---|
| 1 | `members` テーブルを作成する | [question/answer/answer01.sql](question/answer/answer01.sql) |
| 2 | 5件のデータを INSERT する | [question/answer/answer02.sql](question/answer/answer02.sql) |
| 3 | SELECT で一覧・部署絞り込み・salary 降順・平均・DISTINCT・GROUP BY・HAVING を取得する | [question/answer/answer03.sql](question/answer/answer03.sql) |
| 4 | 特定メンバーの salary を UPDATE する | [question/answer/answer04.sql](question/answer/answer04.sql) |
| 5 | 条件に一致するメンバーを DELETE する | [question/answer/answer05.sql](question/answer/answer05.sql) |
| 6 | `example/06_join.sql`のデータに対してJOINクエリを書く | [question/answer/answer06.sql](question/answer/answer06.sql) |

問題6は`example/06_join.sql`で作成する別のデータベース（`join.db`）を使います。詳しくは[question/question06.sql](question/question06.sql)を参照してください。

### 動作確認：各問題の期待件数・期待値

| 問題 | 確認する操作 | 確認したいこと |
|---|---|---|
| 1 | `.schema members` | `id`・`name`・`department`・`salary`の4カラムが定義通りに表示される |
| 2 | `SELECT * FROM members;` | 5件のデータが登録されている |
| 3-(2) | 開発部のメンバーを取得 | **2件**（山田太郎・佐藤次郎） |
| 3-(3) | salaryが300000以上、降順 | **4件**、佐藤次郎(400000)→山田太郎(350000)→鈴木花子(320000)→伊藤四郎(310000)の順（田中三郎の280000は含まれない） |
| 3-(4) | 平均salaryを取得 | `332000`（5人の合計1,660,000円 ÷ 5人） |
| 3-(6) | 部署ごとの人数と平均salary | 開発部=2人・平均375000、営業部=2人・平均315000、総務部=1人・平均280000の3行 |
| 3-(7) | 平均salaryが330000以上の部署 | **開発部のみ1件**（問題3-(6)の結果のうち375000だけが条件を満たす） |
| 4 | 山田太郎のsalaryを380000に更新後、`SELECT * FROM members WHERE name = '山田太郎';` | `salary`が`380000`になっている |
| 5 | 削除後の`SELECT * FROM members;`（question05.sqlの末尾で自動実行される） | **4件**に減っている（salaryが280000だった田中三郎が削除された） |

**正常な状態の見分け方**：件数や平均値が上記と異なる場合、`WHERE`の比較演算子（`>=`と`>`の取り違えなど）や、UPDATE・DELETEを実行する前の初期データの状態（問題1〜2を実行し忘れていないか）を確認してください。
