-- 問題 6：トランザクション（ROLLBACK） — 解答
.headers on
.mode column

-- 削除前の確認
SELECT * FROM products WHERE id = 1;

BEGIN;
DELETE FROM products WHERE id = 1;

-- BEGIN 後（削除されているように見える）
SELECT * FROM products WHERE id = 1;

ROLLBACK;

-- ROLLBACK 後（id=1 が復活）
SELECT * FROM products WHERE id = 1;
