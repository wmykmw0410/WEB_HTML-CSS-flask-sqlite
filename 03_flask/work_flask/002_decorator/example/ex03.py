# 関数は第一級オブジェクト

def a():
    print("A")


# ポイント1：関数は変数に代入できる
print("--- ポイント1：変数への代入 ---")
x = a       # () を付けない → 関数オブジェクトを代入
print(x)    # <function a at 0x...>
x()         # A


# ポイント2：関数オブジェクトの情報を確認する
print("--- ポイント2：関数オブジェクトの情報 ---")
print(a)    # <function a at 0x...>


# ポイント3：print(a) と print(a()) の違い
print("--- ポイント3：print(a) と print(a()) ---")
print(a)    # 関数オブジェクトそのものを表示
print(a())  # a() を実行 → 戻り値 None を表示
