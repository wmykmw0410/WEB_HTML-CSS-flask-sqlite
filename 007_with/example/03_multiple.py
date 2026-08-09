import os

base_dir  = os.path.dirname(__file__)
path_in   = os.path.join(base_dir, 'input.txt')
path_out  = os.path.join(base_dir, 'output.txt')

# 入力ファイルを用意
with open(path_in, 'w', encoding='utf-8') as f:
    f.write('apple\nbanana\ncherry\n')


# ---- 複数ファイルを1行の with で同時に開く ----
print("=== 1行の with で2ファイルを同時に開く ===")
with open(path_in, encoding='utf-8') as f_in, \
     open(path_out, 'w', encoding='utf-8') as f_out:
    for line in f_in:
        f_out.write(line.upper())   # 大文字に変換して書き込む

# 結果確認
with open(path_out, encoding='utf-8') as f:
    print(f.read())


# ---- ネストで書く方法（同じ動作）----
print("=== ネスト（同じ動作だが読みにくい）===")
with open(path_in, encoding='utf-8') as f_in:
    with open(path_out, 'w', encoding='utf-8') as f_out:
        for line in f_in:
            f_out.write(line.lower())

with open(path_out, encoding='utf-8') as f:
    print(f.read())


# ---- as なし ----
print("=== as なし（変数が不要なとき）===")
# 追記モードで開くだけ（戻り値を使わない場合に as を省略）
import contextlib
path_maybe = os.path.join(base_dir, 'not_exist.txt')

with contextlib.suppress(FileNotFoundError):
    os.remove(path_maybe)   # ファイルがなくても例外を無視する
print("ファイルがなくてもエラーにならなかった")

# クリーンアップ
os.remove(path_in)
os.remove(path_out)
