"""位置引数"""
def add(a, b):
    print(a + b)

add(1, 2)
add(a=1, b=2) # キーワード指定も可能
add(b=2, a=1) # キーワード指定は順不同でも可
# add(b=2, 1) # SyntaxError: キーワード引数の後に位置引数は置けない