-- ============================================================
-- 01 CREATE TABLE — テーブル作成
-- ============================================================
-- 実行: sqlite3 books.db < 01_create.sql
-- ============================================================

-- テーブル作成（すでに存在する場合はスキップ）
CREATE TABLE IF NOT EXISTS books (
    id     INTEGER PRIMARY KEY AUTOINCREMENT,
    title  TEXT    NOT NULL,
    author TEXT    NOT NULL,
    price  INTEGER
);

-- 作成したテーブルの定義を確認
.schema books
