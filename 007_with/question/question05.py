"""
練習問題5：次の try/finally を with を使って書き直してください

（書き直す前のコード）
f = open(log_path, encoding='utf-8')
try:
    content = f.read()
    print(content)
finally:
    f.close()
"""
import os

base_dir = os.path.dirname(__file__)
log_path = os.path.join(base_dir, 'log.txt')

# 準備：読み込み対象の log.txt を作っておく
with open(log_path, 'w', encoding='utf-8') as f:
    f.write('[INFO] サーバー起動\n')
    f.write('[INFO] データベース接続完了\n')
    f.write('[WARNING] メモリ使用率 80%\n')

print("問題5: with で書き直し")
# TODO: 上記のコードを with を使って書き直す


# クリーンアップ
os.remove(log_path)
