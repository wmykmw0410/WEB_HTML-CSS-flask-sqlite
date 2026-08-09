# 関数内関数

# Function "outer"
def outer(func):
# Function "inner"
    def inner():
        print("---Start---")
        func()
        print("---End---")
    return inner

# Function A
def a():
    print("A")

# 関数の実行 : 戻り値は変数resultに代入
result = outer(a)

# Calling function
result()
