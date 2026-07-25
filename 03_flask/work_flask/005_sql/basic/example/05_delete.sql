-- ============================================================
-- 05 DELETE — データ削除
-- ============================================================
-- 実行: sqlite3 books.db < 05_delete.sql
-- ============================================================

.headers on
.mode column

-- 削除前の確認
SELECT * FROM books;

-- 1件削除
DELETE FROM books WHERE id = 5;

-- 条件に一致する複数件を削除
DELETE FROM books WHERE price < 2500;

-- 削除後の確認
SELECT * FROM books;

-- テーブルごと削除（全データ・テーブル定義も消える）
-- DROP TABLE IF EXISTS books;
