"""
練習問題3：log.txt に1行追記する（'a' モード） — 解答
"""
import os

base_dir = os.path.dirname(__file__)
log_path = os.path.join(base_dir, 'log.txt')

# 準備：追記対象の log.txt を作っておく
with open(log_path, 'w', encoding='utf-8') as f:
    f.write('[INFO] サーバー起動\n')
    f.write('[INFO] データベース接続完了\n')
    f.write('[WARNING] メモリ使用率 80%\n')

with open(log_path, 'a', encoding='utf-8') as f:
    f.write('[ERROR] 接続タイムアウト\n')

print("問題3: 追記後の log.txt:")
with open(log_path, encoding='utf-8') as f:
    print(f.read())

# クリーンアップ
os.remove(log_path)
