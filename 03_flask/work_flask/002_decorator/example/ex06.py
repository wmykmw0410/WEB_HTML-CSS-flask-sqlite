# 可変長引数
"""
引数(*args, **kwargs)

*args（位置引数の可変長）
*args を使うと、複数の位置引数をタプルとして受け取ることができる

**kwargs（キーワード引数の可変長）
**kwargs を使うと、複数のキーワード引数を辞書として受け取ることできる
"""

# Function "outer"
def outer(func):

# Function "inner"
    def inner(*args, **kwargs):
        print("---Start---")
        func(*args, **kwargs)
        print("---End---")
    return inner


# Tuple
nums = (10, 20, 30, 40,50)


# Function "show_sum"
@outer
def show_sum(nums):
    sum = 0
    for num in nums:
        sum += num
    print(sum)


# Dict
users = {
    "Tom" : 30,
    "Ken" : 40,
    "John" : 50
    }


# Function "show_info"
@outer
def show_info(users):
    for name, age in users.items():
        print(f"Name:{name}, Age:{age}")


# Calling function
show_sum(nums)
show_info(users)