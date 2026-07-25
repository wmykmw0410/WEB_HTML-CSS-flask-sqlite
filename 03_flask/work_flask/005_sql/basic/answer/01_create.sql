-- ============================================================
-- 問題 1：テーブル作成 — 解答
-- ============================================================

CREATE TABLE IF NOT EXISTS members (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    name       TEXT    NOT NULL,
    department TEXT    NOT NULL,
    salary     INTEGER
);

-- 定義を確認
.schema members
