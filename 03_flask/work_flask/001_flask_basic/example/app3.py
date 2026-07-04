from flask import Flask, request

# Create instance
app = Flask(__name__)


# --- パスパラメータ ---

# コンバータなし
@app.route('/dynamic/<value>')
def dynamic_default(value):
    print(f'Type : {type(value)}, Value : {value}')
    return f'<h1>渡された値は[{value}]です</h1>'


# コンバータあり
@app.route('/dynamic2/<int:number>')
def dynamic_converter(number):
    print(f'Type : {type(number)}, Value : {number}')
    return f'<h1>渡された値は[{number}]です</h1>'


# コンバータあり複数値渡し
@app.route('/dynamic3/<value>/<int:number>')
def dynamic_converter_multiple(value, number):
    print(f'Type : {type(value)}, Value : {value}')
    print(f'Type : {type(number)}, Value : {number}')
    return f'<h1>渡された値は[{value}]と[{number}]です</h1>'


# --- クエリパラメータ ---

# 単一のクエリパラメータ  例) /search?q=flask
@app.route('/search')
def search():
    keyword = request.args.get('q', '')
    return f'<h1>検索キーワード: [{keyword}]</h1>'


# 複数のクエリパラメータ  例) /items?sort=name&order=asc
@app.route('/items')
def items():
    sort  = request.args.get('sort', 'id')
    order = request.args.get('order', 'asc')
    return f'<h1>並び順: {sort} / {order}</h1>'


# パスパラメータ + クエリパラメータの組み合わせ
# 例) /categories/books?sort=price&order=desc
@app.route('/categories/<category>')
def category_items(category):
    sort  = request.args.get('sort', 'id')
    order = request.args.get('order', 'asc')
    return f'<h1>カテゴリ: {category} / 並び順: {sort} / {order}</h1>'


# Run
if __name__ == '__main__':
    app.run(debug=True, port=5003)