-- ============================================================
-- 08 トランザクション
-- ============================================================
-- 実行: sqlite3 books.db
--       sqlite> .read 08_transaction.sql
-- ============================================================

.headers on
.mode column

-- 実行前の確認
SELECT * FROM books;

-- ============================================================
-- BEGIN / COMMIT：複数の操作をまとめて確定
-- ============================================================
BEGIN;

INSERT INTO books (title, author, price) VALUES ('新刊A', '山田太郎', 2000);
INSERT INTO books (title, author, price) VALUES ('新刊B', '鈴木花子', 2500);
UPDATE books SET price = 1800 WHERE id = 1;

COMMIT;   -- ここで初めてデータが確定する

-- COMMIT 後の確認
SELECT * FROM books;

-- ============================================================
-- BEGIN / ROLLBACK：操作を取り消す
-- ============================================================
BEGIN;

DELETE FROM books WHERE id = 1;

-- 削除されたように見える
SELECT * FROM books;

ROLLBACK;  -- BEGIN 以降の変更がすべて取り消される

-- ROLLBACK 後の確認（id=1 が復活している）
SELECT * FROM books;
