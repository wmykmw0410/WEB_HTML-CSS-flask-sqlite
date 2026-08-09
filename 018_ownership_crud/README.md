# 018 書籍アプリの所有権とCRUD（総合）

これまで学んだ知識を組み合わせて、`017_blueprint`のブックストアに**所有権**（誰が追加した本か）と**CRUDのフルセット**（追加・一覧・詳細・編集・削除）を実装します。

`017_blueprint`までのブックストアは「ログインしていれば誰でも書籍を追加できる」だけで、追加・閲覧はできても編集・削除する機能自体がありませんでした。このチャプターでは、書籍に「誰が追加したか」を記録し、**自分が追加した書籍だけ**編集・削除できるようにします。

## 前提

| チャプター | 使う知識 |
|---|---|
| 013_flask_sqlalchemy | db.Model・db.session |
| 014_flask_migrate | flask db コマンド |
| 015_login | Flask-Login・Flask-WTF |
| 016_typehints | Optional・Union などの型ヒント |
| 017_blueprint | Blueprint |

## 作るもの

```
機能               ルート                   制限
──────────────────────────────────────────────────
新規登録           /auth/register           誰でも
ログイン           /auth/login              誰でも
ログアウト         /auth/logout             ログイン必須
書籍一覧           /books/                  誰でも（全員分が見える）
書籍詳細           /books/<id>              誰でも
書籍追加           /books/new               ログイン必須
書籍編集           /books/<id>/edit         ログイン必須（自分が追加した本のみ）
書籍削除           /books/<id>/delete       ログイン必須（自分が追加した本のみ）
```

書籍**一覧・詳細は全員に公開**したままにして、**編集・削除だけ**を追加者本人に制限しているのがポイントです。「所有権 = 非公開にする」とは限らず、「操作できる人を制限する」ケースもあることを、bookstore という現実的な題材で体感します。

## フォルダ構成と各ファイルの役割

```
example/app/
├── app.py              アプリ初期化・Blueprint 登録・LoginManager セットアップ
├── config.py           設定（SECRET_KEY・DB パス）
├── models.py           User・Book モデル（1対多のリレーション）
├── forms.py            LoginForm・RegisterForm・BookForm
├── auth/
│   └── views.py        認証 Blueprint（login / register / logout）
├── books/
│   └── views.py        書籍 Blueprint（index / detail / create / update / delete）
└── templates/
    ├── base.html        共通レイアウト（ナビ・フラッシュメッセージ）
    ├── auth/
    │   ├── login.html
    │   └── register.html
    └── books/
        ├── index.html
        ├── detail.html
        ├── create.html
        └── update.html

challenge/                 017_blueprintの続き（000_my_appに組み込む機能の変更分）
├── app.py / models.py / ...   017_blueprintと同じアプリ本体（所有権・編集・削除は未実装）
└── answer/
    └── app.py / models.py / ...   example/app/ と同じ完成版
```

---

## ステップ 1：設定・DB・モデル

### config.py — 設定をクラスで管理

```python
class Config:
    SECRET_KEY                     = 'dev-secret-key'
    SQLALCHEMY_DATABASE_URI        = 'sqlite:///instance/books.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```

`app.config.from_object('config.Config')` でまとめて読み込みます。

### models.py — User と Book の 1 対多

```python
class User(UserMixin, db.Model):
    id       = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    books    = relationship('Book', back_populates='owner')   # 1対多（User側）

class Book(db.Model):
    id      = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title   = db.Column(db.String(100), nullable=False)
    author  = db.Column(db.String(100), nullable=False)
    price   = db.Column(db.Integer, nullable=False)
    genre   = db.Column(db.String(50))
    image   = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    owner   = relationship('User', back_populates='books')   # 多対1（Book側）
```

`user_id` 外部キーで「誰が追加した本か」を管理します。

### app.py — 全体の初期化

```python
db.init_app(app)
Migrate(app, db)
CSRFProtect(app)   # books/index.html等でテンプレート内から直接 csrf_token() を呼ぶために必要

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'   # 未ログイン → ログイン画面へ

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app.register_blueprint(auth_bp)
app.register_blueprint(books_bp)
```

### ポイント：CSRFProtect(app) が必要な理由

`LoginForm`・`BookForm`のような`FlaskForm`は`{{ form.csrf_token }}`で自分のCSRFトークンを出力できますが、削除ボタンのような**`FlaskForm`を使わない素のHTML`<form>`**では、この仕組みが使えません。

