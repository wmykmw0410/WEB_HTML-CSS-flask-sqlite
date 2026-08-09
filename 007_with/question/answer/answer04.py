"""
練習問題4：log.txt と log_backup.txt を同時に開いて内容をコピーする — 解答
"""
import os

base_dir = os.path.dirname(__file__)
log_path = os.path.join(base_dir, 'log.txt')
backup_path = os.path.join(base_dir, 'log_backup.txt')

# 準備：コピー元の log.txt を作っておく
with open(log_path, 'w', encoding='utf-8') as f:
    f.write('[INFO] サーバー起動\n')
    f.write('[INFO] データベース接続完了\n')
    f.write('[WARNING] メモリ使用率 80%\n')

with open(log_path, encoding='utf-8') as f_in, \
     open(backup_path, 'w', encoding='utf-8') as f_out:
    for line in f_in:
        f_out.write(line)

print("問題4: バックアップ完了")
with open(backup_path, encoding='utf-8') as f:
    print(f.read())

# クリーンアップ
os.remove(log_path)
os.remove(backup_path)
