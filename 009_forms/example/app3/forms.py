from wtforms import Form
from wtforms.fields import (
                        StringField,
                        IntegerField,
                        PasswordField, 
                        DateField,
                        RadioField,
                        SelectField, 
                        BooleanField,
                        TextAreaField,
                        EmailField,
                        SubmitField
                    )
from wtforms.validators import (DataRequired,
                                EqualTo,
                                Length,
                                NumberRange,
                                Email,
                                ValidationError)

# Form class #
# User information class
class UserInfoForm(Form):

    # 名前：文字列入力
    name = StringField('Name:', 
                       validators=[DataRequired('Name is required.')],
                       render_kw={"placeholder":"(ex)John Smith"})
    
    # 年齢：整数値入力
    age = IntegerField('Age:', 
                       validators=[NumberRange(18, 100, 'The input range is from 18 to 100 years old.')],
                       default=20)
    
    # パスワード：パスワード入力
    password = PasswordField('Password:',
                             validators=[Length(1, 10, 'Password length must be between 1 and 10 characters.'),
                             EqualTo('confirm_password', 'The password does not match.')])
    
    # 確認用：パスワード入力
    confirm_password = PasswordField('Password Check:')

    # Email：メールアドレス
    email = EmailField('Mail address:',
                       validators=[Email('This is not an email address format.')])
    
    # 生年月日：日付入力
    birthday = DateField('Birthday:',
                         validators=[DataRequired('Birthday is required.')],
                         format="%Y-%m-%d",
                         render_kw={"placeholder":"yyyy/mm/dd"})
    
    # 性別：ラジオボタン
    gender = RadioField('Gender:',
                        choices=[('man', 'Man'), ('woman', 'Woman')],
                        default='man')
    
    # 出身地域：セレクトボタン
    area = SelectField('Area:', 
                       choices=[('east', 'East Japan'), ('west', 'West Japan')])

    # 既婚：真偽値入力
    is_married = BooleanField('Are you married?')

    # メッセージ：複数行テキスト
    note = TextAreaField('Remarks:')
    
    # ボタン
    submit = SubmitField('Send')

    def validate_password(self, password):
        if not (any(c.isalpha() for c in password.data) and \
            any(c.isdigit() for c in password.data) and \
            any(c in '!@#$%^&*()' for c in password.data)):
            raise ValidationError("Your password must include alphanumeric characters and symbols '!@#$%^&*()' .")
