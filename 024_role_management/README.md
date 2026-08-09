# 024 ロールベースの認可（管理者/一般）

`018_ownership_crud`〜`023_crud_api`では「自分のデータか」という**所有権**で操作を制限してきました。このチャプターでは、それとは別の認可の考え方——「どんな役割（ロール）を持っているか」——を学び、**所有者 または 管理者**なら操作できる、という組み合わせを実装します。

## 前提

| チャプター | 使う知識 |
|---|---|
| 018_ownership_crud | 所有権パターン（`user_id`で「自分のデータか」を判定） |
| 023_crud_api | 書籍APIのフルCRUD化 |

## フォルダ構成

```
024_role_management/
├── README.md
├── example/
│   └── 01_role_check.py        所有権とロールの組み合わせ（DB不使用）
└── challenge/                  023_crud_apiの続き（000_my_appに組み込む機能の変更分）
    ├── app.py / models.py / ...   023_crud_apiと同じアプリ本体（Userにis_adminを追加）
    ├── auth/views.py               最初のユーザーを自動的に管理者にする
    ├── books/views.py              所有者 または 管理者だけ編集・削除できる
    ├── api/views.py                 同上（API版）
    └── answer/
        └── app.py / models.py / ...
```

---

## 1. 所有権とロールは別の質問

> [example/01_role_check.py](example/01_role_check.py)

```python
def can_edit(user: User, post: Post) -> bool:
    """本人 または 管理者なら編集できる"""
    is_owner = user.id == post.author_id
    return is_owner or user.is_admin
```

| 質問 | 判定方法 | これまでの例 |
|---|---|---|
| これは「自分の」データか？（所有権） | `user.id == data.user_id` | `018_ownership_crud` |
| この人は「管理者」か？（ロール） | `user.is_admin` | このチャプター |

実務ではこの2つを組み合わせ、「本人 **または** 管理者」を許可する設計がよく使われます（ユーザーは自分のデータを管理でき、管理者は必要に応じて誰のデータでも管理できる）。

### 実行方法

```bash
python 024_role_management/example/01_role_check.py
```

---

## 2. Userモデルにis_adminを追加する

```python
class User(UserMixin, db.Model):
    ...
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
```

## 3. 最初のユーザーを自動的に管理者にする

新規登録フォーム（`RegisterForm`）には`is_admin`の項目を**あえて含めていません**。誰でも登録時に管理者を名乗れてしまう（権限昇格）のを防ぐためです。

その一方で、開発を始めるには管理者が最低1人必要です。ここでは「**最初に登録した1人だけ**自動的に管理者にする」というブートストラップの仕組みを使います。

```python
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        if User.query.count() == 0:
            user.is_admin = True   # 最初の1人だけ自動的に管理者にする
        db.session.add(user)
        db.session.commit()
        ...
```

| 方法 | 特徴 |
|---|---|
| 最初の1人を自動的に管理者にする | 開発・小規模運用では手軽。2人目以降は普通に登録される |
| `seed.py`のような初期データ投入スクリプトで作る | 開発用アカウントを明示的に用意できる |
| DBを直接操作する | 最も確実だが手作業が必要 |

---

## 4. 所有者 または 管理者だけが操作できるようにする

これまでは「本を取得する」ことと「所有者かどうか」を1つのクエリにまとめていました。

```python
# 018_ownership_crud〜023_crud_apiまでのやり方
book = Book.query.filter_by(id=book_id, user_id=current_user.id).first_or_404()
```

管理者は所有者でなくても操作できる必要があるため、「本を取得する」ことと「権限があるか確認する」ことを分けます。

```python
book = Book.query.get_or_404(book_id)
if book.user_id != current_user.id and not current_user.is_admin:
    abort(403)
```

JSON APIでも同じ考え方です（`404`と`403`を区別して返す）。

```python
book = Book.query.get(book_id)
if book is None:
    return jsonify({'detail': 'Book not found'}), 404
if book.user_id != current_user.id and not current_user.is_admin:
    return jsonify({'detail': 'Forbidden'}), 403
```

---

## 5. 練習問題：所有者 または 管理者だけが編集・削除できるようにしよう

> [challenge/](challenge/) — 問題 ｜ [challenge/answer/](challenge/answer/) — 解答

### 問題：ブックストアにロールベースの認可を追加しよう

`023_crud_api`で作った書籍一覧・詳細・追加・カート・チェックアウト・フルCRUD APIの機能はそのままです。ここに、最初のユーザーを自動的に管理者にする仕組みと、「所有者 または 管理者」だけが編集・削除できる制限を追加します。

```bash
cd 024_role_management/challenge
flask db init
flask db migrate -m "add is_admin to users"
flask db upgrade
python app.py
```

#### 仕様

| 問題 | 内容 |
|---|---|
| 1 | `auth/views.py`の`register()`で、`User.query.count() == 0`なら`user.is_admin = True`にする |
| 2 | `books/views.py`の`update`・`delete`を、所有者でも管理者でもなければ`abort(403)`するように変更する |
| 3 | `api/views.py`の`update_book`・`delete_book`を、所有者でも管理者でもなければ`403`を返すように変更する |

#### ヒント

- `Book.query.get_or_404(book_id)`で本を取得してから、`book.user_id != current_user.id and not current_user.is_admin`で権限チェックする（本章セクション4）
- 最初に登録した1人だけが管理者になる。2人目以降は`is_admin=False`のまま登録される（セクション3）
- テンプレート側（`books/index.html`・`books/detail.html`）の編集・削除ボタン表示、ナビゲーションの「（管理者）」表示はすでに対応済み
- 見た目やCSRF・カート・チェックアウト・APIの入力検証の仕組みは`023_crud_api`から変更不要

### 動作確認の流れ

1. 1人目を登録（自動的に管理者になる）
2. 2人目を登録してログインし、書籍を追加する
3. 3人目を登録してログインし、2人目の本を編集しようとする → **403**
4. 1人目（管理者）でログインし直し、2人目の本を編集する → **成功**

## 次のステップ

ここまでで基本チャプターは一区切りです。続きは [025_async](../025_async) で、同期処理と非同期処理の違いを学びます。
