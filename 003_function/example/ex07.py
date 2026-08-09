# 関数を引数に渡して、関数の中で実行する

# Function A
def a():
    print("A")


# Function B : 関数を引数として受け取り実行する
def b(func):
    print("---Start---")
    func()
    print("---End---")


# Calling function B
b(a)
