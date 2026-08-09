from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class UploadForm(FlaskForm):
    name = StringField('名前', validators=[DataRequired()])
    image = FileField(
        '画像',
        validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'], '画像ファイル（jpg/png/gif）のみアップロードできます。')]
    )
    submit = SubmitField('アップロード')
