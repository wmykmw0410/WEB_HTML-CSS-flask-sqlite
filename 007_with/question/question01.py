"""
練習問題1：log.txt にログを3行書き込んでください

内容（例）:
  [INFO] サーバー起動
  [INFO] データベース接続完了
  [WARNING] メモリ使用率 80%
"""
import os

base_dir = os.path.dirname(__file__)
log_path = os.path.join(base_dir, 'log.txt')

# TODO: with open(log_path, 'w', ...) で3行書き込む


print("問題1: log.txt に書き込み完了")

# クリーンアップ
if os.path.exists(log_path):
    os.remove(log_path)
