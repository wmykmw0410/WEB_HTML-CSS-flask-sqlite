"""
練習問題7：products.csv を作成し、DictReader で読み込む — 解答

ヘッダー: id, name, price
データ:
  1, りんご,  150
  2, バナナ,  120
  3, みかん,   80
"""
import os
import csv

base_dir = os.path.dirname(__file__)
csv_path = os.path.join(base_dir, 'products.csv')

print("問題7: CSV 読み書き")

with open(csv_path, 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['id', 'name', 'price'])
    writer.writerows([
        [1, 'りんご', 150],
        [2, 'バナナ', 120],
        [3, 'みかん',  80],
    ])

with open(csv_path, encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(f"  {row['name']} : {row['price']}円")

# クリーンアップ
os.remove(csv_path)
