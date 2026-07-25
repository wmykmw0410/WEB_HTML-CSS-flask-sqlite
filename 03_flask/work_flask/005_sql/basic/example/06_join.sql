-- ============================================================
-- 06 JOIN — テーブルの結合
-- ============================================================
-- 実行: sqlite3 join.db < 06_join.sql
-- ============================================================

-- テーブル作成
CREATE TABLE IF NOT EXISTS authors (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    name    TEXT NOT NULL,
    country TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS books (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    title     TEXT    NOT NULL,
    author_id INTEGER,
    price     INTEGER
);

-- データ追加
INSERT INTO authors (name, country) VALUES ('山田太郎', '日本');
INSERT INTO authors (name, country) VALUES ('鈴木花子', '日本');
INSERT INTO authors (name, country) VALUES ('John Smith', 'アメリカ');

INSERT INTO books (title, author_id, price) VALUES ('Python入門',        1, 2800);
INSERT INTO books (title, author_id, price) VALUES ('Flask Webアプリ開発', 2, 3200);
INSERT INTO books (title, author_id, price) VALUES ('SQLite実践',         1, 1980);
INSERT INTO books (title, author_id, price) VALUES ('著者不明の本',        NULL, 500);  -- author_id なし

.headers on
.mode column

-- ============================================================
-- INNER JOIN：両方のテーブルに一致するレコードだけ取得
-- ============================================================
-- author_id が NULL の「著者不明の本」は結果に含まれない
SELECT
    books.id,
    books.title,
    authors.name    AS author,
    authors.country AS country,
    books.price
FROM books
INNER JOIN authors ON books.author_id = authors.id;

-- ============================================================
-- LEFT JOIN：左テーブル（books）の全件 + 一致する右テーブルの値
-- ============================================================
-- author_id が NULL の本も結果に含まれ、著者列は NULL になる
SELECT
    books.id,
    books.title,
    authors.name    AS author,
    authors.country AS country,
    books.price
FROM books
LEFT JOIN authors ON books.author_id = authors.id;

-- ============================================================
-- 別名（AS）でテーブル名を短縮
-- ============================================================
SELECT
    b.title,
    a.name  AS author,
    b.price
FROM books AS b
INNER JOIN authors AS a ON b.author_id = a.id
ORDER BY b.price DESC;
