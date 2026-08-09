-- ============================================================
-- JOIN 練習問題 — 解答
-- ============================================================
-- 前提: sqlite3 join.db で basic/example/06_join.sql を先に実行してください

.headers on
.mode column

-- (1) INNER JOIN：書籍タイトルと著者名・国を一覧表示
SELECT b.title, a.name AS author, a.country, b.price
FROM books AS b
INNER JOIN authors AS a ON b.author_id = a.id;

-- (2) LEFT JOIN：著者不明の本も含めて表示
SELECT b.title, a.name AS author, b.price
FROM books AS b
LEFT JOIN authors AS a ON b.author_id = a.id;

-- (3) INNER JOIN + GROUP BY：著者ごとの書籍数と平均価格
SELECT a.name AS author, COUNT(*) AS 書籍数, AVG(b.price) AS 平均価格
FROM books AS b
INNER JOIN authors AS a ON b.author_id = a.id
GROUP BY a.name;
