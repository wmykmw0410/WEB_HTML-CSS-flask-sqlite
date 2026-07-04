# 001 Flask 基礎

Flask の基本を学ぶサンプル集です。Hello World から始まり、ルーティング・動的ルーティングまでを順番に学べます。

## 目次

1. [Hello Sample — Flask 最小構成](#1-hello-sample--flask-最小構成) — Flask の最小構成を理解する
2. [Routing Sample — 基本ルーティング](#2-routing-sample--基本ルーティング) — 複数ルートを定義する
3. [Dynamic Routing Sample — 動的ルーティング](#3-dynamic-routing-sample--動的ルーティング) — URL パラメータで動的なルーティングを実装する
4. [HTTP メソッド（GET / POST）](#4-http-メソッドget--post) — GET と POST の使い分けを理解する
5. [リダイレクト](#5-リダイレクト) — redirect と url_for でページ遷移を実装する
6. [エラーハンドリング](#6-エラーハンドリング) — abort とエラーハンドラでエラーページを制御する

---

## フォルダ構成

```
001_flask_basic/
├── README.md
└── example/
    ├── app1.py            # Flask 最小構成・Hello World
    ├── app2.py            # 複数ルートの定義
    ├── app3.py            # URLパラメータ・コンバータ
    ├── app4.py            # HTTP メソッド（GET / POST / PUT / DELETE）
    ├── app5.py            # リダイレクト
    └── app6.py            # エラーハンドリング
```

---

## 1. Hello Sample — Flask 最小構成

> [example/app1.py](example/app1.py) | [README](example/README.md)

Flask アプリケーションの最小構成です。インスタンス生成・ルーティング・起動の3ステップを学びます。

### 用語：Web の基本的な仕組み

ブラウザが Web サーバにリクエストを送り、サーバがレスポンスを返すことで Web ページが表示されます。

```
ブラウザ  ──── リクエスト ────▶  Web サーバ（Flask）
         ◀──── レスポンス ────
```

| 用語 | 説明 |
|---|---|
| **HTTP** | Web 上でデータをやり取りするためのルール（プロトコル） |
| **リクエスト** | ブラウザなどのクライアントがサーバへ送るデータ |
| **レスポンス** | サーバがクライアントへ返すデータ（HTML・JSON など） |

### 用語：URL の構造

`http://127.0.0.1:5000/list` を例に各部分の意味を示します。

```
http://  127.0.0.1  :5000  /list
──────   ─────────  ─────  ─────
スキーム  ホスト     ポート  パス
```

| 部分 | 説明 |
|---|---|
| **スキーム** | 通信方式（`http` / `https`） |
| **ホスト** | サーバの場所（`127.0.0.1` は自分のPC） |
| **ポート** | サーバの窓口番号（Flask のデフォルトは `5000`） |
| **パス** | サーバ上のリソースの場所 |

```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return '<h1>Hello World!</h1>'

if __name__ == '__main__':
    app.run()
```

### ポイント

| 要素 | 説明 |
|---|---|
| `Flask(__name__)` | アプリインスタンスの生成 |
| `@app.route("/")` | URL とビュー関数の紐付け |
| `app.run(debug=True, port=5001)` | 開発サーバーの起動（`http://127.0.0.1:5001`） |

---

## 2. Routing Sample — 基本ルーティング

> [example/app2.py](example/app2.py)

複数の URL に対してそれぞれビュー関数を定義する方法を学びます。

### 用語：ルーティング・エンドポイント

| 用語 | 説明 |
|---|---|
| **ルーティング** | URL のパスとビュー関数を紐付ける仕組み。`@app.route("/list")` で `/list` へのアクセス時に対応する関数が呼ばれる |
| **エンドポイント** | アプリケーションがリクエストを受け付ける URL。Flask では `@app.route()` で定義したパスがエンドポイントになる |

```python
@app.route("/")
def index():
    return '<h1>Top Page</h1>'

@app.route("/list")
def item_list():
    return '<h1>Item List Page</h1>'

@app.route("/detail")
def item_detail():
    return '<h1>Item Detail Page</h1>'
```

### エンドポイント一覧

| URL | 関数名 | 説明 |
|---|---|---|
| `/` | `index` | トップページ |
| `/list` | `item_list` | アイテム一覧ページ |
| `/detail` | `item_detail` | アイテム詳細ページ |

---

## 3. Dynamic Routing Sample — 動的ルーティング

> [example/app3.py](example/app3.py)

URL に変数を含める動的ルーティングを学びます。コンバータを使うことで受け取る値の型を指定できます。

### 用語：パスパラメータ・クエリパラメータ

URL でサーバにデータを渡す方法は大きく2種類あります。

```
http://127.0.0.1:5000/items/42?sort=asc
                              ──  ────────
                              ↑   クエリパラメータ（? 以降）
                              パスパラメータ（パスの一部）
```

| 種類 | 書き方 | 用途 | Flask での取得方法 |
|---|---|---|---|
| **パスパラメータ** | `/items/42` | リソースを特定する ID など | `<int:id>` でルートに埋め込み、引数で受け取る |
| **クエリパラメータ** | `/items?sort=asc` | 絞り込み・並び順など補助的な情報 | `request.args.get('sort')` |

パスパラメータはリソースの **識別** に、クエリパラメータはリソースの **絞り込みや並び替え** に使うのが一般的な設計です。

```python
# コンバータなし（str として受け取る）
@app.route('/dynamic/<value>')
def dynamic_default(value):
    return f'<h1>渡された値は[{value}]です</h1>'

# int コンバータ（整数として受け取る）
@app.route('/dynamic2/<int:number>')
def dynamic_converter(number):
    return f'<h1>渡された値は[{number}]です</h1>'

# 複数の値を受け取る
@app.route('/dynamic3/<value>/<int:number>')
def dynamic_converter_multiple(value, number):
    return f'<h1>渡された値は[{value}]と[{number}]です</h1>'
```

### コンバータ一覧

| コンバータ | 型 | 例 |
|---|---|---|
| （なし）| `str` | `/dynamic/hello` |
| `int:` | `int` | `/dynamic2/42` |
| `float:` | `float` | `/dynamic/<float:value>` |
| `path:` | `str`（`/` を含む） | `/dynamic/<path:value>` |

### クエリパラメータ — `request.args`

`?key=value` の形で URL に付加して渡します。`request.args.get('key', デフォルト値)` で取得します。

```python
from flask import Flask, request

# 単一のクエリパラメータ  例) /search?q=flask
@app.route('/search')
def search():
    keyword = request.args.get('q', '')
    return f'<h1>検索キーワード: [{keyword}]</h1>'

# 複数のクエリパラメータ  例) /items?sort=name&order=asc
@app.route('/items')
def items():
    sort  = request.args.get('sort', 'id')
    order = request.args.get('order', 'asc')
    return f'<h1>並び順: {sort} / {order}</h1>'

# パスパラメータ + クエリパラメータの組み合わせ
# 例) /categories/books?sort=price&order=desc
@app.route('/categories/<category>')
def category_items(category):
    sort  = request.args.get('sort', 'id')
    order = request.args.get('order', 'asc')
    return f'<h1>カテゴリ: {category} / 並び順: {sort} / {order}</h1>'
```

#### ポイント

| 書き方 | 説明 |
|---|---|
| `request.args.get('key')` | 値がなければ `None` を返す |
| `request.args.get('key', 'default')` | 値がなければ第2引数のデフォルト値を返す |
| 複数パラメータ | `&` でつなぐ（例: `?sort=name&order=asc`） |

---

## 4. HTTP メソッド（GET / POST）

> [example/app4.py](example/app4.py)

`@app.route()` の `methods` 引数で受け付ける HTTP メソッドを指定します。デフォルトは GET のみです。

```python
from flask import Flask, request

app = Flask(__name__)

# GET : アイテム一覧を取得
@app.route('/items', methods=['GET'])
def get_items():
    return '<h1>GET: アイテム一覧を取得</h1>'

# POST : アイテムを新規作成
@app.route('/items', methods=['POST'])
def create_item():
    return '<h1>POST: アイテムを新規作成</h1>'

# PUT : アイテムを更新（全体置換）
@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    return f'<h1>PUT: アイテム {item_id} を更新（全体置換）</h1>'

# DELETE : アイテムを削除
@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    return f'<h1>DELETE: アイテム {item_id} を削除</h1>'

# メソッド判定の例
@app.route('/method-check', methods=['GET', 'POST', 'PUT', 'DELETE'])
def method_check():
    return f'<h1>リクエストメソッド: {request.method}</h1>'
```

### ポイント

| メソッド | 用途 | 例 |
|---|---|---|
| `GET` | データの取得・ページ表示 | 一覧・詳細の表示 |
| `POST` | データの新規作成・送信 | フォームの送信 |
| `PUT` | データの更新（全体置換） | レコードの上書き |
| `DELETE` | データの削除 | レコードの削除 |

`request.method` で現在のリクエストメソッドを判定できます。

### 用語：デバッグモード

`app.run(debug=True)` で有効になります。コードを変更すると自動でサーバが再起動され、エラー発生時にはブラウザ上に詳細情報が表示されます。**本番環境では必ず無効にします。**

### ブラウザの開発者ツールで HTTP メソッドを確認する手順

1. `python app4.py` でサーバーを起動する
2. ブラウザで `http://127.0.0.1:5000/form` を開く
3. 開発者ツールを開く（`F12` または `Cmd + Option + I`）
4. **Network** タブを選択する
5. ページをリロードする（`F5` または `Cmd + R`）
6. Network タブに表示されたリクエスト一覧から `form` をクリックする
7. **Headers** タブの **General** セクションに `Request Method: GET` と表示される

ブラウザは GET しか送れないため、POST / PUT / DELETE は curl で確認する。

```bash
# GET
curl http://127.0.0.1:5000/items

# POST
curl -X POST http://127.0.0.1:5000/items

# PUT
curl -X PUT http://127.0.0.1:5000/items/1

# DELETE
curl -X DELETE http://127.0.0.1:5000/items/1
```

---

## 5. リダイレクト

> [example/app5.py](example/app5.py)

`redirect()` でブラウザを別の URL へ転送します。`url_for()` と組み合わせると関数名からURLを動的に生成できます。

```python
from flask import Flask, redirect, url_for

app = Flask(__name__)

# 内部URLへリダイレクト（url_for で関数名を指定）
@app.route('/old')
def old_page():
    return redirect(url_for('new_page'))

@app.route('/new')
def new_page():
    return '<h1>New Page</h1>'

# 外部URLへリダイレクト
@app.route('/go-flask')
def go_flask():
    return redirect('https://flask.palletsprojects.com/')
```

### ポイント

| 関数 | 説明 |
|---|---|
| `redirect(url)` | 指定した URL へリダイレクト（デフォルト: 302） |
| `url_for('関数名')` | ビュー関数名から URL を逆引き生成 |

---

## 6. エラーハンドリング

> [example/app6.py](example/app6.py)

### 用語：HTTP ステータスコード

HTTP リクエストを受信した Web サーバからのレスポンスの状態を示します。ステータスコードは3桁の数字で表され、リクエストが成功したかどうか、エラーが発生したかどうかなどを示します。

| コード | 分類 | 説明 |
|---|---|---|
| 1xx | 情報 | リクエストを受け取り処理継続中 |
| 2xx | 成功 | リクエストを正常に処理 |
| 3xx | リダイレクト | 追加アクションが必要 |
| 4xx | クライアントエラー | クライアント側に問題あり |
| 5xx | サーバーエラー | サーバー側に問題あり |

`abort()` で意図的にエラーを発生させ、`@app.errorhandler()` でエラーページをカスタマイズします。

```python
from flask import Flask, abort

app = Flask(__name__)

# 意図的に 403 エラーを発生させる
@app.route('/admin')
def admin():
    abort(403)

# 404 エラーハンドラ
@app.errorhandler(404)
def not_found(e):
    return '<h1>404 - ページが見つかりません</h1>', 404

# 403 エラーハンドラ
@app.errorhandler(403)
def forbidden(e):
    return '<h1>403 - アクセス権限がありません</h1>', 403

# 500 エラーハンドラ
@app.errorhandler(500)
def internal_server_error(e):
    return '<h1>500 - サーバーエラーが発生しました</h1>', 500
```

### ポイント

| 関数・デコレータ | 説明 |
|---|---|
| `abort(ステータスコード)` | 処理を中断し指定のエラーを発生させる |
| `@app.errorhandler(コード)` | 特定のステータスコードに対するカスタム処理を登録 |

レスポンスの戻り値は `(HTMLテキスト, ステータスコード)` のタプルで返します。

---

## 練習問題

### 問題：書籍管理アプリのルーティングを実装しよう

以下の仕様を満たす Flask アプリ `practice.py` を作成してください。

#### 仕様

| エンドポイント | メソッド | 処理 |
|---|---|---|
| `/` | GET | `<h1>書籍管理アプリ</h1>` を返す |
| `/books` | GET | `<h1>書籍一覧</h1>` を返す |
| `/books/<int:book_id>` | GET | `<h1>書籍 {book_id} の詳細</h1>` を返す |
| `/books` | POST | `<h1>書籍を登録しました</h1>` を返す |
| `/old-books` | GET | `/books` へリダイレクトする |
| 上記以外の URL | — | `<h1>404 - ページが見つかりません</h1>` を返す（ステータスコード 404） |

#### ヒント

- `redirect()` と `url_for()` を使って `/old-books` → `/books` のリダイレクトを実装する
- 同じパス `/books` に GET と POST を別々の関数で定義する場合、それぞれ `methods=['GET']` / `methods=['POST']` を指定する
- 404 エラーハンドラは `@app.errorhandler(404)` で登録する

解答例 → [answer/answer.py](answer/answer.py)


