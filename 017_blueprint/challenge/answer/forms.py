from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, IntegerField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length, NumberRange, Optional


class BookForm(FlaskForm):
    title = StringField('タイトル', validators=[DataRequired(), Length(max=100)])
    author = StringField('著者', validators=[DataRequired(), Length(max=100)])
    price = IntegerField('価格（円）', validators=[DataRequired(), NumberRange(min=1)])
    genre = StringField('ジャンル', validators=[Optional(), Length(max=50)])
    image = FileField(
        '表紙画像',
        validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'], '画像ファイル（jpg/png/gif）のみアップロードできます。')],
    )
    submit = SubmitField('追加する')


class RegisterForm(FlaskForm):
    username = StringField('ユーザー名', validators=[DataRequired(), Length(max=50)])
    password = PasswordField('パスワード', validators=[DataRequired(), Length(min=4, message='4文字以上で入力してください')])
    confirm = PasswordField('パスワード（確認）', validators=[DataRequired(), EqualTo('password', message='パスワードが一致しません')])
    submit = SubmitField('登録')


class LoginForm(FlaskForm):
    username = StringField('ユーザー名', validators=[DataRequired(), Length(max=50)])
    password = PasswordField('パスワード', validators=[DataRequired()])
    submit = SubmitField('ログイン')
