import wtforms.validators as validators
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms.fields import StringField, SelectField, SelectMultipleField, SubmitField, FloatField
from wtforms.widgets import ListWidget, CheckboxInput

from constants import GARBAGE_TYPES, PREFECTURES


class AddGarbageForm(FlaskForm):
    name = StringField("名前: ", render_kw={"placeholder": "(例)東京駅地下中央口改札前"})

    # ハイフンあり/なしどちらでも受け付ける（自動補完用JSはハイフンなし7桁で問い合わせる）
    postal_code = StringField(
        "郵便番号: ",
        [
            validators.Optional(),
            validators.Regexp(r"^\d{3}-?\d{4}$", message="郵便番号の形式が正しくありません（例: 100-0005）")
        ],
        render_kw={"placeholder": "(例)100-0005"}
    )
    prefecture = SelectField(
        "都道府県: ",
        choices=[(p, p) for p in PREFECTURES],
        validators=[validators.input_required()]
    )
    city = StringField(
        "市区町村: ",
        [validators.input_required()],
        render_kw={"placeholder": "(例)千代田区"}
    )
    address_line = StringField(
        "番地・建物名: ",
        [validators.input_required()],
        render_kw={"placeholder": "(例)丸の内1丁目"}
    )
    latitude = FloatField(
        "緯度: ",
        [
            validators.input_required(message="緯度を入力してください"),
            validators.NumberRange(-90, 90, message="緯度は-90から90の範囲で入力してください")
        ],
        render_kw={"placeholder": "(例)35.681236"}
    )
    longitude = FloatField(
        "経度: ",
        [
            validators.input_required(message="経度を入力してください"),
            validators.NumberRange(-180, 180, message="経度は-180から180の範囲で入力してください")
        ],
        render_kw={"placeholder": "(例)139.767125"}
    )
    # 複数選択できるようチェックボックス（ListWidget + CheckboxInput）で描画する。
    # 保存時はリストをカンマ区切り文字列に変換して1カラムに格納する（app.py参照）。
    type = SelectMultipleField(
        "ゴミの種類: ",
        choices=GARBAGE_TYPES,
        validators=[validators.input_required()],
        widget=ListWidget(prefix_label=False),
        option_widget=CheckboxInput()
    )
    photo = FileField(
        "写真: ",
        validators=[
            validators.Optional(),
            FileAllowed(["jpg", "jpeg", "png", "gif"], "画像ファイル（jpg, jpeg, png, gif）のみアップロードできます")
        ]
    )
    submit = SubmitField('登録')
