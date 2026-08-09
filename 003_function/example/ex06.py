count = 0

def increment_wrong():
    count += 1  # UnboundLocalError: global なしに外の変数を変更しようとするとエラー

def increment():
    global count
    count += 1  # global をつけると外の変数を変更できる

print(count)   # 出力: 0 (グローバル変数はそのまま参照できる)
increment()
print(count)   # 出力: 1
