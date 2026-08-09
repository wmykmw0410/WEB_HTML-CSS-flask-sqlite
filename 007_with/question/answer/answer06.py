"""
練習問題6：os.path を使ってパスを操作する — 解答

(1) log_path の親ディレクトリを表示（os.path.dirname）
(2) log_path のファイル名だけを表示（os.path.basename）
(3) 'report.csv' の名前と拡張子を分けて表示（os.path.splitext）
(4) pathlib.Path で log_path を作り直して .stem と .suffix を表示
"""
import os
from pathlib import Path

base_dir = os.path.dirname(__file__)
log_path = os.path.join(base_dir, 'log.txt')

print("問題6: パス操作")

# (1) 親ディレクトリ
print(f"  (1) dirname  : {os.path.dirname(log_path)}")

# (2) ファイル名
print(f"  (2) basename : {os.path.basename(log_path)}")

# (3) 名前と拡張子を分離
name, ext = os.path.splitext('report.csv')
print(f"  (3) splitext : name={name}, ext={ext}")

# (4) pathlib
p = Path(log_path)
print(f"  (4) stem={p.stem}, suffix={p.suffix}")
