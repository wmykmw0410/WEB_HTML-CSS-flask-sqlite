"""
練習問題2：log.txt を読み込んで行番号付きで表示する — 解答
"""
import os

base_dir = os.path.dirname(__file__)
log_path = os.path.join(base_dir, 'log.txt')

# 準備：問題1で作った log.txt が無い場合のために、ここで作っておく
with open(log_path, 'w', encoding='utf-8') as f:
    f.write('[INFO] サーバー起動\n')
    f.write('[INFO] データベース接続完了\n')
    f.write('[WARNING] メモリ使用率 80%\n')

print("問題2: 行番号付き表示")
with open(log_path, encoding='utf-8') as f:
    for i, line in enumerate(f, start=1):
        print(f"  {i}: {line.rstrip()}")

# クリーンアップ
os.remove(log_path)
