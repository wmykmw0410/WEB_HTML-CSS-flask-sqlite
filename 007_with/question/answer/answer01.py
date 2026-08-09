"""
練習問題1：log.txt にログを3行書き込む — 解答
"""
import os

base_dir = os.path.dirname(__file__)
log_path = os.path.join(base_dir, 'log.txt')

with open(log_path, 'w', encoding='utf-8') as f:
    f.write('[INFO] サーバー起動\n')
    f.write('[INFO] データベース接続完了\n')
    f.write('[WARNING] メモリ使用率 80%\n')

print("問題1: log.txt に書き込み完了")

# クリーンアップ
os.remove(log_path)
