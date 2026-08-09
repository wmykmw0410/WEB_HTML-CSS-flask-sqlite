from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SubmitField
from wtforms.validators import DataRequired, Email


# Form class
# Input class
class InputForm(FlaskForm):
    name = StringField('Name:',
                       validators=[DataRequired('This field is required.')])
    email = EmailField('Email:',
                       validators=[Email('This is not a valid email address format.')])
    submit = SubmitField('Submit')