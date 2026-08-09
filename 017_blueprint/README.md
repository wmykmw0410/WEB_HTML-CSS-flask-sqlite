# 017 Blueprint と g オブジェクト

アプリが大きくなってきたときにルートを分割する **Blueprint** と、
リクエスト中にデータを共有する **g オブジェクト** を学びます。

`100_bookstore_api` は Blueprint で `auth` / `books` / `cart` / `api` を分割しており、
このチャプターを終えるとその構造が読めるようになります。

## 前提

- `016_typehints` を終えていること

## フォルダ構成

```
017_blueprint/
├── README.md
└── example/
    ├── 01_blueprint/             Blueprint サンプル
    │   ├── app.py
    │   ├── application/
    │   │   ├── one/views.py      Blueprint「one」のルート定義
    │   │   └── two/views.py      Blueprint「two」のルート定義
    │   ├── static/
    │   │   ├── style_one.css
    │   │   └── style_two.css
    │   └── templates/
    │       ├── base.html
    │       ├── home.html
    │       ├── one/index.html
    │       └── two/index.html
    └── 02_g.py                   g オブジェクトサンプル
└── challenge/                    016_typehintsの続き（000_my_appに組み込む機能の変更分）
    ├── app.py
    ├── models.py
    ├── forms.py
    ├── books.json
    ├── application/
    │   ├── books/views.py         書籍関連ルート（Blueprint「books」）
    │   └── auth/views.py          認証関連ルート（Blueprint「auth」）
    ├── static/
    ├── templates/
    └── answer/
        ├── app.py
        ├── models.py
        ├── forms.py
        ├── books.json
        ├── application/
        │   ├── books/views.py
        │   └── auth/views.py
        ├── static/
        └── templates/
```

---

## 1. Blueprint

### Blueprint とは

ルートやテンプレートをまとめて **部品化** する仕組みです。
`app.py` に全ルートを書き続けると肥大化するため、機能単位で分割します。

```
Blueprint なし                Blueprint あり
──────────────────────────    ────────────────────────────
app.py                        app.py（登録のみ）
  @app.route('/one/...')        application/one/views.py
  @app.route('/two/...')        application/two/views.py
  ...（どんどん増える）
```

### Blueprint の定義

```python
# application/one/views.py
from flask import Blueprint, render_template

one_bp = Blueprint('one_app', __name__, url_prefix='/one')

@one_bp.route('/')
def show_template() -> str:
    return render_template('one/index.html')
```

| 引数 | 説明 |
|---|---|
| `'one_app'` | Blueprint の名前（`url_for` のプレフィックスに使う） |
| `__name__` | テンプレート・静的ファイルの基点となるモジュール名 |
| `url_prefix='/one'` | このBlueprintの全ルートに付くプレフィックス |

### app.py への登録

```python
from flask import Flask
from application.one.views import one_bp
from application.two.views import two_bp

app = Flask(__name__)
app.register_blueprint(one_bp)
app.register_blueprint(two_bp)
```

### url_for での参照

Blueprint 内のビュー関数を参照するときは `ブループリント名.関数名` の形式にします。

```python
url_for('one_app.show_template')   # → /one/
url_for('two_app.show_template')   # → /two/
url_for('show_home')               # app.py のルート（プレフィックスなし）
```

### 実行方法

```bash
python 017_blueprint/example/01_blueprint/app.py
```

| URL | 表示 |
|---|---|
| `http://localhost:5049/` | ホーム（App1 / App2 へのリンク） |
| `http://localhost:5049/one/` | App1（h1 が赤） |
| `http://localhost:5049/two/` | App2（h1 が青） |

---

## 2. g オブジェクト

> [example/02_g.py](example/02_g.py)

### g とは

**1リクエストの間だけ** データを保持できる Flask の特殊オブジェクトです。
`before_request` でセットしておくと、同じリクエスト内の全ルートから参照できます。

```python
from flask import Flask, g

app = Flask(__name__)

@app.before_request
def before_request() -> None:
    g.user = get_user()   # リクエスト開始時に一度だけ実行

@app.route('/')
def do_hello() -> str:
    return f'Hello, {g.user["name"]}'   # g 経由で参照

@app.route('/morning')
def do_morning() -> str:
    return f'Good morning, {g.user["name"]}'
```

### before_request とは

デコレーター `@app.before_request` を付けた関数は、ルートのビュー関数が呼ばれる**直前**に必ず実行されます。

```
リクエスト受信
    ↓
before_request()  ← g.user をセット
    ↓
ルートのビュー関数  ← g.user を使う
    ↓
レスポンス返却
    ↓
g の中身はリセット（次のリクエストでは参照できない）
```

