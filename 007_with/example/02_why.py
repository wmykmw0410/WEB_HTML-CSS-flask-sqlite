import os

base_dir = os.path.dirname(__file__)
path     = os.path.join(base_dir, 'why_sample.txt')

# まず対象ファイルを用意
with open(path, 'w', encoding='utf-8') as f:
    f.write('hello\n')


# ---- パターン1：with なし（危険）----
print("=== with なし ===")
f = open(path, encoding='utf-8')
content = f.read()
f.close()   # 例外が起きるとここに到達せず close されない
print("読み込み:", content.strip())
print("close() を自分で呼ぶ必要がある")


# ---- パターン2：try / finally（安全だが冗長）----
print("\n=== try / finally ===")
f = open(path, encoding='utf-8')
try:
    content = f.read()
finally:
    f.close()   # 例外が起きても必ず実行される
print("読み込み:", content.strip())
print("確実に close される。ただし記述量が多い")


# ---- パターン3：with（シンプルかつ安全）----
print("\n=== with ===")
with open(path, encoding='utf-8') as f:
    content = f.read()
# f.close() は自動。例外が起きても必ず閉じる
print("読み込み:", content.strip())
print("close() の書き忘れがなく、例外時も確実に閉じる")


# ---- 例外が起きたときの違いを確認 ----
print("\n=== 例外が起きたとき ===")

# with ならブロックを抜けると close される
try:
    with open(path, encoding='utf-8') as f:
        raise ValueError("意図的な例外")
except ValueError:
    print(f"例外発生。f.closed = {f.closed}")  # True（with が自動で close した）

# クリーンアップ
os.remove(path)
