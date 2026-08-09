from flask import Flask, url_for


# Create instance
app = Flask(__name__)


# Routing
# Index Page
@app.route("/")
def show_index():
    return 'Index Page'


@app.route('/hello/')
@app.route('/hello/<name>')
def show_hello(name=None):
    return f'Hello, {name}'


# Run
if __name__ == '__main__':
    with app.test_request_context():
        print(url_for('show_index'))              # /
        print(url_for('show_hello'))              # /hello/
        print(url_for('show_hello', name='Tom'))  # /hello/Tom

        # パスパラメータに存在しないキーはクエリパラメータになる
        print(url_for('show_index', page=2))               # /?page=2
        print(url_for('show_hello', name='Tom', lang='ja')) # /hello/Tom?lang=ja