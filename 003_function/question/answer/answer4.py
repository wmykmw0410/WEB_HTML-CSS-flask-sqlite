"""ユーザー情報を受け取り、キーと値を表示する関数を作成せよ

入力データ：name="太郎", age=20, hobby="ゲーム"

出力結果：
        name：太郎
        age：20
        hobby：ゲーム
"""

def show_user_info(**info):
    for key, value in info.items():
        print(f"{key}：{value}")

show_user_info(name="太郎", age=20, hobby="ゲーム")
