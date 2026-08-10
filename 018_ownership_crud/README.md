# 018 メモアプリの所有権とCRUD（総合）

これまで学んだ知識を組み合わせて、メモ帳アプリに**所有権**（誰が追加したメモか）と**CRUDのフルセット**（追加・一覧・詳細・編集・削除）を実装します。

`001`〜`017`ではメモ帳アプリを少しずつ積み上げてきましたが、これまでは「ログインしていれば誰でもメモを追加できる」だけで、追加・閲覧はできても編集・削除する機能自体がありませんでした。このチャプターでは、メモに「誰が追加したか」を記録し、**自分が追加したメモだけ**編集・削除できるようにします。メモ帳アプリはこの後も`019_javascript`でJavaScriptによる機能追加、`020_testing`で自動テスト、`021`〜`025`で外部API連携・JSON APIのフルCRUD化・ロールベースの認可と、引き続き同じアプリに機能を積み上げていきます（詳細は[000_my_app/README.md](../000_my_app/)を参照）。

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
メモ一覧           /memos/                  誰でも（全員分が見える）
メモ詳細           /memos/<id>              誰でも
メモ追加           /memos/new               ログイン必須
メモ編集           /memos/<id>/edit         ログイン必須（自分が追加したメモのみ）
メモ削除           /memos/<id>/delete       ログイン必須（自分が追加したメモのみ）
```

メモ**一覧・詳細は全員に公開**したままにして、**編集・削除だけ**を追加者本人に制限しているのがポイントです。「所有権 = 非公開にする」とは限らず、「操作できる人を制限する」ケースもあることを、メモ帳という現実的な題材で体感します。

## フォルダ構成と各ファイルの役割

```
example/app/
├── app.py              アプリ初期化・Blueprint 登録・LoginManager セットアップ
├── config.py           設定（SECRET_KEY・DB パス）
├── models.py           User・Memo モデル（1対多のリレーション）
├── forms.py            LoginForm・RegisterForm・MemoForm
├── auth/
│   └── views.py        認証 Blueprint（login / register / logout）
├── memos/
│   └── views.py        メモ Blueprint（index / detail / create / update / delete）
└── templates/
    ├── base.html        共通レイアウト（ナビ・フラッシュメッセージ）
    ├── auth/
    │   ├── login.html
    │   └── register.html
    └── memos/
        ├── index.html
        ├── detail.html
        ├── create.html
        └── update.html

challenge/                 000_my_appに組み込む機能の変更分
├── app.py / models.py / ...   メモ帳アプリのアプリ本体（所有権・編集・削除は未実装）
└── answer/
    └── app.py / models.py / ...   example/app/ と同じ完成版
```

---

## ステップ 1：設定・DB・モデル

### config.py — 設定をクラスで管理

```python
class Config:
    SECRET_KEY                     = 'dev-secret-key'
    SQLALCHEMY_DATABASE_URI        = 'sqlite:///instance/memos.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```

`app.config.from_object('config.Config')` でまとめて読み込みます。

### models.py — User と Memo の 1 対多

```python
class User(UserMixin, db.Model):
    id       = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    memos    = relationship('Memo', back_populates='owner')   # 1対多（User側）

class Memo(db.Model):
    id       = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title    = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    body     = db.Column(db.String(500), nullable=False)
    due_date = db.Column(db.String(50))
    user_id  = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    owner    = relationship('User', back_populates='memos')   # 多対1（Memo側）
```

`user_id` 外部キーで「誰が追加したメモか」を管理します。

### app.py — 全体の初期化

```python
db.init_app(app)
Migrate(app, db)
CSRFProtect(app)   # memos/index.html等でテンプレート内から直接 csrf_token() を呼ぶために必要

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'   # 未ログイン → ログイン画面へ

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app.register_blueprint(auth_bp)
app.register_blueprint(memos_bp)
```

### ポイント：CSRFProtect(app) が必要な理由

`LoginForm`・`MemoForm`のような`FlaskForm`は`{{ form.csrf_token }}`で自分のCSRFトークンを出力できますが、削除ボタンのような**`FlaskForm`を使わない素のHTML`<form>`**では、この仕組みが使えません。

