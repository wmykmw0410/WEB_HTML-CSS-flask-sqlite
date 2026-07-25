-- ============================================================
-- 応用 練習問題
-- ============================================================
-- 実行: sqlite3 products.db
--       sqlite> .read advanced/example/practice.sql
-- ============================================================

.headers on
.mode column

-- ---- セットアップ（変更不要） --------------------------------

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

-- ---- 問題 -------------------------------------------------------

-- ============================================================
-- 問題 1：IN
-- ============================================================
-- 書籍 または 文具 の商品を IN を使って取得してください

-- ここに SQL を書く


-- ============================================================
-- 問題 2：BETWEEN
-- ============================================================
-- price が 1000 以上 10000 以下の商品を取得してください

-- ここに SQL を書く


-- ============================================================
-- 問題 3：IS NULL
-- ============================================================
-- stock が登録されていない（NULL）商品を取得してください

-- ここに SQL を書く


-- ============================================================
-- 問題 4：ALTER TABLE
-- ============================================================
-- products テーブルに description カラム（TEXT）を追加してください

-- ここに SQL を書く


-- ============================================================
-- 問題 5：トランザクション（COMMIT）
-- ============================================================
-- BEGIN / COMMIT を使って、以下の2件をまとめて INSERT してください
-- ('新商品A', 5000, '電子機器', 10)
-- ('新商品B',  800, '文具',     50)

-- ここに SQL を書く


-- ============================================================
-- 問題 6：トランザクション（ROLLBACK）
-- ============================================================
-- BEGIN の後に DELETE FROM products WHERE id = 1 を実行し、
-- ROLLBACK で取り消してください。削除前後を SELECT で確認してください

-- ここに SQL を書く


-- 最終確認
SELECT * FROM products;
