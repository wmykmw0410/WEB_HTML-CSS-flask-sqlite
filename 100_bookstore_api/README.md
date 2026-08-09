# 100 ブックストア（統合アプリ）

`018_ownership_crud`〜`024_role_management`で積み上げてきた機能を1つにまとめたブックストアです。認証・所有権とロールによる認可・カートとチェックアウト（郵便番号からの住所自動解決）・フルCRUDのJSON APIを、単一のFlaskアプリで提供します。

## フォルダ構成

```
app/
├── app.py               アプリ初期化・Blueprint登録・LoginManagerセットアップ
├── config.py            設定（SECRET_KEY・DBパス）
├── models.py            User（is_admin列あり）・Book・Order・OrderItem
├── forms.py             LoginForm・RegisterForm・BookForm
├── auth/views.py        認証（login / register / logout）
├── books/views.py       書籍（index / detail / create / update / delete）
├── cart/views.py        カート・チェックアウト（session管理 + zipcloud APIで住所解決）
├── api/views.py         書籍のJSON API（フルCRUD）
├── static/style.css
└── templates/
    ├── base.html
    ├── auth/
    ├── books/
    └── cart/
```

## 必要なパッケージ

このアプリが使っている機能ごとに、以下のパッケージが必要です。

| パッケージ | バージョン | 用途 |
|---|---|---|
| Flask | 2.3.3 | Webフレームワーク本体 |
| Flask-WTF | 1.2.2 | フォーム・CSRF保護（`018_ownership_crud`〜） |
| Flask-Login | 0.6.3 | ログイン・セッション管理（`015_login`〜） |
| Flask-SQLAlchemy | 3.0.3 | ORM（`Book`・`User`などのモデル、`013_flask_sqlalchemy`〜） |
| Flask-Migrate | 4.0.4 | マイグレーション（`flask db`コマンド、`014_flask_migrate`〜） |
| requests | 2.33.1 | チェックアウト時のzipcloud API呼び出し（`021_webapi`〜） |

```bash
pip install Flask==2.3.3 Flask-WTF==1.2.2 Flask-Login==0.6.3 Flask-SQLAlchemy==3.0.3 Flask-Migrate==4.0.4 requests==2.33.1
```

その他のチャプターも含めた一覧は[ルートのREADME](../README.md#動作確認済みのライブラリバージョン)を参照してください。

## 起動方法

```bash
cd 100_bookstore_api/app
flask db init
flask db migrate -m "create tables"
flask db upgrade
python app.py
```

ブラウザで`http://localhost:5072/auth/register`から登録してください。**最初に登録したユーザーが自動的に管理者になります**（`is_admin=True`）。2人目以降は一般ユーザーとして登録されます。

## 権限モデル

書籍の編集・削除は、**追加した本人** または **管理者** のどちらかであれば行えます。

| 操作 | 誰でも | ログイン済み | 追加した本人 | 管理者 |
|---|:---:|:---:|:---:|:---:|
| 書籍一覧・詳細の閲覧 | ✅ | ✅ | ✅ | ✅ |
| 書籍の追加 | | ✅ | ✅ | ✅ |
| 書籍の編集・削除 | | | ✅ | ✅（他人の本も可） |

## 画面の機能

| ルート | メソッド | 権限 | 説明 |
|---|---|---|---|
| `/books/` | GET | 誰でも | 書籍一覧（`?author=`で絞り込み可） |
| `/books/<id>` | GET | 誰でも | 書籍詳細 |
| `/books/new` | GET/POST | ログイン必須 | 書籍追加（画像アップロード対応） |
| `/books/<id>/edit` | GET/POST | 所有者 or 管理者 | 書籍更新 |
| `/books/<id>/delete` | POST | 所有者 or 管理者 | 書籍削除 |
| `/cart/` | GET | ログイン必須 | カート表示 |
| `/cart/add/<book_id>` | POST | ログイン必須 | カートに追加 |
| `/cart/update/<book_id>` | POST | ログイン必須 | カートの数量を変更 |
| `/cart/remove/<book_id>` | POST | ログイン必須 | カートから削除 |
| `/cart/clear` | POST | ログイン必須 | カートを空にする |
| `/cart/checkout` | POST | ログイン必須 | 郵便番号から住所を解決して注文を確定 |
| `/cart/orders` | GET | ログイン必須 | 注文履歴 |
| `/auth/register` | GET/POST | 誰でも | 新規登録 |
| `/auth/login` | GET/POST | 誰でも | ログイン |
| `/auth/logout` | GET | ログイン必須 | ログアウト |

チェックアウト時は`requests`で[zipcloud API](https://zipcloud.ibsnet.co.jp/doc/api)を呼び出し、入力された郵便番号から住所を自動解決して注文に保存します（インターネット接続が必要です）。該当住所が無い場合や通信に失敗した場合は、注文を作成せずカート画面に戻ります。

## JSON APIの使い方

画面と同じプロセス・同じセッションを使うため、ブラウザでログインした状態であればそのまま`fetch`等で呼び出せます。`curl`やPythonから使う場合はログインのセッションCookieを維持する必要があります。

| メソッド | パス | 権限 | 処理 |
|---|---|---|---|
| GET | `/api/books` | 誰でも | 書籍一覧（`?author=`で絞り込み可） |
| GET | `/api/books/<id>` | 誰でも | 書籍詳細 |
| POST | `/api/books` | ログイン必須 | 書籍追加 |
| PUT | `/api/books/<id>` | 所有者 or 管理者 | 書籍更新 |
| DELETE | `/api/books/<id>` | 所有者 or 管理者 | 書籍削除 |

```python
import re
import requests

BASE = 'http://127.0.0.1:5072'
session = requests.Session()

# ログインページからCSRFトークンを取り出してログインする
r = session.get(f'{BASE}/auth/login')
token = re.search(r'name="csrf_token"[^>]*value="([^"]+)"', r.text).group(1)
session.post(f'{BASE}/auth/login', data={'username': 'alice', 'password': 'pass1234', 'csrf_token': token})

# 以降は session を使えばCookieが自動で送られる
r2 = session.post(f'{BASE}/api/books', json={'title': '新しい本', 'author': '著者名', 'price': 1000})
print(r2.status_code, r2.json())   # 201

# 未ログイン・必須項目なし・他人のデータへの操作はそれぞれ 401 / 400 / 403 になる
r3 = requests.post(f'{BASE}/api/books', json={'title': 'x', 'author': 'y', 'price': 1})
print(r3.status_code)   # 401
```

**注意**：API経由の書き込み（`POST`/`PUT`/`DELETE`）はCSRF保護の対象外にしています（`csrf.exempt(api_bp)`）。JSONクライアントはCSRFトークンを送らないためです。
