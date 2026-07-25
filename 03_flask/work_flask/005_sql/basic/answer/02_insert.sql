-- ============================================================
-- 問題 2：データ追加（INSERT） — 解答
-- ============================================================

INSERT INTO members (name, department, salary) VALUES ('山田太郎', '開発部', 350000);
INSERT INTO members (name, department, salary) VALUES ('鈴木花子', '営業部', 320000);
INSERT INTO members (name, department, salary) VALUES ('佐藤次郎', '開発部', 400000);
INSERT INTO members (name, department, salary) VALUES ('田中三郎', '総務部', 280000);
INSERT INTO members (name, department, salary) VALUES ('伊藤四郎', '営業部', 310000);

-- 追加結果を確認
.headers on
.mode column
SELECT * FROM members;
