"""
練習問題3：log.txt に1行追記してください（'a' モード）

追記内容: [ERROR] 接続タイムアウト
"""
import os

base_dir = os.path.dirname(__file__)
log_path = os.path.join(base_dir, 'log.txt')

# 準備：追記対象の log.txt を作っておく
with open(log_path, 'w', encoding='utf-8') as f:
    f.write('[INFO] サーバー起動\n')
    f.write('[INFO] データベース接続完了\n')
    f.write('[WARNING] メモリ使用率 80%\n')

# TODO: with open(log_path, 'a', ...) で1行追記

print("問題3: 追記後の log.txt:")
with open(log_path, encoding='utf-8') as f:
    print(f.read())

# クリーンアップ
os.remove(log_path)
