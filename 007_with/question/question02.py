"""
練習問題2：log.txt を読み込んで行番号付きで表示してください

期待する出力例:
  1: [INFO] サーバー起動
  2: [INFO] データベース接続完了
  3: [WARNING] メモリ使用率 80%
"""
import os

base_dir = os.path.dirname(__file__)
log_path = os.path.join(base_dir, 'log.txt')

# 準備：読み込み対象の log.txt を作っておく
with open(log_path, 'w', encoding='utf-8') as f:
    f.write('[INFO] サーバー起動\n')
    f.write('[INFO] データベース接続完了\n')
    f.write('[WARNING] メモリ使用率 80%\n')

print("問題2: 行番号付き表示")
# TODO: with open で読み込み、enumerate を使って行番号付きで print


# クリーンアップ
os.remove(log_path)
