import os

base_dir = os.path.dirname(__file__)
path     = os.path.join(base_dir, 'sample.txt')

# ---- 書き込み（'w'：上書き）----
with open(path, 'w', encoding='utf-8') as f:
    f.write('1行目\n')
    f.write('2行目\n')
    f.write('3行目\n')
print("書き込み完了")

# ---- 読み込み：全体を1つの文字列で ----
print("\n--- read()：全体 ---")
with open(path, encoding='utf-8') as f:
    content = f.read()
print(content)

# ---- 読み込み：行のリストで ----
print("--- readlines()：リスト ---")
with open(path, encoding='utf-8') as f:
    lines = f.readlines()   # ['1行目\n', '2行目\n', '3行目\n']
print(lines)

# ---- 読み込み：行ごとにループ ----
print("--- for ループ ---")
with open(path, encoding='utf-8') as f:
    for line in f:
        print(line.rstrip())   # rstrip() で末尾の改行を除去

# ---- 追記（'a'：末尾に追加）----
with open(path, 'a', encoding='utf-8') as f:
    f.write('4行目（追記）\n')

print("\n追記後:")
with open(path, encoding='utf-8') as f:
    print(f.read())

# クリーンアップ
os.remove(path)
