# ゴミの種類を複数選択できるように変更

日付: 2026-08-29

## これは何をする作業か

それまで「ゴミの種類」は1つしか選べないプルダウン（`SelectField`）だった。1つのゴミ箱が複数の種類（例: 缶とペットボトル両方）を回収できるように、チェックボックスで複数選択できるように変更する。

## 手順

1. `trash_map/form.py` を開き、`type` フィールドの定義を `SelectField` から `SelectMultipleField` に変更する。あわせてチェックボックスとして描画するために `ListWidget` / `CheckboxInput` をimportする。
   ```python
   from wtforms.fields import (..., SelectMultipleField, ...)
   from wtforms.widgets import ListWidget, CheckboxInput

   type = SelectMultipleField(
       "ゴミの種類: ",
       choices=[
           ("burnable", "燃えるゴミ"),
           ("nonburnable", "不燃ごみ"),
           ("can", "缶"),
           ("pet_bottle", "ペットボトル"),
           ("glass", "瓶"),
       ],
       validators=[validators.input_required()],
       widget=ListWidget(prefix_label=False),
       option_widget=CheckboxInput()
   )
   ```
2. データベースの `type` カラムは複数の値をカンマ区切り（例: `"burnable,can"`）で保存するため、文字数が足りるように長さを拡張する。`trash_map/models.py` を開き、次のように変更する。
   ```python
   # 変更前: db.Column(db.String(20), ...)
   # 変更後:
   type = db.Column(db.String(100), nullable=False)
   ```
3. `trash_map/app.py` の `add_page` 関数を開く。フォームの `type` は複数選択なのでPythonの**リスト**（例: `['burnable', 'can']`）になる。DBには1つの文字列としてしか保存できないので、カンマ区切り文字列に変換してから保存する。
   ```python
   # 変更前: type=form.type.data
   # 変更後:
   type=",".join(form.type.data)
   ```
4. `trash_map/templates/trash/add.html` で `{{ form.type() }}` とだけ書いていた部分を、チェックボックスを1つずつループで描画する形に書き換える。
   ```html
   {% for subfield in form.type %}
   <li>
       <label>{{ subfield(required=false) }} {{ subfield.label.text }}</label>
   </li>
   {% endfor %}
   ```
   - `required=false` を付けている理由: これを付けないと、バリデーションの `input_required()` の影響で **各チェックボックス1つ1つ** に `required` 属性が付いてしまい、ブラウザが「全部チェックしないと送信できない」という誤った挙動になる。
   - `required=false` を付けても、サーバー側の `input_required()` は「1つもチェックされていない」場合だけを弾く仕組みなので、「最低1つは選択する」というバリデーション自体はきちんと機能する。

## 動作確認

1. `/add` をブラウザ（またはGETリクエスト）で開き、5つのチェックボックス（燃えるゴミ・不燃ごみ・缶・ペットボトル・瓶）に `required` 属性が付いていないことを確認する。
2. `type=['can', 'glass']` のように2つ選んで送信し、`302 /thankyou`（登録成功）になり、DBの `type` が `"can,glass"` として保存されることを確認する。
3. 何もチェックせずに送信し、`200`（バリデーションエラーで再表示）になることを確認する。
4. 確認用に登録したテストレコードはDBから削除しておく。
