from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class ContactForm(FlaskForm):
    name = StringField('お名前',
                       validators=[DataRequired('お名前は必須です。'),
                                   Length(max=50)])
    email = EmailField('メールアドレス',
                       validators=[DataRequired('メールアドレスは必須です。'),
                                   Email('メールアドレスの形式が正しくありません。')])
    category = SelectField('お問い合わせ種別',
                           choices=[('general', '一般'),
                                    ('support', 'サポート'),
                                    ('other', 'その他')])
    message = TextAreaField('メッセージ',
                            validators=[DataRequired('メッセージは必須です。'),
                                        Length(max=500)])
    submit = SubmitField('送信する')
