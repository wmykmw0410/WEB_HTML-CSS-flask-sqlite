-- ============================================================
-- 問題 3：SELECT — 解答
-- ============================================================

.headers on
.mode column

-- (1) 全件取得
SELECT * FROM members;

-- (2) 開発部のメンバーだけ取得
SELECT * FROM members WHERE department = '開発部';

-- (3) salary が 300000 以上のメンバーを salary の降順で取得
SELECT * FROM members WHERE salary >= 300000 ORDER BY salary DESC;

-- (4) 全メンバーの平均 salary を取得
SELECT AVG(salary) AS 平均salary FROM members;

-- (5) 部署の一覧を重複なしで取得（DISTINCT）
SELECT DISTINCT department FROM members;

-- (6) 部署ごとのメンバー数と平均 salary（GROUP BY）
SELECT department, COUNT(*) AS 人数, AVG(salary) AS 平均salary
FROM members
GROUP BY department;

-- (7) 平均 salary が 330000 以上の部署だけ取得（HAVING）
SELECT department, AVG(salary) AS 平均salary
FROM members
GROUP BY department
HAVING AVG(salary) >= 330000;
