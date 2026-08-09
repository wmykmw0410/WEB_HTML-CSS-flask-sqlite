-- ============================================================
-- 問題 4：UPDATE — 解答
-- ============================================================

.headers on
.mode column

-- 更新前の確認
SELECT * FROM members WHERE name = '山田太郎';

-- 山田太郎の salary を 380000 に更新
UPDATE members SET salary = 380000 WHERE name = '山田太郎';

-- 更新後の確認
SELECT * FROM members WHERE name = '山田太郎';
