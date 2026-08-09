-- ============================================================
-- 04 UPDATE — データ更新
-- ============================================================
-- 実行: sqlite3 books.db < 04_update.sql
-- ============================================================

.headers on
.mode column

-- 更新前の確認
SELECT * FROM books;

-- 1件更新（price を変更）
UPDATE books SET price = 2500 WHERE id = 1;

-- 複数列を同時に更新
UPDATE books SET title = 'Python完全入門', price = 3000 WHERE id = 1;

-- 更新後の確認
SELECT * FROM books WHERE id = 1;
