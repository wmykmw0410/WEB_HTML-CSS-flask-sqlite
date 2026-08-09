def log(func):
    def inner():
        print("=== 開始 ===")
        func()
        print("=== 終了 ===")
    return inner

@log
def greet():
    print("Hello!")

greet()
