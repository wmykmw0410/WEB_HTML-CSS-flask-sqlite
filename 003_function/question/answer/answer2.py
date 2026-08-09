"""次の関数 show_info を呼び出すとき、位置引数とキーワード引数を混ぜて使用するとき
正しい呼び出し方を選べ"""

def show_info(name, age, country="日本"):
    print(f"{name}さん（{age}歳）は{country}出身です。")



# A. show_info("田中", country="アメリカ", 30)
# B. show_info("田中", 30, country="アメリカ")
# C. show_info(name="田中", 30, "アメリカ")
# D. show_info(30, "田中", "アメリカ")

# B