```html
<form method="POST" action="{{ url_for('books.delete', book_id=book.id) }}">
    <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
    <button type="submit">削除</button>
</form>
```

この`csrf_token()`（テンプレート内で呼べる関数）は、`CSRFProtect(app)`を実行して初めてJinjaのグローバル関数として使えるようになります。`CSRFProtect(app)`を書き忘れると、`{{ form.csrf_token }}`を使うページは動きますが、この素のフォームを使うページは`jinja2.exceptions.UndefinedError`（`csrf_token`が未定義）になります。

---

## ステップ 2：フォーム（forms.py）

```python
class LoginForm(FlaskForm):
    username = StringField('ユーザー名', validators=[DataRequired(), Length(max=50)])
    password = PasswordField('パスワード', validators=[DataRequired()])
    submit   = SubmitField('ログイン')

class BookForm(FlaskForm):
    title  = StringField('タイトル', validators=[DataRequired(), Length(max=100)])
    author = StringField('著者', validators=[DataRequired(), Length(max=100)])
    price  = IntegerField('価格（円）', validators=[DataRequired(), NumberRange(min=1)])
    genre  = StringField('ジャンル', validators=[Optional(), Length(max=50)])
    image  = FileField('表紙画像', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'], '...')])
    submit = SubmitField('保存する')
```

`RegisterForm` は `LoginForm` に加えて `confirm`（`EqualTo('password')`）を持ちます。

---

## ステップ 3：認証 Blueprint（auth/views.py）

| ルート | 処理 |
|---|---|
| `/auth/login` | フォームを検証 → `User.query.filter_by(username=...).first()` → `check_password` → `login_user` |
| `/auth/register` | `User` を生成 → `set_password`（ハッシュ化）→ `db.session.add` → commit |
| `/auth/logout` | `logout_user()` → ログイン画面へ |

### ポイント：ログイン判定

```python
user: Optional[User] = User.query.filter_by(username=form.username.data).first()
if user and user.check_password(form.password.data):
    login_user(user)
```

`user` が `None`（存在しない）か `check_password` が `False`（パスワード不一致）なら認証失敗です。`015_login`で使った`Optional[User]`をここでも付けています。

---

## ステップ 4：書籍 Blueprint（books/views.py）

| ルート | 処理 |
|---|---|
| `/books/` | 全件取得（所有者にかかわらず全員分表示） |
| `/books/<id>` | `Book.query.get_or_404(book_id)` で1件取得（誰の本でも見られる） |
| `/books/new` | `Book(user_id=current_user.id)` で追加者を紐づける |
| `/books/<id>/edit` | `filter_by(id=..., user_id=current_user.id)` で自分の本のみ編集可能 |
| `/books/<id>/delete` | 同上。`first_or_404()` で他人の ID は 404 に |

### ポイント：get_or_404() と first_or_404() の使い分け

```python
# 詳細ページ：所有者を問わないので主キー検索でよい
book: Book = Book.query.get_or_404(book_id)

# 編集・削除：自分の本だけに絞り込んだ上で検索する
book: Book = Book.query.filter_by(id=book_id, user_id=current_user.id).first_or_404()
```

`.get_or_404(主キー)`は`013_flask_sqlalchemy`で学んだ`.query.get()`に「無ければ404」を足したショートカットです。書籍詳細は誰の本でも見られてよいので、所有権の絞り込みをしないこの形で十分です。

一方、編集・削除は`user_id=current_user.id`を条件に加えた`.filter_by(...).first_or_404()`を使います。`user_id`を条件に含めることで、他のユーザーの`book_id`を指定されても404になります。`.first()`とは違い`.first_or_404()`は「無ければ即404」なので、型ヒントは`Optional[Book]`ではなく`Book`のままで済みます。

一覧（`index`）は`filter_by(user_id=...)`を**付けていない**点に注意してください。書籍は全員に見えるべきものなので、絞り込みは「編集・削除のときだけ」行います。

### ポイント：編集フォームへの既存値の埋め込み

```python
form = BookForm(obj=book)   # book の title / author / price / genre がフォームに自動セットされる
```

