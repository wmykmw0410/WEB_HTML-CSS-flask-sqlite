from flask import Flask, render_template

app = Flask(__name__)


class Human:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self):
        return f'Name:{self.name} Age:{self.age}'


class Item:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __str__(self):
        return f'ItemID:{self.id} ItemName:{self.name}'


# 変数展開（辞書・リスト・クラス）
@app.route('/vars')
def show_vars():
    words = {'temp': 'Template Engine', 'jinja': 'Jinja2'}
    alphabets = ['AAA', 'BBB', 'CCC']
    tom = Human('Tom', 20)
    return render_template('vars.html', key=words, words=alphabets, user=tom)


# for ループ
@app.route('/for')
def show_for():
    items = [Item(1, 'Curry'), Item(2, 'Rice'), Item(3, 'Pan')]
    return render_template('for.html', items=items)


# if / elif / else
@app.route('/if/')
@app.route('/if/<color>')
def show_if(color='colorless'):
    return render_template('if.html', color=color)


# for + if の組み合わせ
@app.route('/for-if/<int:id>')
def show_for_if(id):
    items = [Item(1, 'Curry'), Item(2, 'Rice'), Item(3, 'Pan')]
    return render_template('for_if.html', show_id=id, items=items)


if __name__ == '__main__':
    app.run(debug=True, port=5011)
