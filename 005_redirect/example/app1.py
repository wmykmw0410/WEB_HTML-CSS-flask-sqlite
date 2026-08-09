from flask import Flask, redirect, url_for

# Create instance
app = Flask(__name__)


# Top Page
@app.route('/')
def index():
    return '<h1>Top Page</h1>'


# Old URL -> 新しいURLへリダイレクト
@app.route('/old')
def old_page():
    return redirect(url_for('new_page'))


# New URL
@app.route('/new')
def new_page():
    return '<h1>New Page</h1>'


# 外部URLへリダイレクト
@app.route('/go-flask')
def go_flask():
    return redirect('https://flask.palletsprojects.com/')


# url_for に引数を渡す（動的ルーティングのURLを組み立てる）
@app.route('/items/<int:item_id>')
def item_detail(item_id):
    return f'<h1>Item {item_id}</h1>'


@app.route('/go-item/<int:item_id>')
def go_item(item_id):
    return redirect(url_for('item_detail', item_id=item_id))


# Run
if __name__ == '__main__':
    app.run(debug=True, port=5008)
