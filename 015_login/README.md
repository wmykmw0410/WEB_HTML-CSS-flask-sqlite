# 015 ログイン機能

Flask アプリにログイン・ログアウト・新規登録機能を実装します。
このチャプターを終えると `100_bookstore_api` のログイン部分（`auth/`）が読めるようになります。

## 前提

- `013_flask_sqlalchemy` を終えていること（db.Model / db.session を理解している）
- `014_flask_migrate` を終えていること（flask db コマンドを使える）

## 使うライブラリ

| ライブラリ | 用途 | インストール |
|---|---|---|
| Flask-WTF | フォーム生成・CSRF 保護 | `pip install Flask-WTF` |
| Flask-Login | ログイン状態（セッション）の管理 | `pip install Flask-Login` |
| Werkzeug | パスワードのハッシュ化（任意） | Flask に付属（追加不要） |

```bash
pip install Flask-WTF Flask-Login
```

## フォルダ構成

```
015_login/
├── README.md
├── example/
│   ├── 01_flask_wtf.py       フォーム定義・バリデーション（Flask-WTF）
│   ├── 02_app/               統合：ログイン機能付きアプリ
│   │   ├── app.py
│   │   ├── models.py
│   │   ├── forms.py
│   │   └── templates/
│   │       ├── base.html
│   │       ├── index.html
│   │       ├── login.html
│   │       ├── register.html
│   │       └── mypage.html
│   └── 03_password_hash.py   パスワードのハッシュ化（Werkzeug）← 応用（任意）
├── question/                  練習問題
│   ├── 02_app/                 問題（example/02_app をベースに機能を追加する）
│   └── answer/
│       └── 02_app/             解答
└── challenge/                 014_flask_migrateの続き（000_my_appに組み込む機能の変更分）
    ├── challenge.py
    ├── forms.py
    ├── books.json
    ├── static/
    ├── templates/
    └── answer/
        ├── challenge.py
        ├── forms.py
        ├── books.json
        ├── static/
        └── templates/
```

---

## 1. Flask-WTF フォーム

> [example/01_flask_wtf.py](example/01_flask_wtf.py)

Flask-WTF を使うと、フォームの定義・バリデーション・CSRF 保護をクラスで管理できます。

### フォームクラスの定義

```python
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField('ユーザー名', validators=[DataRequired(), Length(max=50)])
    password = PasswordField('パスワード', validators=[DataRequired()])
    submit   = SubmitField('ログイン')
```

| フィールド | HTML の `type` | 用途 |
|---|---|---|
| `StringField` | `text` | 文字入力 |
| `PasswordField` | `password` | パスワード（マスク表示） |
| `SubmitField` | `submit` | 送信ボタン |
| `TextAreaField` | `textarea` | 複数行テキスト |

| バリデーター | 役割 |
|---|---|
| `DataRequired()` | 未入力を禁止 |
| `Length(min, max)` | 文字数を制限 |
| `EqualTo('field')` | 別フィールドと一致するか確認（パスワード確認欄に使う） |

### ルート側の使い方

```python
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():   # POST かつ全バリデーション通過
        username = form.username.data
        password = form.password.data
        # ...認証処理...
    return render_template('login.html', form=form)
```

| メソッド / 属性 | 説明 |
|---|---|
| `form.validate_on_submit()` | `POST` かつ全フィールドのバリデーション成功なら `True` |
| `form.フィールド名.data` | ユーザーが入力した値 |
| `form.フィールド名.errors` | バリデーションエラーのリスト |

### テンプレート側

```html
<form method="post">
    {{ form.hidden_tag() }}
    {{ form.username.label }}
    {{ form.username() }}
    {% for error in form.username.errors %}
        <p style="color:red">{{ error }}</p>
    {% endfor %}
    {{ form.password.label }}
    {{ form.password() }}
    {{ form.submit() }}
</form>
```

| テンプレート構文 | 説明 |
|---|---|
| `form.hidden_tag()` | CSRF トークンを `<input type="hidden">` で出力（必須） |
| `form.フィールド名()` | `<input>` タグを出力 |
| `form.フィールド名.label` | `<label>` タグを出力 |
| `form.フィールド名.errors` | バリデーションエラーのリスト |

### CSRF とは

**CSRF（クロスサイトリクエストフォージェリ）** は、悪意あるサイトがユーザーになりすましてリクエストを送る攻撃です。Flask-WTF はフォームごとに秘密トークンを発行・検証するため、`form.hidden_tag()` を入れるだけで防御できます。

---

## 2. Flask-Login

### セットアップ

```python
from flask_login import LoginManager

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'   # 未ログイン時のリダイレクト先ビュー名
```

### User モデルに UserMixin を追加

```python
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id       = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)

    def set_password(self, raw):
        self.password = generate_password_hash(raw)   # ハッシュ化して保存

    def check_password(self, raw):
        return check_password_hash(self.password, raw)  # 照合
```

