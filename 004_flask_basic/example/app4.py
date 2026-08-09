from flask import Flask, render_template

app = Flask(__name__)


# Top Page（変数を渡さないパターン）
@app.route('/')
def index():
    return render_template('index.html')


# Item Detail（動的ルーティングで受け取った値をテンプレートに渡すパターン）
@app.route('/items/<int:item_id>')
def item_detail(item_id):
    return render_template('detail.html', item_id=item_id)


# Run
if __name__ == '__main__':
    app.run(debug=True, port=5004)