### g の用途

| 使い方 | 例 |
|---|---|
| ログイン中のユーザー情報をセット | `g.user = load_user_from_session()` |
| DB コネクションの管理 | `g.db = get_db_connection()` |
| リクエストをまたいで共有したくない一時データ | 認証情報、計測タイマーなど |

### g vs session の違い

| | `g` | `session` |
|---|---|---|
| 有効範囲 | 1リクエスト内のみ | ブラウザを閉じるまで（Cookie） |
| 保存場所 | サーバーのメモリ | クライアントの Cookie |
| 用途 | リクエスト内の一時データ | ログイン状態など永続データ |

### current_app とは

`g`と同じ「今処理中のリクエストに関する情報」を扱う仕組みとして、`current_app`（今動いている`Flask`アプリ本体へのプロキシ）もあります。ファイルを扱うルートでは、保存先のパスを組み立てるのによく使われます。

```python
from flask import current_app

static_img_dir = os.path.join(current_app.root_path, 'static', 'img')
```

`current_app.root_path`は、そのBlueprint（や`app.py`）を定義しているファイルの場所に関係なく、**アプリ本体（`app = Flask(__name__)`）が置かれているディレクトリ**を返します。Blueprintのように複数ファイルにルートが分かれていても、`app`インスタンスを直接importせずにアプリの情報へアクセスできるのがポイントです。

---

## 3. 練習問題

| 問題 | 内容 | ヒント |
|---|---|---|
| 1 | `01_blueprint/` に Blueprint「three」を追加し `/three/` で Hello が返るようにする | `three_bp = Blueprint(...)` を定義して `app.register_blueprint` |
| 2 | `02_g.py` の `before_request` でアクセス時刻（`datetime.now()`）を `g.time` にセットし、全ルートで表示する | `from datetime import datetime` |

---

## 4. 練習問題：書籍データの管理アプリをBlueprintで分割しよう

> [challenge/app.py](challenge/app.py) — 問題 ｜ [challenge/answer/app.py](challenge/answer/app.py) — 解答

### 問題：1ファイルにまとまったルートをBlueprintで分割しよう

`016_typehints`で作った書籍一覧・詳細・追加フォーム・新規登録・ログイン・ログアウトの機能はそのままです（新しい機能は追加しません）。1ファイルにまとまっていたルートを、`books`（書籍関連）と`auth`（認証関連）の2つのBlueprintに分割し、`g`オブジェクトの使い方も練習します。

`Book`・`User`モデルは循環importを避けるため`models.py`に切り出し済みです（`db = SQLAlchemy()`を`app.py`側で`db.init_app(app)`する構成。本章セクション1、および`013_flask_sqlalchemy`で説明した`db.init_app(app)`パターンの実践例です）。

```bash
cd 017_blueprint/challenge
flask db init
flask db migrate -m "create books and users tables"
flask db upgrade
python app.py
```

#### 仕様

| 問題 | 内容 |
|---|---|
| 1 | `application/books/views.py`の`books_bp`と`application/auth/views.py`の`auth_bp`を`app.py`で`app.register_blueprint()`する |
| 2 | `login_manager.login_view`と各ビューの`redirect(url_for(...))`を`'auth.login'`・`'books.book_list'`のようなBlueprint形式のエンドポイント名に書き換える |
| 3 | `register.html`・`login.html`内の`url_for('login')`・`url_for('register')`も同様にBlueprint形式に書き換える |
| 4 | `app.py`の`before_request`で`g.access_time`に現在時刻をセットし、`base.html`のフッターに表示する |

#### ヒント

- 問題1が終わるまでは、書籍一覧を含めすべてのルートが404になる（Blueprintが未登録のため）。これは正常な状態
- 問題2・3を後回しにしたまま問題1だけ終えると、`/`は表示できても`/login`や`/register`を開いた時点で`werkzeug.routing.exceptions.BuildError`が発生する。このエラーメッセージは`Did you mean 'auth.login' instead?`のように正しいエンドポイント名を教えてくれるので、参考にする
- Blueprint内のエンドポイント名は`ブループリント名.関数名`（例:`books.book_list`）（本章セクション1）
- `g`は`before_request`でセットすると同じリクエスト内のテンプレートからも`{{ g.access_time }}`で参照できる（セクション2）
- 見た目やCSRF・ファイルアップロードの仕組み、ルーティングやビジネスロジックは`016_typehints`から変更不要（ファイル分割とBlueprint化のみ）