```html
<form method="POST" action="{{ url_for('memos.delete', memo_id=memo.id) }}">
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

class MemoForm(FlaskForm):
    title    = StringField('タイトル', validators=[DataRequired(), Length(max=100)])
    category = SelectField('カテゴリ', choices=CATEGORY_CHOICES)
    body     = TextAreaField('本文', validators=[DataRequired(), Length(max=500)])
    due_date = StringField('期限（任意）', validators=[Optional(), Length(max=50)])
    submit   = SubmitField('保存する')
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

## ステップ 4：メモ Blueprint（memos/views.py）

| ルート | 処理 |
|---|---|
| `/memos/` | 全件取得（所有者にかかわらず全員分表示） |
| `/memos/<id>` | `Memo.query.get_or_404(memo_id)` で1件取得（誰のメモでも見られる） |
| `/memos/new` | `Memo(user_id=current_user.id)` で追加者を紐づける |
| `/memos/<id>/edit` | `filter_by(id=..., user_id=current_user.id)` で自分のメモのみ編集可能 |
| `/memos/<id>/delete` | 同上。`first_or_404()` で他人の ID は 404 に |

### ポイント：get_or_404() と first_or_404() の使い分け

```python
# 詳細ページ：所有者を問わないので主キー検索でよい
memo: Memo = Memo.query.get_or_404(memo_id)

# 編集・削除：自分のメモだけに絞り込んだ上で検索する
memo: Memo = Memo.query.filter_by(id=memo_id, user_id=current_user.id).first_or_404()
```

`.get_or_404(主キー)`は`013_flask_sqlalchemy`で学んだ`.query.get()`に「無ければ404」を足したショートカットです。メモ詳細は誰のメモでも見られてよいので、所有権の絞り込みをしないこの形で十分です。

一方、編集・削除は`user_id=current_user.id`を条件に加えた`.filter_by(...).first_or_404()`を使います。`user_id`を条件に含めることで、他のユーザーの`memo_id`を指定されても404になります。`.first()`とは違い`.first_or_404()`は「無ければ即404」なので、型ヒントは`Optional[Memo]`ではなく`Memo`のままで済みます。

一覧（`index`）は`filter_by(user_id=...)`を**付けていない**点に注意してください。メモは全員に見えるべきものなので、絞り込みは「編集・削除のときだけ」行います。

### ポイント：編集フォームへの既存値の埋め込み

```python
form = MemoForm(obj=memo)   # memo の title / category / body / due_date がフォームに自動セットされる
```

`obj=` に渡したオブジェクトのカラム名とフォームのフィールド名が一致していれば自動で値が入ります。`MemoForm`のフィールドはすべて文字列系（`StringField`・`SelectField`・`TextAreaField`）なので、`009_forms`で扱った`FileField`のような特別な変換は不要です。

---

## 実行方法

```bash
cd 018_ownership_crud/example/app
flask db init
flask db migrate -m "create users and memos tables"
flask db upgrade
python app.py
```

ブラウザで `http://localhost:5053/auth/register` にアクセスしてユーザーを登録してください。

### 動作確認：本人と他人でメモの編集・削除の可否が変わるか

| 確認する操作 | 確認したいこと |
|---|---|
| ユーザーA（例: `alice`）で登録・ログインし、メモを1件追加する | 一覧・詳細ページにそのメモが表示され、詳細ページに「追加したユーザー: alice」と表示される |
| そのままメモの編集・削除ボタンを押す | 編集フォームが開く／削除が成功する（自分が追加したメモなので操作できる） |
| ログアウトし、別のユーザーB（例: `bob`）で登録・ログインする | `bob`としてログインした状態になる |
| `bob`でログインしたまま、`alice`のメモの詳細ページ（`/memos/<id>`）にアクセスする | メモの内容は**見える**（一覧・詳細は誰でも閲覧可能） |
| `bob`でログインしたまま、`alice`のメモの編集URL（`/memos/<id>/edit`）に直接アクセスする | **404 Not Found**になる（`filter_by(id=..., user_id=current_user.id)`の条件に一致しないため） |
| `bob`でログインしたまま、`alice`のメモの削除を試す（フォームのURLを直接POSTする、または開発者ツールで確認する） | 同様に404になり、削除されない |

