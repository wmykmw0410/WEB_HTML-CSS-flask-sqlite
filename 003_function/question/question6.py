"""
問題6：以下のコードを完成させてください。add関数とmultiply関数の
両方に適用できるデコレータ show_result を作成してください。

期待する出力：
add の結果 → 8
multiply の結果 → 15
"""

# ここにデコレータ show_result を定義する

@show_result
def add(a, b):
    return a + b

@show_result
def multiply(a, b):
    return a * b

add(3, 5)
multiply(3, 5)
