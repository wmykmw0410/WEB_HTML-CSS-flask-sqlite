-- 問題 1：IN — 解答
-- 前提: sqlite3 ec.db で practice.sql を先に実行してください
.headers on
.mode column
SELECT * FROM products WHERE category IN ('書籍', '文具');
