"""デフォルト引数"""
# 例1
def add1(a=1, b=2):
    print(a + b)

add1()
add1(3, 2)

# 例2
def add2(a, b=2):
    print(a + b)

add2(3)
add2(a = 3)

# エラーのパターン
# デフォルト引数は右側から準備する
# def add(a=1, b):
#     print(a + b)

# add(b = 3)
