from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    username = StringField('ユーザー名',
                           validators=[DataRequired('ユーザー名を入力してください'),
                                       Length(max=50)])
    password = PasswordField('パスワード',
                             validators=[DataRequired('パスワードを入力してください')])
    submit = SubmitField('ログイン')


class RegisterForm(FlaskForm):
    username = StringField('ユーザー名',
                           validators=[DataRequired('ユーザー名を入力してください'),
                                       Length(max=50)])
    password = PasswordField('パスワード',
                             validators=[DataRequired('パスワードを入力してください'),
                                         Length(min=4, message='4 文字以上で入力してください')])
    submit = SubmitField('登録')