**正常な状態の見分け方**：メモの**閲覧**は誰でもでき、**編集・削除**は追加した本人でなければ404になる、という非対称な制限が正しい状態です。他人のメモが編集・削除できてしまう場合は、`update()`・`delete()`の`filter_by`に`user_id=current_user.id`が含まれているか確認してください。

---

## 練習問題：所有権とCRUDを実装しよう

> [challenge/](challenge/) — 問題 ｜ [challenge/answer/](challenge/answer/) — 解答

### 問題：メモ帳アプリに所有権とCRUDのフルセットを実装しよう

メモ一覧・詳細・追加・認証の機能はそのままです（`challenge/`にすでに実装済み）。ここに「誰が追加したか」を記録する所有権の仕組みと、編集・削除のルートを実装します。

```bash
cd 018_ownership_crud/challenge
flask db init
flask db migrate -m "create users and memos tables"
flask db upgrade
python app.py
```

#### 仕様

| 問題 | 内容 |
|---|---|
| 1 | `models.py`に`Memo.user_id`（`ForeignKey('users.id')`）と`owner`リレーション、`User.memos`リレーションを追加する |
| 2 | `memos/views.py`の`create()`で、`Memo(...)`に`user_id=current_user.id`を追加して追加者を記録する |
| 3 | `memos/views.py`に`update()`を実装する。`filter_by(id=memo_id, user_id=current_user.id).first_or_404()`で自分のメモだけ取得し、`MemoForm(obj=memo)`でフォームに事前入力する |
| 4 | `memos/views.py`に`delete()`を実装する。同様に自分のメモだけ取得して削除する |

#### ヒント

- 問題1が終わるまでは、メモ詳細ページに「追加したユーザー」が表示されない（`memo.owner`が無いため）。これは正常な状態
- `first_or_404()`は見つからなければ404で処理を中断するため、戻り値は`Optional`にならず`Memo`型のまま使える（本章ステップ4）
- 見た目やCSRFの仕組みは変更不要（`015_login`と同じパターン）

解答は`challenge/answer/`を参照してください。

### 動作確認：問題を1つずつ実装するたびに何が変わるか

```bash
cd 018_ownership_crud/challenge
python app.py
```

| 進捗 | 確認する操作 | 確認したいこと |
|---|---|---|
| 問題1完了前 | メモ詳細ページ（`http://127.0.0.1:5054/memos/<id>`）を見る | 「追加したユーザー」の表示が出ない、または`memo.owner`関連でエラーになる（ヒントにある通り正常） |
| 問題2完了後 | 新しいメモを追加してから詳細ページを見る | 「追加したユーザー」に自分のユーザー名が表示される |
| 問題3完了後 | 自分が追加したメモの編集ページ（`/memos/<id>/edit`）にアクセスする | フォームに既存の`title`・`category`・`body`・`due_date`が事前入力された状態で表示される |
| 問題3完了後 | 別ユーザーでログインし、他人のメモの編集URLに直接アクセスする | **404**になる |
| 問題4完了後 | 自分が追加したメモを削除する | 一覧から消える |
| 問題4完了後 | 別ユーザーでログインし、他人のメモの削除を試す | **404**になり、削除されない |

**正常な状態の見分け方**：問題を1つ実装するごとに、上の表の該当行の挙動だけが変化し、それ以外（メモ一覧・詳細の閲覧など）は変わらないことを確認してください。

---

## さらなる練習問題

`example/app/`（または`challenge/answer/`）をベースに、以下の機能も追加してみましょう。

| 問題 | 内容 |
|---|---|
| 1 | 登録済みのユーザー名での二重登録をブロックする（`forms.py` に `validate_username` を追加） |
| 2 | ログイン済みのユーザーが `/auth/login` にアクセスしたら `/memos/` にリダイレクトする |
| 3 | メモ一覧で自分が追加したメモにだけ「自分の投稿」のようなラベルを表示する |
| 4 | 削除フォームに確認ダイアログ（`confirm()`）以外の対策（例：削除前に確認ページを挟む）を考える |

## 次のステップ

続きは [019_javascript](../019_javascript) です。このメモ帳アプリにJavaScriptで機能を追加します。
