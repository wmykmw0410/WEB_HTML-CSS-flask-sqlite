import os
from pathlib import Path

# ---- os.path ----
print("=== os.path ===")

# __file__ は実行中のスクリプト自身のパス
print(f"__file__         : {__file__}")
print(f"dirname          : {os.path.dirname(__file__)}")            # 親ディレクトリ
print(f"basename         : {os.path.basename(__file__)}")           # ファイル名

path = os.path.join(os.path.dirname(__file__), 'data', 'sample.txt')
print(f"join             : {path}")                                 # パスを連結

name, ext = os.path.splitext('report.csv')
print(f"splitext         : name={name}, ext={ext}")                 # 名前と拡張子を分離

print(f"exists(存在しないパス): {os.path.exists('/no/such/path')}")  # 存在確認
print(f"isfile           : {os.path.isfile(__file__)}")             # ファイルか
print(f"isdir            : {os.path.isdir(os.path.dirname(__file__))}")  # ディレクトリか

# ---- pathlib.Path（モダンな書き方）----
print("\n=== pathlib.Path ===")

p = Path(__file__)
print(f"Path(__file__)   : {p}")
print(f".parent          : {p.parent}")     # 親ディレクトリ（os.path.dirname 相当）
print(f".name            : {p.name}")       # ファイル名（os.path.basename 相当）
print(f".stem            : {p.stem}")       # 拡張子なしのファイル名
print(f".suffix          : {p.suffix}")     # 拡張子（'.py'）
print(f".exists()        : {p.exists()}")   # 存在確認

# / 演算子でパスを連結できる（os.path.join より直感的）
child = p.parent / 'data' / 'sample.txt'
print(f"parent / 'data'  : {child}")

# ---- ディレクトリ一覧 ----
print("\n=== ディレクトリ操作 ===")
base = Path(__file__).parent

# ディレクトリ内のファイル一覧
print("example/ のファイル:")
for item in sorted(base.iterdir()):
    print(f"  {item.name}  ({'dir' if item.is_dir() else 'file'})")

# 拡張子でフィルタ
py_files = list(base.glob('*.py'))
print(f"\n.py ファイル数: {len(py_files)}")
