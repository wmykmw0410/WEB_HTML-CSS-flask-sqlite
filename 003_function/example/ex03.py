"""可変長位置引数（*args）と可変長キーワード引数（**kwargs）"""

def show_args(*args):
    print(args)         # タプルとして受け取る
    print(type(args))   # <class 'tuple'>

show_args(1, 2, 3)      # (1, 2, 3)
show_args()             # 引数が無ければ空タプル ()


def show_kwargs(**kwargs):
    print(kwargs)        # 辞書として受け取る
    print(type(kwargs))  # <class 'dict'>

show_kwargs(x=1, y=2)   # {'x': 1, 'y': 2}
show_kwargs()           # 引数が無ければ空辞書 {}


# *args と **kwargs は同じ関数の中で併用できる（この順番で書く）
def show_both(*args, **kwargs):
    print("args:", args)
    print("kwargs:", kwargs)

show_both(1, 2, x=3, y=4)  # args: (1, 2)  kwargs: {'x': 3, 'y': 4}
