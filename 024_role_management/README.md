# 024 ロールベースの認可（管理者/一般）

`018_ownership_crud`で学んだ所有権パターンをもとに、これまでは「自分のメモか」という**所有権**だけでメモの編集・削除を制限してきました。しかし実際のアプリでは、不適切な投稿を消したり、トラブル対応をしたりするために「**管理者**は他人のデータも操作できる」という仕組みが必要になることがよくあります。このチャプターでは、所有権とは別の認可の考え方——「どんな役割（ロール）を持っているか」——を学び、**所有者 または 管理者**なら操作できる、という組み合わせを実装します。

## 前提

| チャプター | 使う知識 |
|---|---|
| 018_ownership_crud | 所有権パターン（`user_id`で「自分のデータか」を判定） |
| 023_crud_api | JSON APIのフルCRUD化・入力検証 |

## フォルダ構成

```
024_role_management/
├── README.md
├── example/
│   └── 01_role_check.py        所有権とロールの組み合わせ（DB不使用）
└── challenge/                  023_crud_apiの続き（000_my_appに組み込む機能の変更分）
    ├── app.py / models.py / ...   023_crud_apiと同じアプリ本体（Userにis_adminを追加）
    ├── auth/views.py               最初のユーザーを自動的に管理者にする
    ├── memos/views.py              所有者 または 管理者だけ編集・削除できる
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

### 動作確認：本人・管理者・他人で`can_edit`の結果がどう変わるか

| 確認する操作 | 確認したいこと |
|---|---|
| スクリプトをそのまま実行する | `alice（本人）が編集できるか: True`・`admin（管理者）が編集できるか: True`・`bob（他人）が編集できるか: False`の3行が表示される |
| 最後の行を確認する | `assert`がすべて通り、「所有権とロール、どちらか一方でも条件を満たせば編集できることを確認しました。」まで表示される（`AssertionError`が出ずに最後まで実行できることが正常） |
| `can_edit`の`return is_owner or user.is_admin`を試しに`return is_owner and user.is_admin`（`or`→`and`）に書き換えて実行する | `admin（管理者）が編集できるか: False`に変わり、`assert can_edit(admin, post) is True`で`AssertionError`が出る。確認後は必ず`or`に戻す |

**正常な状態の見分け方**：所有者(`alice`)と管理者(`admin`)は`True`、どちらでもない`bob`だけが`False`になるのが正しい状態です。管理者なのに`False`になる場合は`or`条件の実装ミスを疑ってください。

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

`018_ownership_crud`以来、「メモを取得する」ことと「所有者かどうか」を1つのクエリにまとめていました。

```python
# これまでのやり方（018_ownership_crudと同じ考え方）
memo = Memo.query.filter_by(id=memo_id, user_id=current_user.id).first_or_404()
```

管理者は所有者でなくても操作できる必要があるため、「メモを取得する」ことと「権限があるか確認する」ことを分けます。

```python
memo = Memo.query.get_or_404(memo_id)
if memo.user_id != current_user.id and not current_user.is_admin:
    abort(403)
```

JSON APIでも同じ考え方です（`404`と`403`を区別して返す）。

```python
memo = Memo.query.get(memo_id)
if memo is None:
    return jsonify({'detail': 'Memo not found'}), 404
if memo.user_id != current_user.id and not current_user.is_admin:
    return jsonify({'detail': 'Forbidden'}), 403
