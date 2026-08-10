from flask_wtf import FlaskForm
from wtforms import PasswordField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length, Optional

CATEGORY_CHOICES = [
    ('家事', '家事'),
    ('仕事', '仕事'),
    ('趣味', '趣味'),
    ('アイデア', 'アイデア'),
    ('プライベート', 'プライベート'),
]


class LoginForm(FlaskForm):
    username = StringField('ユーザー名', validators=[DataRequired(), Length(max=50)])
    password = PasswordField('パスワード', validators=[DataRequired()])
    submit   = SubmitField('ログイン')


class RegisterForm(FlaskForm):
    username = StringField('ユーザー名', validators=[DataRequired(), Length(max=50)])
    password = PasswordField('パスワード', validators=[DataRequired(), Length(min=4, message='4文字以上で入力してください')])
    confirm  = PasswordField('パスワード（確認）', validators=[DataRequired(), EqualTo('password', message='パスワードが一致しません')])
    submit   = SubmitField('登録')


class MemoForm(FlaskForm):
    title    = StringField('タイトル', validators=[DataRequired(), Length(max=100)])
    category = SelectField('カテゴリ', choices=CATEGORY_CHOICES)
    body     = TextAreaField('本文', validators=[DataRequired(), Length(max=500)])
    due_date = StringField('期限（任意・例: 2026-08-10）', validators=[Optional(), Length(max=50)])
    submit   = SubmitField('保存する')
