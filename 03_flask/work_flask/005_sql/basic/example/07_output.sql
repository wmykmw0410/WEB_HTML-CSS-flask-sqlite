-- ============================================================
-- 07 データファイルへの出力
-- ============================================================
-- 実行: sqlite3 books.db
--       sqlite> .read 07_output.sql
-- ============================================================

-- CSV ファイルへ出力
.mode csv
.headers on
.output result.csv
SELECT * FROM books;
.output stdout    -- 標準出力に戻す
.mode column      -- 表示モードを元に戻す

-- JSON ファイルへ出力
.mode json
.output result.json
SELECT * FROM books;
.output stdout
.mode column
