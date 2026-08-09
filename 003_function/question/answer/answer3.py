"""複数の食べ物リストを表示する関数を作成せよ

入力データ："カレー", "寿司", "ラーメン"

出力結果：好きな食べ物：
        カレー
        寿司
        ラーメン
"""

def list_foods(*foods):
    print("好きな食べ物：")
    for food in foods:
        print(food)

list_foods("カレー", "寿司", "ラーメン")