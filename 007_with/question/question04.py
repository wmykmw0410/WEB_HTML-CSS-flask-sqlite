"""
練習問題4：log.txt を読み込みながら log_backup.txt にコピーしてください

1行の with で2ファイルを同時に開くこと
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

# TODO: with open(...) as f_in, open(..., 'w') as f_out: でコピー

print("問題4: バックアップ完了")
with open(backup_path, encoding='utf-8') as f:
    print(f.read())

# クリーンアップ
os.remove(log_path)
os.remove(backup_path)
