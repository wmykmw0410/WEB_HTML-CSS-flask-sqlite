# 009 フォーム

生の HTML フォームから始め、WTForms・Flask-WTF・session・ファイルアップロードまで段階的にフォーム処理を学びます。

各章は「機能の学習」と「`000_my_app`を完成させるための機能追加」の2部構成です。前者は`example/`で単体のサンプルとして学び、後者は`challenge/`でメモ帳アプリを組み立てながら取り組みます。

## 前提

- `007_with` を終えていること（`os.path.join` / `os.makedirs` などパス操作の基礎。セクション6で使用）

## 目次

1. [生のフォーム（request）](#1-生のフォームrequest) — `request.args` / `request.form` で値を受け取る
2. [WTForms 基本](#2-wtforms-基本) — Form クラスとフィールド種類
3. [WTForms バリデーション](#3-wtforms-バリデーション) — バリデーター・カスタムバリデーター
4. [Flask-WTF（CSRF 保護）](#4-flask-wtfcsrf-保護) — FlaskForm・SECRET_KEY・`validate_on_submit()`
5. [session + PRG パターン](#5-session--prg-パターン) — session によるデータ保持とリダイレクト
6. [ファイルアップロード](#6-ファイルアップロード) — FileField・secure_filename・画像の保存と表示
7. [練習問題](#7-練習問題) — お問い合わせフォーム（1〜4の総合）
8. [練習問題：メモを追加するフォーム](#8-練習問題メモを追加するフォーム) — 000_my_appへの機能追加

---

## フォルダ構成

```
009_forms/
├── README.md
├── example/
│   ├── app1/   生のフォーム（request.args / request.form）
│   ├── app2/   WTForms 基本（フィールド種類・送信結果表示）
│   ├── app3/   WTForms バリデーション（validate・カスタムバリデーター）
│   ├── app4/   Flask-WTF（FlaskForm・CSRF・validate_on_submit）
│   ├── app5/   session + POST後リダイレクト（PRGパターン）
│   └── app6/   ファイルアップロード（FileField・secure_filename）
└── challenge/            # 008_requestの続き（000_my_appに組み込む機能の追加分）
    ├── challenge.py
    ├── forms.py          # MemoForm（title/category/body）
    ├── memos.json
    ├── static/
    ├── templates/
    │   └── new_memo.html # メモ追加フォーム（完成済み）
    └── answer/
        ├── challenge.py
        ├── forms.py
        ├── memos.json
        ├── static/
        └── templates/
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

### 動作確認：GETとPOSTで何が違うかを確かめる

```bash
cd 009_forms/example/app1
python app.py
```

| 確認する操作 | 確認したいこと |
|---|---|
| ブラウザで`http://127.0.0.1:5023/get?name=Taro`にアクセスする | `Hello, Taro!`と表示される。**アドレスバーに`?name=Taro`が見えている**（GETはデータがURLの一部になる） |
| `?name=`を`?name=Jiro`に書き換えて再アクセスする | 表示が`Hello, Jiro!`に変わる。URLを直接書き換えるだけで値を変更できることを確認する |
| `http://127.0.0.1:5023/get`に`?name=...`を付けずにアクセスする | `Hello, None!`と表示される（`request.args.get('name')`が値を渡されないと`None`を返すため） |
| `http://127.0.0.1:5023/`にアクセスし、フォームに名前を入力して送信する | `Hello, ...!`と表示される。**送信後もURLは`/`のまま**（POSTのデータはURLに出ない） |
| POST送信後にブラウザの再読み込み（リロード）をする | ブラウザによっては「フォームを再送信しますか」という警告が出る（POSTの二重送信問題。対策は本章セクション5のPRGパターンで学ぶ） |

この2つを見比べることで、「GETはURLにデータが乗るので共有・ブックマークできる代わりに機微な情報には向かない」「POSTはURLに出ないが、リロードで再送信されうる」という違いが体感できます。

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

### 動作確認：フィールドの種類ごとの見た目と、送信後の値の表示

```bash
cd 009_forms/example/app2
python app.py
```

| 確認する操作 | 確認したいこと |
|---|---|
| `http://127.0.0.1:5024/`にアクセスする | `enter.html`が表示され、`Name`（テキスト）・`Age`（数値）・`Gender`（ラジオボタン）・`Area`（セレクトボックス）・`Remarks`（複数行）と、フィールドの種類ごとに違う入力要素が表示される |
| 何か値を入力（または未入力のまま）して送信する | `result.html`に遷移し、`form.フィールド名.data`で入力した値がそのまま表示される |
| **Name欄を空欄のまま**、**Ageに文字列を入力**して送信する | それでも正常に送信・表示されてしまう（**バリデーションが無いため**）。この「何を入れても通ってしまう」状態が、次のセクション3で解決する課題 |

最後の確認が重要です。ここではまだ`DataRequired()`のようなバリデーターを付けていないため、空欄や不正な値でも弾かれません。「本来は弾きたいのに弾けていない」状態を体感してから、セクション3のバリデーションに進みましょう。

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

### 動作確認：バリデーション成功時と失敗時の違い

```bash
cd 009_forms/example/app3
python app.py
```

| 確認する操作 | 確認したいこと |
|---|---|
| `http://127.0.0.1:5025/`でName欄を空欄のまま送信する | `result.html`に**進まず**、同じ入力画面が再表示され、「名前は必須です。」という赤字のエラーメッセージが出る（セクション2では素通りしていた入力が、ここでは弾かれる） |
| Ageに`17`や`101`のような範囲外の値を入力して送信する | 「18〜100 の範囲で入力してください。」と表示され、再度入力画面に戻る |
| PasswordとPassword(確認)に**違う値**を入力して送信する | 「パスワードが一致しません。」と表示される（`EqualTo`によるチェック） |
| Passwordに**英字だけ**（記号・数字を含まない）を入力して送信する | カスタムバリデーター`validate_password`のメッセージ「英字・数字・記号...をすべて含めてください。」が表示される |
| すべての項目を仕様通りに正しく入力して送信する | 今度は`result.html`に遷移し、入力した値が表示される |

**正常な状態の見分け方**：エラーがある間は「送信してもURLが変わらず、同じ入力画面にエラーメッセージだけが増える」のが正しい挙動です。逆に、不正な値なのに`result.html`に進んでしまう場合はバリデーターの設定ミスを疑ってください。

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

### 動作確認：CSRFトークンがあるとき・ないとき

```bash
cd 009_forms/example/app4
python app.py
```

| 確認する操作 | 確認したいこと |
|---|---|
| `http://127.0.0.1:5026/`で正しく入力して送信する | `output.html`に遷移し、入力した`name`・`email`が表示される（ここまではセクション3と同じ挙動） |
| テンプレートの`{{ form.csrf_token }}`を一時的にコメントアウトしてアプリを再起動し、同じフォームを送信する | 画面遷移せず**400 Bad Request**（`The CSRF token is missing.`）になる。確認後は必ずコメントアウトを元に戻す |
| フォームを開いたタブをそのままにして`app.py`を再起動し、そのタブから送信する | `SECRET_KEY = os.urandom(24)`が起動のたびに変わるため、以前発行されたCSRFトークンが無効になり、400エラーになる（**なぜSECRET_KEYの管理が重要か**を体感できるポイント） |

**正常な状態の見分け方**：CSRFトークンが有効なら「バリデーション結果に応じて画面遷移する／しない」というセクション3までと同じ挙動になります。トークンが無効・欠落しているときだけ、バリデーションの結果に関係なく400エラーで止まるのが正しい違いです。

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

### 動作確認：リダイレクトと二重送信対策

```bash
cd 009_forms/example/app5
python app.py
```

| 確認する操作 | 確認したいこと |
|---|---|
| `http://127.0.0.1:5027/`で入力して送信する | 送信後、**アドレスバーが`/output`に変わり**、入力した`name`・`email`が表示される（`/`のままだったセクション1〜4との違い） |
| `/output`が表示された状態でブラウザの再読み込み（リロード）をする | セクション1のPOSTで出た「フォームを再送信しますか」という警告が**出ない**。`/output`はGETリクエストなので、リロードしても同じデータを取得し直すだけで再送信は起きない |
| `/output`から`/`に戻る（アドレスバーに直接入力するか戻るボタン） | フォームの`Name`・`Email`欄に**さっき送信した値が入った状態**で表示される（`session`に保存した値で事前入力される） |
| ブラウザの開発者ツールでCookieを確認する | `session`という名前のCookieが発行されている（暗号署名された状態でブラウザ側に保存されている） |

**正常な状態の見分け方**：POST送信後は必ずURLが`/output`に変わることが正しい状態です。もしURLが`/`のままデータだけ表示されている場合は、`redirect(url_for('output'))`が呼ばれていない＝PRGパターンになっていない可能性があります。

### ポイント

| 要素 | 説明 |
|---|---|
| `session['key'] = value` | サーバ側（Cookie）にデータを保存 |
| `redirect(url_for('output'))` | POST 後に GET リクエストへ転換 |
| `'key' in session` | session にキーが存在するか確認 |
| `SECRET_KEY` | session の署名に必要（Flask-WTF の CSRF と共有） |

`session` に保存したデータはブラウザを閉じるまで（またはクリアするまで）保持されます。

---

## 6. ファイルアップロード

> [example/app6/](example/app6/)

`FileField` を使って画像などのファイルをアップロードし、サーバに保存して表示する方法を学びます。

### フォームの定義（FileField）

```python
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
```

`FileAllowed`は今まで使ってきた`DataRequired`や`Length`と同じ**バリデーター**の一種で、拡張子を制限します。

### テンプレートの `enctype`

ファイルを送信するフォームには `enctype="multipart/form-data"` が**必須**です。これが無いとファイルの中身が送信されません。

```html
<form method="post" enctype="multipart/form-data">
    {{ form.csrf_token }}
    {{ form.name() }}
    {{ form.image() }}
    {{ form.submit() }}
</form>
```

### ルート側の処理

```python
import os
from werkzeug.utils import secure_filename

app.config['UPLOAD_FOLDER'] = os.path.join(base_dir, 'static', 'uploads')

@app.route('/', methods=['GET', 'POST'])
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        if form.image.data and form.image.data.filename:
            filename = secure_filename(form.image.data.filename)
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            form.image.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('upload'))
    return render_template('upload.html', form=form)
```

### ポイント

| 要素 | 説明 |
|---|---|
| `form.image.data` | アップロードされたファイルオブジェクト（`FileStorage`型）。ファイルが選択されていなければ空文字列相当になる |
| `secure_filename(filename)` | ファイル名から危険な文字を除去する（Werkzeug付属）。理由は下記 |
| `os.makedirs(dir, exist_ok=True)` | 保存先ディレクトリが無ければ作成する。`exist_ok=True`で既に存在してもエラーにならない |
| `os.path.join(dir, filename)` | `007_with`で学んだパス連結。OSに依存しない形でパスを組み立てる |
| `file.save(path)` | ファイルを指定パスに保存する（`FileStorage`のメソッド） |

### なぜ `secure_filename()` が必要か

アップロードされるファイル名はユーザーの入力そのものであり、そのまま使うと**パストラバーサル攻撃**の危険があります。

```python
# 悪意あるファイル名の例
file.filename = "../../../etc/passwd"

# secure_filename() を通すと危険な文字が除去される
secure_filename("../../../etc/passwd")  # => "etc_passwd"
```

`../`のような相対パス指定や、OSで問題になる記号を取り除いてくれるため、保存前には必ず通します。

### アップロードした画像を表示する

DBには**ファイル名のみ**を保存し、表示時は`url_for('static', ...)`でパスを生成します（`static`フォルダの中身はFlaskが自動的にURLとして配信してくれます）。

```html
{% if filename %}
    <img src="{{ url_for('static', filename='uploads/' + filename) }}" width="200">
{% endif %}
```

### 動作確認：アップロードした画像がそのまま表示されるか

```bash
cd 009_forms/example/app6
python app.py
```

| 確認する操作 | 確認したいこと |
|---|---|
| `http://127.0.0.1:5028/`で名前を入力し、`.jpg`や`.png`の画像を選んでアップロードする | 送信後、選んだ画像がページにそのまま表示される |
| アップロード先のフォルダ（`example/app6/static/uploads/`）を確認する | アップロードした画像ファイルが実際に保存されている |
| 同じ操作をもう一度、**画像を選ばずに**送信する | `image`は必須にしていないため、画像無しでも送信できる（`form.image.data`が空文字列相当になり、`if`文でスキップされる） |
| `.exe`や`.pdf`など許可していない拡張子のファイルを選んで送信する | 画面遷移せず、`FileAllowed`のエラーメッセージ（「画像ファイル（jpg/png/gif）のみアップロードできます。」）が表示される |
| ファイル名に日本語や空白を含むファイルをアップロードする | `secure_filename()`によって安全なファイル名に変換されて保存される（元のファイル名と多少見た目が変わることがあるのは正常） |

**正常な状態の見分け方**：許可された拡張子の画像はアップロード後にそのまま表示され、許可されていない拡張子はエラーメッセージだけが表示されて画像は保存されません。両方を試して、成功と失敗の両方の挙動を確認しておきましょう。

---

## 7. 練習問題

### 問題：お問い合わせフォームを作ろう

1. 以下のコマンドで [answer/app.py](answer/app.py) を実行してアプリの動作を確認する

```bash
python 009_forms/answer/app.py
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

---

## 8. 練習問題：メモを追加するフォーム

> [challenge/challenge.py](challenge/challenge.py) — 問題 ｜ [challenge/answer/challenge.py](challenge/answer/challenge.py) — 解答

### 問題：メモを追加するフォームを作ろう

`008_request`で作ったメモ一覧・詳細ページ・リダイレクト（`challenge/challenge.py`にすでに実装済み）に、新しいメモを追加するフォームを追加します。フォームの定義（[challenge/forms.py](challenge/forms.py)）とテンプレート（[challenge/templates/new_memo.html](challenge/templates/new_memo.html)）は完成済みなので、Python側のルーティングだけを実装します。`MemoForm`は`title`（`StringField`）・`category`（`SelectField`）・`body`（`TextAreaField`）の3フィールドで、画像アップロードは扱いません（ファイルアップロード自体は本章セクション6の`example/app6`で学習済みです）。

```bash
python 009_forms/challenge/challenge.py
```

#### 仕様

| エンドポイント | メソッド | 処理 |
|---|---|---|
| `/memos/new` | GET | `new_memo.html`を描画する（`form`を渡す） |
| `/memos/new` | POST（バリデーション成功時） | メモデータを`memos.json`に追記して、メモ一覧（`/`）へリダイレクトする |
| `/memos/new` | POST（バリデーション失敗時） | エラーメッセージ付きで`new_memo.html`を再描画する |

#### ヒント

- `MemoForm`は`FlaskForm`を継承済みなので、CSRF保護と`validate_on_submit()`がそのまま使える（セクション4）
- `memos_list`（`memos.json`から読み込んだリスト）に新しいメモの辞書を`append`し、`memos`（idをキーにした辞書）にも追加する
- 最後に`with open(MEMOS_PATH, 'w', encoding='utf-8') as f: json.dump(memos_list, f, ...)`で`memos.json`に書き戻す（`007_with`で学んだJSON書き込み）
- 保存が終わったら`redirect(url_for('book_list'))`で一覧に戻る（PRGパターン、セクション5）

#### 動作確認の流れ

```bash
cd 009_forms/challenge
python challenge.py
```

| 確認する操作 | 確認したいこと |
|---|---|
| `http://127.0.0.1:5030/memos/new`にアクセスする | タイトル・カテゴリ・本文の3項目を持つフォームが表示される |
| タイトルまたは本文を**空欄**のまま送信する | 画面遷移せず、`new_memo.html`が再表示されてエラーメッセージが出る（`DataRequired()`によるチェック。セクション3・4と同じ挙動） |
| 3項目すべて入力して送信する | メモ一覧ページ（`/`）に**リダイレクト**され、追加したメモがURLの変化とともに表示される（PRGパターン。セクション5と同じ挙動） |
| `memos.json`をエディタで開く | 追加したメモのデータ（`title`・`category`・`body`）が新しい要素として追記されている |
| 追加したメモの詳細ページ（`/memos/<id>`）にアクセスする | `008_request`で作った詳細ページに、今追加したメモの内容が表示される |

**正常な状態の見分け方**：バリデーションに失敗している間はURLが`/memos/new`のまま変わらず、成功すると`/`にリダイレクトされる、という一貫した挙動になっているか確認してください。
