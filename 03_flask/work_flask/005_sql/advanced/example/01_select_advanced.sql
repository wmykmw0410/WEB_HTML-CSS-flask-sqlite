-- ============================================================
-- 01 SELECT 応用 — IN / BETWEEN / IS NULL
-- ============================================================
-- 実行: sqlite3 books.db < 01_select_advanced.sql
-- ============================================================

.headers on
.mode column

-- IN：複数の値と一致
SELECT * FROM books WHERE author IN ('山田太郎', '鈴木花子');

-- BETWEEN：範囲指定（A 以上 B 以下）
SELECT * FROM books WHERE price BETWEEN 2000 AND 3500;

-- IS NULL / IS NOT NULL
SELECT * FROM books WHERE price IS NULL;
SELECT * FROM books WHERE price IS NOT NULL;
