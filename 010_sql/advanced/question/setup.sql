-- ============================================================
-- 応用 練習問題 — セットアップ（変更不要）
-- ============================================================
-- 実行: sqlite3 products.db
--       sqlite> .read advanced/question/setup.sql
-- 以降、question01.sql〜question06.sql は同じセッションの中で実行してください
-- ============================================================

CREATE TABLE IF NOT EXISTS products (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    name     TEXT    NOT NULL,
    price    INTEGER NOT NULL,
    category TEXT,
    stock    INTEGER
);

INSERT INTO products (name, price, category, stock) VALUES ('Python入門',  2800, '書籍',    10);
INSERT INTO products (name, price, category, stock) VALUES ('Flask開発',   3200, '書籍',     5);
INSERT INTO products (name, price, category, stock) VALUES ('ノートPC',  120000, '電子機器',  3);
INSERT INTO products (name, price, category, stock) VALUES ('マウス',     3500, '電子機器', 20);
INSERT INTO products (name, price, category, stock) VALUES ('ノート',      200, '文具',    100);
INSERT INTO products (name, price, category, stock) VALUES ('ペン',        150, '文具',   NULL);  -- stock なし
