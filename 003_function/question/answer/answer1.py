"""名前を受け取ってあいさつを表示する関数を作成する
引数にデフォルト値"ゲスト"を設定して、引数なしでも使えるようせよ"""

def greet(name="guest"):
    print(f"Hello, {name}.")

name=input("whats your name ?")
greet(name)