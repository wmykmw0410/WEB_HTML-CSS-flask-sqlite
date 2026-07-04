# 004 フォーム

生の HTML フォームから始め、WTForms・Flask-WTF・session まで段階的にフォーム処理を学びます。

## 目次

1. [生のフォーム（request）](#1-生のフォームrequest) — `request.args` / `request.form` で値を受け取る
2. [WTForms 基本](#2-wtforms-基本) — Form クラスとフィールド種類
3. [WTForms バリデーション](#3-wtforms-バリデーション) — バリデーター・カスタムバリデーター
4. [Flask-WTF（CSRF 保護）](#4-flask-wtfcsrf-保護) — FlaskForm・SECRET_KEY・`validate_on_submit()`
5. [session + PRG パターン](#5-session--prg-パターン) — session によるデータ保持とリダイレクト
6. [練習問題](#6-練習問題) — お問い合わせフォーム（1〜4の総合）

---

## フォルダ構成

```
004_forms/
├── README.md
└── example/
    ├── app1/   生のフォーム（request.args / request.form）
    ├── app2/   WTForms 基本（フィールド種類・送信結果表示）
    ├── app3/   WTForms バリデーション（validate・カスタムバリデーター）
    ├── app4/   Flask-WTF（FlaskForm・CSRF・validate_on_submit）
    └── app5/   session + POST後リダイレクト（PRGパターン）
```

---

## 1. 生のフォーム（request）

> [example/app1/](example/app1/)

テンプレートもライブラリも使わず、`request` オブジェクトから直接フォーム値を取り出す最小構成です。

### HTML フォームの基本要素

> HTML サンプル → [example/app2/templates/enter_html.html](example/app2/templates/enter_html.html)

フォームは `<form>` タグで囲み、`method` で送信方法を指定します。`<input>` の `name` 属性が Flask 側で取得するキーになります。

```html
<form method="POST" action="/">
    <input type="text" name="username">
    <input type="submit" value="送信">
</form>
```

#### input タグの種類

| type 属性 | 表示例 | 備考 |
|---|---|---|
| `type="text"` | `[John Smith        ]` | `size` で表示幅を指定 |
| `type="number"` | `[  20  ▲▼]` | スピンボタン付き |
| `type="password"` | `[••••••••••        ]` | 入力文字が隠れる |
| `type="email"` | `[xxxx@example.com  ]` | ブラウザ側でフォーマット検証 |
| `type="date"` | `[yyyy-mm-dd 📅]` | `value` は `YYYY-MM-DD` 形式 |
| `type="radio"` | `(●) Man  ( ) Woman` | 同じ `name` でグループ化、`checked` で初期選択 |
| `type="checkbox"` | `[✓] Are you married?` | チェック時は `value` の値が送信される |
| `type="submit"` | `[  Send  ]` | `value` がボタンのラベル |

#### radio / select / textarea は別タグ

| タグ | 表示例 | 備考 |
|---|---|---|
| `<input type="radio">` | `(●) Man  ( ) Woman` | 同じ `name` でグループ化。1つしか選べない |
| `<select>` | `[East Japan ▼]` | ドロップダウン。`<option>` で選択肢を定義 |
| `<textarea>` | 複数行の入力エリア | `style` で高さ・幅を指定 |

```html
<!-- ラジオボタン：同じ name でグループ化 -->
<input type="radio" name="gender" value="man" checked> Man
<input type="radio" name="gender" value="woman"> Woman

<!-- セレクトボックス -->
<select name="area">
    <option value="east">East Japan</option>
    <option value="west">West Japan</option>
</select>

<!-- 複数行テキスト -->
<textarea name="note" style="height:100px; width:150px"></textarea>
```

#### `label` タグ

`for` 属性と `input` の `id` を一致させると、ラベルクリックで入力欄にフォーカスできます。

```html
<label for="username">名前:</label>
<input type="text" id="username" name="username">
```

---

### GET パラメータ — `request.args`

URL の `?name=...` 部分（クエリパラメータ）を取得します。

```python
@app.route("/get")
def do_get():
    name = request.args.get('name')
    return f'Hello, {name}!'
```

### POST パラメータ — `request.form`

`<form method="post">` で送信されたデータを取得します。

```python
@app.route("/", methods=['GET', 'POST'])
def do_get_post():
    if request.method == 'POST':
        name = request.form.get('name')
        return f'Hello, {name}!'
    return """
    <form method="post">
    Name : <input type="text" name="name">
    <input type="submit" value="post">
    </form>
    """
```

### ポイント

| 取得方法 | 対象 | 説明 |
|---|---|---|
| `request.args.get('key')` | GET | URL の `?key=value` |
| `request.form.get('key')` | POST | フォームの `name="key"` |

---

## 2. WTForms 基本

> [example/app2/](example/app2/)

WTForms を使ってフォームをクラスで定義します。フィールドの種類とテンプレートへの渡し方を学びます。

### Form クラスの定義

```python
from wtforms import Form
from wtforms.fields import StringField, IntegerField, RadioField, ...

class UserInfoForm(Form):
    name     = StringField('Name:')
    age      = IntegerField('Age:', default=20)
    gender   = RadioField('Gender:', choices=[('man', 'Man'), ('woman', 'Woman')])
    area     = SelectField('Area:', choices=[('east', 'East Japan'), ('west', 'West Japan')])
    note     = TextAreaField('Remarks:')
    submit   = SubmitField('Send')
```

### ビュー関数

```python
from forms import UserInfoForm

@app.route('/', methods=['GET', 'POST'])
def show_enter():
    form = UserInfoForm(request.form)
    if request.method == "POST":
        return render_template('result.html', form=form)
    return render_template('enter.html', form=form)
```

### テンプレートでの表示

```html
<form method="POST">
    {{ form.name.label }}{{ form.name(size=20) }} <br>
    {{ form.age.label }}{{ form.age() }} <br>
    {{ form.gender.label }}{{ form.gender() }} <br>
    {{ form.submit() }}
</form>
```

送信後は `form.フィールド名.data` で入力値を参照できます。

```html
<li>Name: {{ form.name.data }}</li>
<li>Age: {{ form.age.data }}</li>
```

### 主なフィールド種類

| フィールド | 入力要素 |
|---|---|
| `StringField` | テキスト入力 |
| `IntegerField` | 数値入力 |
| `PasswordField` | パスワード入力 |
| `EmailField` | メールアドレス入力 |
| `DateField` | 日付入力 |
| `RadioField` | ラジオボタン |
| `SelectField` | セレクトボックス |
| `BooleanField` | チェックボックス |
| `TextAreaField` | 複数行テキスト |

---

## 3. WTForms バリデーション

> [example/app3/](example/app3/)

バリデーターを使って入力値を検証します。エラー時はフォームを再表示し、成功時のみ結果を表示します。

### バリデーターの追加

```python
from wtforms.validators import DataRequired, EqualTo, Length, NumberRange, Email, ValidationError

class UserInfoForm(Form):
    name = StringField('Name:',
                       validators=[DataRequired('名前は必須です。')])
    age  = IntegerField('Age:',
                        validators=[NumberRange(18, 100, '18〜100 の範囲で入力してください。')])
    password = PasswordField('Password:',
                             validators=[Length(1, 10),
                                        EqualTo('confirm_password', 'パスワードが一致しません。')])
    email = EmailField('Mail address:',
                       validators=[Email('メールアドレスの形式が正しくありません。')])
```

### `form.validate()` で検証する

```python
@app.route('/', methods=['GET', 'POST'])
def show_enter():
    form = UserInfoForm(request.form)
    if request.method == "POST" and form.validate():
        return render_template('result.html', form=form)
    return render_template('enter.html', form=form)
```

### カスタムバリデーター

`validate_フィールド名()` メソッドを定義すると独自ルールを追加できます。

```python
def validate_password(self, password):
    if not (any(c.isalpha() for c in password.data) and
            any(c.isdigit() for c in password.data) and
            any(c in '!@#$%^&*()' for c in password.data)):
        raise ValidationError("英字・数字・記号 '!@#$%^&*()' をすべて含めてください。")
```

### エラーメッセージの表示

```html
{% for error in form.name.errors %}
    <span style="color:red;">{{ error }}</span>
{% endfor %}
```

### 主なバリデーター

| バリデーター | 用途 |
|---|---|
| `DataRequired()` | 空欄を禁止 |
| `Length(min, max)` | 文字数制限 |
| `NumberRange(min, max)` | 数値範囲 |
| `Email()` | メール形式チェック |
| `EqualTo('field')` | 別フィールドとの一致（パスワード確認など） |
| `ValidationError` | カスタムバリデーターで使う例外 |

---

## 4. Flask-WTF（CSRF 保護）

> [example/app4/](example/app4/)

### CSRF とは

**CSRF（Cross-Site Request Forgery）** は、ログイン中のユーザーを罠サイトへ誘導し、そのユーザーになりすましてフォームを送信させる攻撃です。対策として、フォームに**サーバだけが知る使い捨てトークン**を埋め込み、送信時に一致するか検証します。トークンが合わなければリクエストを拒否します。Flask-WTF はこの仕組みを自動で行います。トークンの生成には `SECRET_KEY` が使われるため、設定が必須です。

Flask-WTF は WTForms の Flask 拡張です。`FlaskForm` を継承するだけで **CSRF トークン** が自動管理されます。

### `FlaskForm` と `SECRET_KEY`

```python
from flask_wtf import FlaskForm
import os

app.config['SECRET_KEY'] = os.urandom(24)  # CSRF トークンの署名に必要

class InputForm(FlaskForm):
    name  = StringField('Name:',  validators=[DataRequired()])
    email = EmailField('Email:', validators=[Email()])
    submit = SubmitField('Submit')
```

### `validate_on_submit()` — POST + バリデーションを1行で

```python
@app.route('/', methods=['GET', 'POST'])
def input():
    form = InputForm()
    if form.validate_on_submit():   # POST かつ valid な場合のみ True
        return render_template('output.html', name=form.name.data, email=form.email.data)
    return render_template('input.html', form=form)
```

`form.validate_on_submit()` は「POST メソッド **かつ** バリデーション成功」のとき `True` になります。GET リクエストや POST でもバリデーション失敗のときは `False` です。

### テンプレートに CSRF トークンを埋め込む

```html
<form method="post" novalidate>
    {{ form.csrf_token }}
    {{ render_field(form.name) }}
    {{ render_field(form.email) }}
    {{ form.submit }}
</form>
```

`{{ form.csrf_token }}` を忘れると送信時に **400 Bad Request** になります。

### WTForms との違い

| | WTForms（`Form`） | Flask-WTF（`FlaskForm`） |
|---|---|---|
| インポート元 | `wtforms` | `flask_wtf` |
| CSRF 保護 | なし | 自動（`SECRET_KEY` が必要） |
| バリデーション | `form.validate()` | `form.validate_on_submit()` |
| フォームの生成 | `Form(request.form)` | `FlaskForm()` |

---

## 5. session + PRG パターン

> [example/app5/](example/app5/)

`session` でデータをサーバ側に保持し、POST 後にリダイレクトする **PRG（Post/Redirect/Get）パターン** を学びます。

### PRG パターンとは

```
ブラウザ  POST /  ──▶  Flask
          ◀── 302 /output ──
          GET /output  ──▶  Flask
          ◀── 200 HTML ──
```

POST 直後にリダイレクトすることで、ブラウザのリロード時に **フォームの二重送信** を防ぎます。

### session にデータを保存

```python
from flask import session, redirect, url_for

@app.route('/', methods=['GET', 'POST'])
def input():
    form = InputForm()
    if form.validate_on_submit():
        session['name']  = form.name.data
        session['email'] = form.email.data
        return redirect(url_for('output'))   # POST 後はリダイレクト

    # 再訪問時: session の値でフォームを事前入力
    if 'name' in session:
        form.name.data = session['name']
    return render_template('input.html', form=form)


@app.route('/output')
def output():
    return render_template('output.html')
```

### テンプレートで session を参照

```html
<li>Name: {{ session['name'] }}</li>
<li>Email: {{ session['email'] }}</li>
```

### ポイント

| 要素 | 説明 |
|---|---|
| `session['key'] = value` | サーバ側（Cookie）にデータを保存 |
| `redirect(url_for('output'))` | POST 後に GET リクエストへ転換 |
| `'key' in session` | session にキーが存在するか確認 |
| `SECRET_KEY` | session の署名に必要（Flask-WTF の CSRF と共有） |

`session` に保存したデータはブラウザを閉じるまで（またはクリアするまで）保持されます。

---

## 6. 練習問題

### 問題：お問い合わせフォームを作ろう

1. 以下のコマンドで [answer/app.py](answer/app.py) を実行してアプリの動作を確認する

```bash
python answer/app.py
```

2. `answer/` を見ずに、同じ機能のアプリを自分で作成する

#### 確認ポイント

`answer/app.py` を実行したとき、以下の動作になることを確認してください。

| URL | 表示内容 |
|---|---|
| `/` | お問い合わせフォーム（入力画面） |
| POST `/` | バリデーション成功時 → 送信完了画面（入力内容を表示） |
| POST `/` | バリデーション失敗時 → エラーメッセージ付きで入力画面を再表示 |

#### 仕様

| フィールド | 種類 | バリデーション |
|---|---|---|
| お名前 | `StringField` | 必須・50文字以内 |
| メールアドレス | `EmailField` | 必須・メール形式 |
| お問い合わせ種別 | `SelectField` | 一般 / サポート / その他 |
| メッセージ | `TextAreaField` | 必須・500文字以内 |

#### ヒント

- `FlaskForm` を継承して CSRF 保護を有効にする（セクション 4）
- `validate_on_submit()` で POST + バリデーションを判定する（セクション 4）
- テンプレートに `{{ form.csrf_token }}` を忘れずに書く（セクション 4）
- エラーメッセージは `form.フィールド名.errors` でループして表示する（セクション 3）
