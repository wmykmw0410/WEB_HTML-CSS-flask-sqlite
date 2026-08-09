-- ============================================================
-- 02 INSERT — データ追加
-- ============================================================
-- 実行: sqlite3 books.db < 02_insert.sql
-- ============================================================

-- 1件追加
INSERT INTO books (title, author, price) VALUES ('Python入門',    '山田太郎', 2800);

-- 複数件追加
INSERT INTO books (title, author, price) VALUES ('Flask入門',     '鈴木花子', 3200);
INSERT INTO books (title, author, price) VALUES ('SQLite実践',    '佐藤次郎', 1980);
INSERT INTO books (title, author, price) VALUES ('データベース設計', '田中三郎', 4500);
INSERT INTO books (title, author, price) VALUES ('HTML & CSS入門', '伊藤四郎', 2200);
INSERT INTO books (title, author, price) VALUES ('Python応用',    '山田太郎', 3500);  -- GROUP BY 練習用（山田太郎が2冊になる）

-- 追加結果を確認
.headers on
.mode column
SELECT * FROM books;
