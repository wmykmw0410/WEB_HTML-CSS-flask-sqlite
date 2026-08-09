# 023 JSON APIのフルCRUD化

`022_flask_api`で作ったJSON APIは参照専用（`GET`）でした。このチャプターでは書き込み系（`POST`・`PUT`・`DELETE`）を揃え、入力検証とAPI特有の認可（未ログイン時の401・他人のデータへの403）を学びます。

## 前提

| チャプター | 使う知識 |
|---|---|
| 015_login | Flask-Login・ログイン処理 |
| 018_ownership_crud | 所有権パターン（`user_id`で「自分のデータか」を判定） |
| 022_flask_api | `jsonify`・Blueprintでの画面/API分割・ステータスコード |

## フォルダ構成

```
023_crud_api/
├── README.md
├── example/
│   ├── app.py
│   └── api/
│       └── views.py            書籍APIのフルCRUD + 入力検証（ダミーデータ）
└── challenge/                  022_flask_apiの続き（000_my_appに組み込む機能の変更分・完成版）
    ├── app.py / models.py / ...   022_flask_apiと同じアプリ本体
    └── api/views.py                書き込み系（POST/PUT/DELETE）・入力検証・所有者チェックを追加
```

---

## 1. 入力検証（バリデーション）

> [example/api/views.py](example/api/views.py)

HTMLフォームならWTFormsが検証してくれますが、JSON APIには使えません。リクエストボディの中身を自分でチェックし、問題があれば`400 Bad Request`を返します。

```python
def validate_book_payload(data: dict) -> str | None:
    if not data.get('title'):
        return 'title is required'
    if not isinstance(data.get('price'), int):
        return 'price must be an integer'
    return None

@api_bp.post('/books')
def create_book():
    data = request.get_json()
    error = validate_book_payload(data)
    if error:
        return jsonify({'detail': error}), 400
    ...
```

| ステータスコード | 意味 | 使う場面 |
|---|---|---|
| 400 Bad Request | リクエストの中身が不正 | 必須項目が無い、型が違う など |
| 401 Unauthorized | 誰であるか確認できていない | 未ログイン |
| 403 Forbidden | 誰であるかは分かるが権限がない | 他人のデータを操作しようとした |
| 404 Not Found | 対象が存在しない | 指定したIDのデータが無い |

`401`と`403`の違いに注意してください。「ログインしていない」のか「ログインはしているが権限が無い」のかで使い分けます。

## 2. PUT — 更新

```python
@api_bp.put('/books/<int:book_id>')
def update_book(book_id: int):
    book = find_book(book_id)
    if book is None:
        return jsonify({'detail': 'Book not found'}), 404

    data = request.get_json()
    error = validate_book_payload(data)
    if error:
        return jsonify({'detail': error}), 400

    book['title'] = data['title']
    book['price'] = data['price']
    return jsonify(book)
```

`POST`が新規作成（成功時201）なのに対し、`PUT`は既存データの更新（成功時200）です。存在しないIDを指定したら`404`、検証に失敗したら`400`を返す点は`POST`と同じです。

### 実行方法

```bash
python 023_crud_api/example/app.py
```

```bash
curl http://127.0.0.1:5067/api/books
curl -X POST http://127.0.0.1:5067/api/books -H "Content-Type: application/json" -d '{"title": "新しい本", "price": 1000}'
curl -X POST http://127.0.0.1:5067/api/books -H "Content-Type: application/json" -d '{"price": 1000}'
# => 400 {"detail": "title is required"}
curl -X PUT http://127.0.0.1:5067/api/books/1 -H "Content-Type: application/json" -d '{"title": "更新後のタイトル", "price": 2200}'
curl -i -X DELETE http://127.0.0.1:5067/api/books/1
```

---

## 3. ログイン中のAPIで @login_required が使えない理由

これまでのHTMLルートでは`@login_required`を使えば、未ログイン時に自動でログイン画面へリダイレクト（302）されました。しかしJSON APIのクライアント（`curl`やモバイルアプリなど）にとって、HTMLのログイン画面へのリダイレクトは意味を持ちません。そのため、JSON APIのルートでは`@login_required`を使わず、自分で`current_user.is_authenticated`をチェックして`401`をJSONで返します。

```python
@api_bp.post('/books')
def create_book():
    if not current_user.is_authenticated:
        return jsonify({'detail': 'Login required'}), 401
    ...
```

`022_flask_api`までのAPIは同一プロセス内のBlueprintだったため、`current_user`（セッションベースの認証）がそのまま使えます。もしAPIを別プロセス（別サーバー）に分離するのであれば、この芸当は使えません（別プロセスはセッションCookieを共有できないため、APIキーやトークンなど別の認証手段が必要になります）。

## 4. CSRF保護とJSON API

