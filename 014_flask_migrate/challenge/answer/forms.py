from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, Optional


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