`UserMixin` を継承すると、Flask-Login が必要とする下表のメソッドが自動で付与されます。

| メソッド / プロパティ | 意味 | UserMixin のデフォルト |
|---|---|---|
| `is_authenticated` | ログイン済みか | `True` |
| `is_active` | 有効なアカウントか | `True` |
| `is_anonymous` | 匿名ユーザーか | `False` |
| `get_id()` | ユーザーの識別子を返す | `str(self.id)` |

`generate_password_hash` / `check_password_hash` の詳細は [5. 応用（任意）](#5-応用任意パスワードのハッシュ化) を参照してください。

### user_loader の登録

セッション復元のために、ID からユーザーを取得する関数を1つ登録します。

```python
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
```

Flask-Login はページを開くたびにセッションから `user_id` を取り出してこの関数を呼び、`current_user` に設定します。

### ログイン・ログアウト

```python
from flask_login import login_user, logout_user

login_user(user)   # セッションに user_id を記録（ログイン）
logout_user()      # セッションから user_id を削除（ログアウト）
```

### ページ保護と current_user

```python
from flask_login import login_required, current_user

@app.route('/mypage')
@login_required           # 未ログインなら login_view にリダイレクト
def mypage():
    return f'こんにちは、{current_user.username} さん'
```

| API | 説明 |
|---|---|
| `login_user(user)` | ログイン処理（セッション記録） |
| `logout_user()` | ログアウト処理（セッション削除） |
| `@login_required` | 未ログインをブロックするデコレーター |
| `current_user` | 現在ログイン中の User オブジェクト（未ログイン時は `AnonymousUser`） |
| `current_user.is_authenticated` | ログイン済みなら `True` |

### flash() — 次の画面に1回だけメッセージを渡す

登録失敗・ログイン失敗のような「リダイレクト後に結果を伝えたい」場面では、`flash()`を使います。

```python
from flask import flash, redirect, url_for

@app.route('/register', methods=['GET', 'POST'])
def register():
    ...
    flash('登録が完了しました。ログインしてください。')
    return redirect(url_for('login'))
```

`flash()`はメッセージを`session`に一時保存するだけで、画面には何も表示しません。表示するのはテンプレート側の役目です。

```html
{% for msg in get_flashed_messages() %}
    <p class="flash">{{ msg }}</p>
{% endfor %}
```

`get_flashed_messages()`はメッセージを**取り出すと同時にsessionから削除**するため、次のリクエストでは表示されません（「1回だけ表示する」を実現する仕組み）。`base.html`のように共通レイアウトに書いておけば、どのルートで`flash()`しても表示されます。

---

## 3. 統合：ログイン機能付きアプリ

> [example/02_app/](example/02_app/)

1・2 を組み合わせた最小構成のアプリです。

### ルート一覧

| ルート | メソッド | 説明 |
|---|---|---|
| `/` | GET | トップページ（ログイン不要） |
| `/register` | GET / POST | 新規登録 |
| `/login` | GET / POST | ログイン |
| `/logout` | GET | ログアウト |
| `/mypage` | GET | マイページ（`@login_required`） |

### 型ヒント：`Optional[User]`

ここで`Optional`という型ヒントの書き方が初めて登場します。`.first()`は該当するレコードが無ければ`None`を返すため、戻り値は「`User`かもしれないし`None`かもしれない」型になります。型ヒントの体系的な説明は`016_typehints`で扱います。

```python
from typing import Optional

user: Optional[User] = User.query.filter_by(username=form.username.data).first()
if user and user.check_password(form.password.data):
    login_user(user)
```

`if user and ...`という書き方自体は今までと同じですが、`Optional[User]`という型ヒントを付けることで「ここは`None`チェックが必要な値だ」ということがコードを読むだけで分かるようになります。

`load_user`（Flask-Loginがセッションからユーザーを復元する関数）も同様に、該当ユーザーが存在しない場合`None`を返しうるため`-> Optional[User]`という戻り値の型ヒントを付けています。

```python
@login_manager.user_loader
def load_user(user_id: str) -> Optional[User]:
    return User.query.get(int(user_id))
```

### 実行方法

```bash
cd 015_login/example/02_app
flask db init
flask db migrate -m "create users table"
flask db upgrade
python app.py
```

ブラウザで `http://localhost:5042` にアクセスしてください。

### ファイル構成

```
02_app/
├── app.py       LoginManager セットアップ・ルート定義
├── models.py    User モデル（UserMixin 継承）
├── forms.py     LoginForm・RegisterForm
└── templates/
    ├── base.html
    ├── index.html
    ├── login.html
    ├── register.html
    └── mypage.html
```

---

## 4. 練習問題

> [question/02_app/](question/02_app/) — 問題 ｜ [question/answer/02_app/](question/answer/02_app/) — 解答

`question/02_app/`（`example/02_app/`と同じ内容のコピー）をベースに以下の機能を追加してみましょう。

```bash
cd 015_login/question/02_app
flask db init
flask db migrate -m "create users table"
flask db upgrade
python app.py
```

| 問題 | 内容 | ヒント |
|---|---|---|
| 1 | ユーザー登録フォームにパスワード確認欄（`confirm`）を追加する | `EqualTo('password')` バリデーター |
| 2 | ログイン成功時にフラッシュメッセージを表示する | `flash('ログインしました')` |
| 3 | ログイン済みのユーザーが `/login` にアクセスしたらトップにリダイレクトする | `current_user.is_authenticated` |
| 4 | 重複ユーザー名での登録をブロックする | `User.query.filter_by(username=...).first()` |

解答は `question/answer/02_app/` を参照してください。

---

## 5. 練習問題：書籍データの管理にログイン機能を組み込もう

> [challenge/challenge.py](challenge/challenge.py) — 問題 ｜ [challenge/answer/challenge.py](challenge/answer/challenge.py) — 解答

### 問題：ログインしたユーザーだけが書籍を追加できるようにしよう

`014_flask_migrate`で作った書籍一覧・詳細・書籍追加フォーム・リダイレクト（`challenge/challenge.py`にすでに実装済み）に、Flask-Login を組み込みます。新規登録・ログイン・ログアウトの機能を実装し、`/books/new`をログイン必須にします。

`Migrate(app, db)`はすでに設定済みなので、`User`モデルを定義したら`flask db migrate`でマイグレーションファイルを生成し、`books`テーブルに加えて`users`テーブルを追加してください。

```bash
cd 015_login/challenge

# 問題1：User モデルと LoginManager を用意したら、マイグレーションで users テーブルを追加する
flask --app challenge db migrate -m "create users table"
flask --app challenge db upgrade
python challenge.py

# 問題2〜4を実装したら、ブラウザで新規登録→ログイン→書籍追加を確認
```

#### 仕様

| 問題 | 内容 |
|---|---|
| 1 | `User`モデル（id / username / password）を`UserMixin`付きで定義し、`user_loader`を実装する |
| 2 | `/register`で`RegisterForm`を使ってユーザーを作成し、`/login`にリダイレクトする |
| 3 | `/login`で認証して`login_user()`する。`/logout`で`logout_user()`する |
| 4 | `/books/new`に`@login_required`を追加する |

#### ヒント

- `User`モデルの`set_password`/`check_password`は`werkzeug.security`の`generate_password_hash`/`check_password_hash`を使う（本章セクション2）
- `login_manager.user_loader`に登録する関数は`User.query.get(int(user_id))`を返す（セクション2）
- 認証は`User.query.filter_by(username=...).first()`で取得したユーザーと`check_password()`の結果で判定する（セクション3）
- フォーム（`forms.py`の`RegisterForm`・`LoginForm`）とテンプレート（`register.html`・`login.html`・`base.html`のナビゲーション）はすでに用意されているので、Pythonコードのみ変更すればよい
- 見た目やCSRF・ファイルアップロードの仕組みは`014_flask_migrate`から変更不要

---

## 6. 応用（任意）：パスワードのハッシュ化

> [example/03_password_hash.py](example/03_password_hash.py)

`set_password` / `check_password` の中で使っている Werkzeug の仕組みを学びます。
パスワードをそのまま DB に保存するのは危険です。**ハッシュ化** して保存し、ログイン時に照合します。

```python
from werkzeug.security import generate_password_hash, check_password_hash

raw = 'mypassword123'

# ハッシュ化（DB に保存する値）
hashed = generate_password_hash(raw)
print(hashed)
# → 'pbkdf2:sha256:600000$...'  毎回異なるランダムな文字列

# 照合（ログイン時）
print(check_password_hash(hashed, 'mypassword123'))  # True
print(check_password_hash(hashed, 'wrongpass'))      # False
```

| 関数 | 引数 | 戻り値 | 呼ぶタイミング |
|---|---|---|---|
| `generate_password_hash(password)` | 平文パスワード | ハッシュ文字列 | ユーザー登録時 |
| `check_password_hash(hash, password)` | ハッシュ, 平文 | `True` / `False` | ログイン時の照合 |

### なぜハッシュが必要か

| 問題 | ハッシュ化による対策 |
|---|---|
| DB が流出したとき平文パスワードが見える | ハッシュから元のパスワードを復元できない（一方向変換） |
| 全ユーザーのハッシュが同じになると一括解析される | ソルト（ランダム値）が付くため、同じパスワードでも毎回ハッシュが異なる |

---

## 次のステップ

続きは [016_typehints](../016_typehints) で、このチャプターで使った`Optional[User]`のような型ヒントを体系的に学びます。その後 [017_blueprint](../017_blueprint) に進みます。
