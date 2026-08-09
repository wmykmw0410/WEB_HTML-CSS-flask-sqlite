def add(num1: int, num2: int) -> str:
    """
    2つの整数を加算し、説明文付きの文字列で返す

    Args:
        num1: 1つ目の整数
        num2: 2つ目の整数

    Returns:
        加算結果を含む説明文
    """
    result: str = 'The result of addition => '
    return result + str(num1 + num2)

#-----Calling-----
print(add(10, 20))


def greet(name: str) -> str:
    """
    名前を受け取り、挨拶文を返す

    Args:
        name: 挨拶する相手の名前

    Returns:
        挨拶文
    """
    return f"Hello, {name}."

#-----Calling-----
print(greet("Tom"))


def divide(divided: float, divisor: float) -> float:
    """
    2つの数値を割り算し、説明文付きの文字列で返す

    Args:
        divided: 割られる数
        divisor: 割る数

    Returns:
        割り算結果を含む説明文
    """
    return f"The result of division => {divided / divisor}"

#-----Calling-----
print(divide(10.0, 2.0))


def process_items(items: list[str]) -> None:
    """
    文字列のリストを1件ずつ表示する

    Args:
        items: 表示したい文字列のリスト
    """
    for item in items:
        print(item)

#-----Calling-----
process_items(["A", "B", "C"])


def count_characters(word_list: list[str]) -> dict[str, int]:
    """
    単語ごとの文字数を辞書にまとめる

    Args:
        word_list: 文字数を数えたい単語のリスト

    Returns:
        単語をキー、文字数を値とする辞書
    """
    count_map: dict[str, int] = {}

    for word in word_list:
        count_map[word] = len(word)

    return count_map

character_counts = count_characters(["apple", "amazon", "google"])
print("The string for the character is", character_counts)