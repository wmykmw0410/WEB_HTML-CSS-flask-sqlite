"""
練習問題7：products.csv を作成してください

ヘッダー: id, name, price
データ:
  1, りんご,  150
  2, バナナ,  120
  3, みかん,   80

作成後、csv.DictReader で読み込んで name と price を表示してください
"""
import os
import csv

base_dir = os.path.dirname(__file__)
csv_path = os.path.join(base_dir, 'products.csv')

print("問題7: CSV 読み書き")
# TODO: csv.writer で書き込み → csv.DictReader で読み込み


# クリーンアップ
if os.path.exists(csv_path):
    os.remove(csv_path)
