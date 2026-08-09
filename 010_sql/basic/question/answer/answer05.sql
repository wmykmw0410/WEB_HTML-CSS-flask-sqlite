-- ============================================================
-- 問題 5：DELETE — 解答
-- ============================================================

.headers on
.mode column

-- 削除前の確認
SELECT * FROM members WHERE salary < 290000;

-- salary が 290000 未満のメンバーを削除
DELETE FROM members WHERE salary < 290000;

-- 最終状態を確認
SELECT * FROM members;
