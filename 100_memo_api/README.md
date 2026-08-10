# 100 メモ帳アプリ（統合アプリ）

`001`〜`025`で少しずつ積み上げてきた機能を1つにまとめたメモ帳アプリです。認証・所有権とロールによる認可・JavaScriptによる機能追加（文字数カウント・絞り込み・ピン留め）・外部APIとの連携（郵便番号から住所解決）・フルCRUDのJSON APIを、単一のFlaskアプリで提供します。

## フォルダ構成

```
app/
├── app.py               アプリ初期化・Blueprint登録・LoginManagerセットアップ
├── config.py            設定（SECRET_KEY・DBパス）
├── models.py            User（is_admin列あり）・Memo（is_pinned・postal_code・address列あり）
├── forms.py             LoginForm・RegisterForm・MemoForm
├── auth/views.py        認証（login / register / logout）
├── memos/views.py        メモ（index / detail / create / update / delete / toggle-pin）
├── api/views.py         メモのJSON API（フルCRUD）
├── static/style.css
├── static/script.js     文字数カウント・カテゴリ絞り込み・ピン留めのfetch()
└── templates/
    ├── base.html
    ├── auth/
    └── memos/
```

## 必要なパッケージ

このアプリが使っている機能ごとに、以下のパッケージが必要です。

| パッケージ | バージョン | 用途 |
|---|---|---|
| Flask | 2.3.3 | Webフレームワーク本体 |
| Flask-WTF | 1.2.2 | フォーム・CSRF保護（`009_forms`〜） |
| Flask-Login | 0.6.3 | ログイン・セッション管理（`015_login`〜） |
| Flask-SQLAlchemy | 3.0.3 | ORM（`Memo`・`User`などのモデル、`013_flask_sqlalchemy`〜） |
| Flask-Migrate | 4.0.4 | マイグレーション（`flask db`コマンド、`014_flask_migrate`〜） |
| requests | 2.33.1 | メモ登録・更新時のzipcloud API呼び出し（`021_webapi`） |

```bash
pip install Flask==2.3.3 Flask-WTF==1.2.2 Flask-Login==0.6.3 Flask-SQLAlchemy==3.0.3 Flask-Migrate==4.0.4 requests==2.33.1
```

その他のチャプターも含めた一覧は[ルートのREADME](../README.md#動作確認済みのライブラリバージョン)を参照してください。

## 起動方法

### ローカルで直接起動する場合

```bash
cd 100_memo_api/app
flask db init
flask db migrate -m "create tables"
flask db upgrade
python app.py
```

### Dockerで起動する場合

`python app.py`（開発用サーバー）の代わりに、本番向けのWSGIサーバー（`gunicorn`）で動かすDocker構成も用意しています。

```bash
cd 100_memo_api/app
docker compose up --build
```

マイグレーションの適用も含めてコンテナ起動時に自動で行われます。詳しい仕組みや`docker compose`を使わない起動方法、クラウドへのデプロイ手順は[appendix/docker.md](../appendix/docker.md)を参照してください。

### 動作確認

どちらの方法でも、ブラウザで`http://localhost:5085/auth/register`から登録してください。**最初に登録したユーザーが自動的に管理者になります**（`is_admin=True`）。2人目以降は一般ユーザーとして登録されます。

## 権限モデル

メモの編集・削除は、**追加した本人** または **管理者** のどちらかであれば行えます。

| 操作 | 誰でも | ログイン済み | 追加した本人 | 管理者 |
|---|:---:|:---:|:---:|:---:|
| メモ一覧・詳細の閲覧 | ✅ | ✅ | ✅ | ✅ |
| メモの追加 | | ✅ | ✅ | ✅ |
| メモの編集・削除・ピン留め切り替え | | | ✅ | ✅（他人のメモも可） |

## 画面の機能

| ルート | メソッド | 権限 | 説明 |
|---|---|---|---|
| `/memos/` | GET | 誰でも | メモ一覧（`?category=`で絞り込み可、JavaScriptでの絞り込みボタンも利用可） |
| `/memos/<id>` | GET | 誰でも | メモ詳細（場所が登録されていれば住所も表示） |
| `/memos/new` | GET/POST | ログイン必須 | メモ追加（郵便番号を入力すると住所を自動解決） |
| `/memos/<id>/edit` | GET/POST | 所有者 or 管理者 | メモ更新 |
| `/memos/<id>/delete` | POST | 所有者 or 管理者 | メモ削除 |
| `/memos/<id>/toggle-pin` | POST | ログイン必須 | ピン留めのON/OFF切り替え（`fetch()`で呼ばれ、JSONを返す） |
| `/auth/register` | GET/POST | 誰でも | 新規登録 |
| `/auth/login` | GET/POST | 誰でも | ログイン |
| `/auth/logout` | GET | ログイン必須 | ログアウト |

メモの登録・更新時、郵便番号が入力されていれば`requests`で[zipcloud API](https://zipcloud.ibsnet.co.jp/doc/api)を呼び出し、住所を自動解決してメモに保存します（インターネット接続が必要です）。該当住所が無い場合や通信に失敗した場合は、メモを保存せずフォーム画面に戻ります。

## JSON APIの使い方

画面と同じプロセス・同じセッションを使うため、ブラウザでログインした状態であればそのまま`fetch`等で呼び出せます。`curl`やPythonから使う場合はログインのセッションCookieを維持する必要があります。

| メソッド | パス | 権限 | 処理 |
|---|---|---|---|
| GET | `/api/memos` | 誰でも | メモ一覧（`?category=`で絞り込み可） |
| GET | `/api/memos/<id>` | 誰でも | メモ詳細 |
| POST | `/api/memos` | ログイン必須 | メモ追加 |
| PUT | `/api/memos/<id>` | 所有者 or 管理者 | メモ更新 |
| DELETE | `/api/memos/<id>` | 所有者 or 管理者 | メモ削除 |

```python
import re
import requests

BASE = 'http://127.0.0.1:5085'
session = requests.Session()

# ログインページからCSRFトークンを取り出してログインする
r = session.get(f'{BASE}/auth/login')
token = re.search(r'name="csrf_token"[^>]*value="([^"]+)"', r.text).group(1)
session.post(f'{BASE}/auth/login', data={'username': 'alice', 'password': 'pass1234', 'csrf_token': token})

# 以降は session を使えばCookieが自動で送られる
r2 = session.post(f'{BASE}/api/memos', json={'title': '新しいメモ', 'category': '仕事', 'body': '本文'})
print(r2.status_code, r2.json())   # 201

# 未ログイン・必須項目なし・他人のデータへの操作はそれぞれ 401 / 400 / 403 になる
r3 = requests.post(f'{BASE}/api/memos', json={'title': 'x', 'category': '仕事', 'body': 'y'})
print(r3.status_code)   # 401
```

**注意**：API経由の書き込み（`POST`/`PUT`/`DELETE`）はCSRF保護の対象外にしています（`csrf.exempt(api_bp)`）。JSONクライアントはCSRFトークンを送らないためです。
