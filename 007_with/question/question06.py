"""
練習問題6：os.path を使ってパスを操作してください

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
# TODO: (1)〜(4) を実装