`obj=` に渡したオブジェクトのカラム名とフォームのフィールド名が一致していれば自動で値が入ります。ただし`image`は`FileField`なので、`obj=`によって`book.image`の**文字列**（ファイル名）がそのまま`form.image.data`に入ってしまいます。新しい画像が選択されたかどうかは`FileStorage`かどうかで判定します。

```python
from werkzeug.datastructures import FileStorage

if isinstance(form.image.data, FileStorage) and form.image.data.filename:
    book.image = _save_image(form)   # 新しい画像が選択されたときだけ保存し直す
```

---

## 実行方法

```bash
cd 018_ownership_crud/example/app
flask db init
flask db migrate -m "create users and books tables"
flask db upgrade
python app.py
```

ブラウザで `http://localhost:5053/auth/register` にアクセスしてユーザーを登録してください。

---

## 練習問題：所有権とCRUDを実装しよう

> [challenge/](challenge/) — 問題 ｜ [challenge/answer/](challenge/answer/) — 解答

### 問題：017_blueprintのブックストアに所有権とCRUDのフルセットを実装しよう

`017_blueprint`で作った書籍一覧・詳細・追加・認証の機能はそのままです（`challenge/`にすでに実装済み）。ここに「誰が追加したか」を記録する所有権の仕組みと、編集・削除のルートを実装します。

```bash
cd 018_ownership_crud/challenge
flask db init
flask db migrate -m "create users and books tables"
flask db upgrade
python app.py
```

#### 仕様

| 問題 | 内容 |
|---|---|
| 1 | `models.py`に`Book.user_id`（`ForeignKey('users.id')`）と`owner`リレーション、`User.books`リレーションを追加する |
| 2 | `books/views.py`の`create()`で、`Book(...)`に`user_id=current_user.id`を追加して追加者を記録する |
| 3 | `books/views.py`に`update()`を実装する。`filter_by(id=book_id, user_id=current_user.id).first_or_404()`で自分の本だけ取得し、`BookForm(obj=book)`でフォームに事前入力する |
| 4 | `books/views.py`に`delete()`を実装する。同様に自分の本だけ取得して削除する |

#### ヒント

- 問題1が終わるまでは、書籍詳細ページに「追加したユーザー」が表示されない（`book.owner`が無いため）。これは正常な状態
- `first_or_404()`は見つからなければ404で処理を中断するため、戻り値は`Optional`にならず`Book`型のまま使える（本章ステップ4）
- 画像の差し替えは`isinstance(form.image.data, FileStorage) and form.image.data.filename`のときだけ行う。`obj=book`によって`image`に既存のファイル名（文字列）が入ってしまうため
- 見た目やCSRF・ファイルアップロードの仕組みは`017_blueprint`から変更不要

解答は`challenge/answer/`を参照してください。

---

## 100_bookstore_api との対応

`100_bookstore_api`は、このアプリを土台に`019_cart`〜`024_role_management`までの機能を積み上げた最終形です。

| | このアプリ（018） | 100_bookstore_api（最終形） |
|---|---|---|
| 権限モデル | **所有権**のみ（`user_id`で「自分の本か」を判定） | **所有権 + ロール**（追加した本人 または 管理者）（`024_role_management`で追加） |
| 誰が書籍を編集できるか | 追加した本人のみ | 追加した本人 または 管理者 |
| 書籍一覧・詳細 | 全員に公開 | 同じ |
| カート・チェックアウト | なし | あり（`019_cart`で追加） |
| JSON API | なし | あり、フルCRUD（`022_flask_api`・`023_crud_api`で追加） |

「自分のデータだけ操作できる（所有権）」と「特定の役割の人だけ操作できる（ロール）」は、どちらも認可（authorization）の実装パターンですが目的が異なります。`100_bookstore_api`では「所有者 **または** 管理者」という形でこの2つを組み合わせています。

---

## さらなる練習問題

`example/app/`（または`challenge/answer/`）をベースに、以下の機能も追加してみましょう。

| 問題 | 内容 |
|---|---|
| 1 | 登録済みのユーザー名での二重登録をブロックする（`forms.py` に `validate_username` を追加） |
| 2 | ログイン済みのユーザーが `/auth/login` にアクセスしたら `/books/` にリダイレクトする |
| 3 | 書籍一覧で自分が追加した本にだけ「自分の投稿」のようなラベルを表示する |
| 4 | 削除フォームに確認ダイアログ（`confirm()`）以外の対策（例：削除前に確認ページを挟む）を考える |