```

---

## 5. 練習問題：所有者 または 管理者だけが編集・削除できるようにしよう

> [challenge/](challenge/) — 問題 ｜ [challenge/answer/](challenge/answer/) — 解答

### 問題：メモ帳アプリにロールベースの認可を追加しよう

メモ一覧・詳細・追加・編集・削除・ピン留め・フルCRUD APIの機能は`challenge/`にすでに実装済みです（`023_crud_api`と同じ）。ここに、最初のユーザーを自動的に管理者にする仕組みと、「所有者 または 管理者」だけが編集・削除できる制限を追加します（管理者は不適切なメモを削除するなど、モデレーションの役割を担います）。

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
| 2 | `memos/views.py`の`update`・`delete`を、所有者でも管理者でもなければ`abort(403)`するように変更する |
| 3 | `api/views.py`の`update_memo`・`delete_memo`を、所有者でも管理者でもなければ`403`を返すように変更する |

#### ヒント

- `Memo.query.get_or_404(memo_id)`でメモを取得してから、`memo.user_id != current_user.id and not current_user.is_admin`で権限チェックする（本章セクション4）
- 最初に登録した1人だけが管理者になる。2人目以降は`is_admin=False`のまま登録される（セクション3）
- テンプレート側（`memos/index.html`・`memos/detail.html`）の編集・削除ボタン表示、ナビゲーションの「（管理者）」表示はすでに対応済み
- 見た目やCSRF・ピン留め・APIの入力検証の仕組みはすでに実装済みで変更不要

### 動作確認の流れ

1. 1人目を登録（自動的に管理者になる）
2. 2人目を登録してログインし、メモを追加する
3. 3人目を登録してログインし、2人目のメモを編集しようとする → **403**
4. 1人目（管理者）でログインし直し、2人目のメモを編集する → **成功**

以下は`challenge/answer`（完成版）を実際に動かして、上記の流れをより具体的に確認する手順です。

```bash
cd 024_role_management/challenge/answer
flask db init
flask db migrate -m "add is_admin to users"
flask db upgrade
python app.py
```

### 動作確認：一般ユーザー同士は403、管理者は成功する

| 確認する操作 | 確認したいこと |
|---|---|
| `http://127.0.0.1:5084/auth/register`で1人目（例：`admin`）を登録してログインする | ナビゲーションなどに管理者であることが分かる表示が出る（`User.query.count() == 0`の間に登録した唯一のユーザーが`is_admin=True`になるため。本章セクション3） |
| ログアウトし、2人目（例：`alice`）を登録・ログインして、メモを1件追加する | 通常のユーザーとして自分のメモを作成できる（管理者表示は出ない） |
| ログアウトし、3人目（例：`bob`）を登録・ログインして、`alice`のメモの編集ページ（`http://127.0.0.1:5084/memos/<memo_id>/edit`）に直接アクセスする | **403 Forbidden**の画面が表示される。削除操作（詳細ページの削除ボタン）を試しても同様に403になる |
| ログアウトし、1人目（管理者）でログインし直して、同じ`alice`のメモの編集ページにアクセスし、内容を更新する | 403にならず編集フォームが開き、更新も**成功**する（`memos.detail`にリダイレクトされ「メモを更新しました。」と表示される） |
| 管理者でログインしたまま、同じメモを削除する | 削除も成功し、メモ一覧（`http://127.0.0.1:5084/memos/`）から消える |
| （API版）`bob`としてログイン中のセッションで`PUT http://127.0.0.1:5084/api/memos/<memo_id>`を叩く（`requests.Session`でログインする方法は`023_crud_api`の使用例と同じ） | ステータスコード**403**と`{"detail": "Forbidden"}`が返る |
| 同じリクエストを1人目（管理者）のセッションで実行する | ステータスコード**200**で更新後のメモのJSONが返る（`memo.user_id != current_user.id and not current_user.is_admin`の条件を、管理者は`is_admin`側で回避できるため。本章セクション4） |

**正常な状態の見分け方**：同じ「他人のメモを編集・削除する」という操作でも、実行したユーザーが管理者かどうかだけで結果が変わるのが正しい状態です。一般ユーザー同士なら画面は403エラー・APIは`{"detail": "Forbidden"}`(403)、管理者ならどちらも成功（画面は更新後の詳細ページ、APIは200/204）になります。一般ユーザーなのに他人のメモを編集できてしまう場合は、`memos/views.py`または`api/views.py`の権限チェック漏れを疑ってください。

## 次のステップ

ここまでで基本チャプターは一区切りです。続きは [025_async](../025_async) で、同期処理と非同期処理の違いを学びます。
