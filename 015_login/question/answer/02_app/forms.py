from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError

from models import User


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
    # 問題1：パスワード確認欄
    confirm  = PasswordField('パスワード（確認）',
                             validators=[DataRequired(),
                                         EqualTo('password', message='パスワードが一致しません')])
    submit = SubmitField('登録')

    # 問題4：重複ユーザー名をブロック
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError(f'"{field.data}" はすでに使われています。')
