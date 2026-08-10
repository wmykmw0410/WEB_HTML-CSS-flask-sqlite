from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length

CATEGORY_CHOICES = [
    ('家事', '家事'),
    ('仕事', '仕事'),
    ('趣味', '趣味'),
    ('アイデア', 'アイデア'),
    ('プライベート', 'プライベート'),
]


class MemoForm(FlaskForm):
    title = StringField('タイトル', validators=[DataRequired(), Length(max=100)])
    category = SelectField('カテゴリ', choices=CATEGORY_CHOICES)
    body = TextAreaField('本文', validators=[DataRequired(), Length(max=500)])
    submit = SubmitField('追加する')
