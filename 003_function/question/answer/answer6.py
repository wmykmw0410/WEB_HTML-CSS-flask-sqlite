def show_result(func):
    def inner(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f"{func.__name__} の結果 → {result}")
        return result
    return inner

@show_result
def add(a, b):
    return a + b

@show_result
def multiply(a, b):
    return a * b

add(3, 5)
multiply(3, 5)