`Flask-WTF`の`CSRFProtect(app)`は、デフォルトで**アプリ全体**の`POST`・`PUT`・`DELETE`にCSRF保護をかけます。HTMLフォームには`{{ form.csrf_token }}`がありますが、JSON APIのクライアントはCSRFトークンを送りません。そのままでは以下のように弾かれてしまいます。

```
400 Bad Request
The CSRF token is missing.
```

APIのBlueprintだけをCSRF保護の対象外にします。

```python
csrf = CSRFProtect(app)
csrf.exempt(api_bp)   # JSON APIはCSRF保護の対象外にする
```

**なぜAPIをCSRF対象外にしてよいのか**：CSRF攻撃は「ブラウザが自動でCookieを送ってしまう」ことを悪用します。フォーム送信を前提としないAPIクライアント（`curl`・モバイルアプリなど）はそもそもこの攻撃経路に乗らないため、CSRFトークンでの防御は意味を持ちません（本番でブラウザからJSON APIを直接叩かせる設計にする場合は、別途CORSやトークン認証などの対策が必要です）。

---

## 5. 書籍API（フルCRUD版）の使い方

> [challenge/](challenge/)

`022_flask_api`で作った書籍一覧・詳細・追加・カート・チェックアウトの機能に加えて、書籍APIが参照専用（`GET`）からフルCRUD（`GET`/`POST`/`PUT`/`DELETE`）になっています。書き込み系は`018_ownership_crud`と同じ所有権パターンで保護されており、**自分が追加した本だけ**編集・削除できます。

### 起動方法

```bash
cd 023_crud_api/challenge
flask db init
flask db migrate -m "create tables"
flask db upgrade
python app.py
```

### エンドポイント一覧

| メソッド | パス | 認可 | 説明 |
|---|---|---|---|
| GET | `/api/books` | 誰でも | 書籍一覧（`?author=`で絞り込み可） |
| GET | `/api/books/<id>` | 誰でも | 書籍詳細 |
| POST | `/api/books` | ログイン必須 | 書籍を追加（追加者が`owner`になる） |
| PUT | `/api/books/<id>` | 所有者のみ | 書籍を更新 |
| DELETE | `/api/books/<id>` | 所有者のみ | 書籍を削除 |

### 使用例

参照系は`curl`だけで確認できます。

```bash
curl http://127.0.0.1:5068/api/books
curl http://127.0.0.1:5068/api/books?author=夏目漱石

# 未ログインで書き込むと401
curl -i -X POST http://127.0.0.1:5068/api/books \
     -H "Content-Type: application/json" \
     -d '{"title": "新しい本", "author": "著者名", "price": 1000}'
# => 401 {"detail": "Login required"}
```

書き込み系はログインしたセッションが必要です。`/auth/login`はHTMLフォームなのでCSRFトークンが必須で、`curl`に手でトークンを付けるのは煩雑なため、`021_webapi`で学んだ`requests`の`Session`（Cookieを自動で保持してくれる）を使うのが簡単です。

```python
import re
import requests

BASE = 'http://127.0.0.1:5068'
session = requests.Session()

# ログインページからCSRFトークンを取り出してログインする
r = session.get(f'{BASE}/auth/login')
token = re.search(r'name="csrf_token"[^>]*value="([^"]+)"', r.text).group(1)
session.post(f'{BASE}/auth/login', data={'username': 'alice', 'password': 'pass1234', 'csrf_token': token})

# 以降は session を使えばCookieが自動で送られる
r2 = session.post(f'{BASE}/api/books', json={'title': '新しい本', 'author': '著者名', 'price': 1000})
print(r2.status_code, r2.json())   # 201 {'id': ..., 'title': '新しい本', ...}

# 必須項目が無い、または型が違うと400
r3 = session.post(f'{BASE}/api/books', json={'price': 1000})
print(r3.status_code, r3.json())   # 400 {'detail': 'title is required'}

# 更新・削除は所有者本人のみ（他人の本を指定すると403、存在しないIDは404）
book_id = r2.json()['id']
session.put(f'{BASE}/api/books/{book_id}', json={'title': '更新後のタイトル', 'author': '著者名', 'price': 1200})
session.delete(f'{BASE}/api/books/{book_id}')
```

### 実装のポイント

- `validate_book_payload(data)`：`title`・`author`が無い、または`price`が整数でなければエラーメッセージを返す共通の検証関数（本章セクション1）
- 未ログイン判定は`current_user.is_authenticated`を自分でチェックする方式（`@login_required`は使わない。セクション3）
- 所有者チェックは`book.user_id != current_user.id`（`018_ownership_crud`と同じ考え方）
- `csrf.exempt(api_bp)`を`app.py`に設定済み。これが無いと書き込み系が「CSRF token is missing」で弾かれる（セクション4）

## 次のステップ

続きは [024_role_management](../024_role_management) で、ロールベースの認可（管理者/一般）を学びます。
