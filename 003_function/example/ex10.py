# Decorator

# Function "outer"
def outer(func):

# Function "inner"
    def inner():
        print("---Start---")
        func()
        print("---End---")
    return inner

# Function A
@outer
def a():
    print("A")


# Function B
@outer
def b():
    print("B")


# Calling function
a()
b()