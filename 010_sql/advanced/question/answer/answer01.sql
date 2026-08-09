-- 問題 1：IN — 解答
-- 前提: setup.sql を先に実行しておくこと
.headers on
.mode column
SELECT * FROM products WHERE category IN ('書籍', '文具');
