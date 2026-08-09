def greet():
    name = "Alice"  # ローカル変数
    print("Hello,", name)

greet()
# print(name)  # エラー！関数の外からは name にアクセスできない
