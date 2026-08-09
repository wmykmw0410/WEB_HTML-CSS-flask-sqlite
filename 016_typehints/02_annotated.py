from typing import Annotated

def process_value(
    value: Annotated[int, "0〜100の整数"]
) -> None:
    """
    0〜100の範囲の整数を受け取り、範囲内なら表示する

    Args:
        value: 0以上100以下の整数

    Raises:
        ValueError: 範囲外の値が渡された場合
    """
    if 0 <= value <= 100:
        print(f"受け取った値は範囲内です: {value}")
    else:
        raise ValueError(f"範囲外の値です。受け取った値: {value}")
    
#-----Calling-----
process_value(50)

try:
    process_value(150)
except ValueError as e:
    print(e)