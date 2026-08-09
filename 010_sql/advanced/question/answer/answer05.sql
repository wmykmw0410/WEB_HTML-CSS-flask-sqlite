-- 問題 5：トランザクション（COMMIT） — 解答
.headers on
.mode column

BEGIN;
INSERT INTO products (name, price, category, stock) VALUES ('新商品A', 5000, '電子機器', 10);
INSERT INTO products (name, price, category, stock) VALUES ('新商品B',  800, '文具',     50);
COMMIT;

SELECT * FROM products;
