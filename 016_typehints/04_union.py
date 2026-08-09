def parse_input(value: int | str) -> str:
    """
    入力値の型に応じてメッセージを返す

    Args:
        value: 整数または文字列

    Returns:
        型に応じた説明

    Raises:
        ValueError: 想定外の型が渡された場合
    """
    if isinstance(value, int):
        return f"値は整数型です=> {value}"
    elif isinstance(value, str):
        return f"値は文字列型です=> {value}"
    else:
        raise ValueError("引数が整数型/文字列型ではありません")


#-----Calling-----
print(parse_input(123))
print(parse_input("ABC"))
print(parse_input(99.9))