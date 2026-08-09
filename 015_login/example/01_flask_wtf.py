"""
Flask-WTF フォームの基本

実行:
    python example/02_flask_wtf.py
    ブラウザで http://localhost:5000 にアクセス
"""
from flask import Flask, render_template_string, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret'   # CSRF トークン生成に必要

# --------------------------------------------------
# フォームクラスの定義
# --------------------------------------------------
class LoginForm(FlaskForm):
    username = StringField(
        'ユーザー名',
        validators=[DataRequired(message='ユーザー名を入力してください'),
                    Length(max=50, message='50 文字以内で入力してください')]
    )
    password = PasswordField(
        'パスワード',
        validators=[DataRequired(message='パスワードを入力してください')]
    )
    submit = SubmitField('ログイン')


TEMPLATE = """
<!doctype html>
<title>Flask-WTF サンプル</title>
<h1>ログイン</h1>
{% if message %}
    <p style="color:green">{{ message }}</p>
{% endif %}
<form method="post">
    {{ form.hidden_tag() }}

    <p>
        {{ form.username.label }}<br>
        {{ form.username(size=30) }}
        {% for error in form.username.errors %}
            <span style="color:red"> {{ error }}</span>
        {% endfor %}
    </p>

    <p>
        {{ form.password.label }}<br>
        {{ form.password(size=30) }}
        {% for error in form.password.errors %}
            <span style="color:red"> {{ error }}</span>
        {% endfor %}
    </p>

    {{ form.submit() }}
</form>
"""

@app.route('/', methods=['GET', 'POST'])
def index() -> str:
    form = LoginForm()
    message: str = ''
    if form.validate_on_submit():          # POST かつバリデーション成功
        message = f'送信完了：ユーザー名 = {form.username.data}'
    return render_template_string(TEMPLATE, form=form, message=message)


if __name__ == '__main__':
    app.run(debug=True, port=5041)
