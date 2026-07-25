-- ============================================================
-- 03 SELECT — データ取得（基本）
-- ============================================================
-- 実行: sqlite3 books.db < 03_select.sql
-- ============================================================

.headers on
.mode column

-- 全件・全列取得
SELECT * FROM books;

-- 特定の列だけ取得
SELECT title, price FROM books;

-- WHERE：条件で絞り込む
SELECT * FROM books WHERE price > 2500;

-- AND / OR：複数条件
SELECT * FROM books WHERE price >= 2000 AND price <= 3500;
SELECT * FROM books WHERE author = '山田太郎' OR author = '鈴木花子';

-- LIKE：部分一致（% は任意の文字列、_ は任意の1文字）
SELECT * FROM books WHERE title LIKE '%入門%';

-- ORDER BY：並び替え（ASC = 昇順、DESC = 降順）
SELECT * FROM books ORDER BY price ASC;
SELECT * FROM books ORDER BY price DESC;

-- LIMIT：取得件数を制限
SELECT * FROM books ORDER BY price DESC LIMIT 3;

-- 集計関数
SELECT COUNT(*) AS 件数   FROM books;
SELECT AVG(price) AS 平均 FROM books;
SELECT MAX(price) AS 最高 FROM books;
SELECT MIN(price) AS 最低 FROM books;
SELECT SUM(price) AS 合計 FROM books;

-- DISTINCT：重複を除外
SELECT DISTINCT author FROM books;

-- ============================================================
-- GROUP BY：グループ集計
-- ============================================================
-- 著者ごとの書籍数
SELECT author, COUNT(*) AS 件数 FROM books GROUP BY author;

-- 著者ごとの平均価格
SELECT author, AVG(price) AS 平均価格 FROM books GROUP BY author;

-- ============================================================
-- HAVING：グループに対する条件
-- ============================================================
-- 書籍数が 2 件以上の著者だけ
SELECT author, COUNT(*) AS 件数
FROM books
GROUP BY author
HAVING COUNT(*) >= 2;

-- 平均価格が 2500 円以上の著者だけ
SELECT author, AVG(price) AS 平均価格
FROM books
GROUP BY author
HAVING AVG(price) >= 2500;
