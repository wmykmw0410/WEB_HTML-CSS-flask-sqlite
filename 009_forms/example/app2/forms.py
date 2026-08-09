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

# Form class #
# User information class
class UserInfoForm(Form):
    # 名前：文字列入力
    name = StringField('Name:', render_kw={"placeholder":"(ex)John Smith"})
    # 年齢：整数値入力
    age = IntegerField('Age:', default=20)
    # パスワード：パスワード入力
    password = PasswordField('Password:')
    # 確認用：パスワード入力
    confirm_password = PasswordField('Password Check:')
    # Email：メールアドレス
    email = EmailField('Mail address:')
    # 生年月日：日付入力
    birthday = DateField('Birthday:', format="%Y-%m-%d", render_kw={"placeholder":"yyyy/mm/dd"})
    # 性別：ラジオボタン
    gender = RadioField('Gender:', choices=[('man', 'Man'), ('woman', 'Woman')], default='man')
    # 出身地域：セレクトボタン
    area = SelectField('Area:', choices=[('east', 'East Japan'), ('west', 'West Japan')])
    # 既婚：真偽値入力
    is_married = BooleanField('Are you married?')
    # メッセージ：複数行テキスト
    note = TextAreaField('Remarks:')
    # ボタン
    submit = SubmitField('Send')


