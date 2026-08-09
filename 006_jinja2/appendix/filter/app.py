from flask import Flask, render_template, abort
from werkzeug.exceptions import NotFound

app = Flask(__name__)


class Human:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self):
        return f'Name:{self.name} Age:{self.age}'


# 組み込みフィルター（ブロック）
@app.route('/filter')
def show_filter_block():
    word = 'pen'
    return render_template('filter/block.html', show_word=word)


# 組み込みフィルター（変数）
@app.route('/filter2')
def show_filter_variable():
    user_list = [
        Human('Tom', 20), Human('Ken', 30), Human('John', 40),
        Human('Mary', 50), Human('Anna', 60),
    ]
    return render_template('filter/filter_list.html', users=user_list)


# カスタムフィルターの定義
@app.template_filter('truncate')
def str_truncate(value, length=10):
    if len(value) > length:
        return value[:length] + '...'
    return value


# カスタムフィルターの使用
@app.route('/filter3')
def show_my_filter():
    word = '寿限無'
    long_word = 'じゅげむじゅげむごこうのすりきれ'
    return render_template('filter/my_filter.html', show_word1=word, show_word2=long_word)


# エラーハンドラ
@app.errorhandler(NotFound)
def show_404_page(error):
    return render_template('errors/404.html'), 404


@app.route('/abort')
def create_exception():
    abort(404, 'The requested page or file cannot be found.')


if __name__ == '__main__':
    app.run(debug=True, port=5013)
