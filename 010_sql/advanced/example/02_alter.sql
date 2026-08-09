-- ============================================================
-- 02 ALTER TABLE — テーブルの変更
-- ============================================================
-- 実行: sqlite3 books.db
--       sqlite> .read advanced/example/02_alter.sql
-- ============================================================

-- 変更前の定義を確認
.schema books

-- カラムを追加
ALTER TABLE books ADD COLUMN publisher TEXT;

-- デフォルト値を指定して追加
ALTER TABLE books ADD COLUMN in_stock INTEGER DEFAULT 1;

-- 変更後の定義を確認
.schema books
