# 008 request・クエリパラメータ・HTTPメソッド

Flaskの`request`オブジェクトを使って、クエリパラメータの絞り込みとHTTPメソッドの使い分けを学びます。

各章は「機能の学習」と「`000_my_app`を完成させるための機能追加」の2部構成です。前者は`example/`で単体のサンプルとして学び、後者は`challenge/`でメモ帳アプリを組み立てながら取り組みます。

### requestオブジェクトとは

`request`はFlaskが用意しているオブジェクトで、今処理中のHTTPリクエストの情報をまとめて持っています。ビュー関数の引数として渡されるわけではなく、`from flask import request`でインポートすれば、リクエスト処理中のどこからでも参照できます。

| 属性 | 内容 | 学習チャプター |
|---|---|---|
| `request.args` | クエリパラメータ（`?key=value`） | `004_flask_basic`・本章セクション2 |
| `request.method` | HTTPメソッド（GET/POST/PUT/DELETEなど） | 本章セクション1 |
| `request.form` | フォームから送信されたデータ | `009_forms` |
| `request.path` | リクエストされたパス（例: `/books/1`） | — |
| `request.headers` | リクエストヘッダー | — |

`request.args`はすでに`004_flask_basic`で使いましたが、`request`オブジェクトにはそれ以外にも、リクエストに関するさまざまな情報が入っています。この章では`request.method`を扱います。

## 目次

1. [HTTPメソッド（GET / POST / PUT / DELETE）](#1-httpメソッドget--post--put--delete)
2. [クエリパラメータでの絞り込み](#2-クエリパラメータでの絞り込み)
3. [パスパラメータでの1件取得](#3-パスパラメータでの1件取得)
4. [練習問題](#4-練習問題)

---

## フォルダ構成

```
008_request/
├── README.md
├── example/
│   ├── app1.py            # HTTPメソッド（GET / POST / PUT / DELETE・request.method）
│   ├── app2.py            # クエリパラメータでの絞り込み（request.args）
│   └── app3.py            # パスパラメータでの1件取得（jsonify・404）
└── challenge/               # 007_withの続き（000_my_appに組み込む機能の追加分）
    ├── challenge.py
    ├── memos.json          # 007_withで学んだJSON読み込みで使うデータ
    ├── static/
    ├── templates/          # base.htmlを継承する構成（006_jinja2の練習問題より）
    └── answer/
        ├── challenge.py
        ├── books.json
        ├── static/
        └── templates/
```

---

## 1. HTTPメソッド（GET / POST / PUT / DELETE）

> [example/app1.py](example/app1.py)

`@app.route()`の`methods`引数で受け付けるHTTPメソッドを指定します。デフォルトはGETのみです。

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

`request.method`で現在のリクエストメソッドを判定できます。

### ブラウザは GET しか送れない

ブラウザのアドレスバーへの直接入力や`<a href="">`は常にGETリクエストです。POST / PUT / DELETEを試すにはcurlを使います。

```bash
# GET
curl http://127.0.0.1:5018/items

# POST
curl -X POST http://127.0.0.1:5018/items

# PUT
curl -X PUT http://127.0.0.1:5018/items/1

# DELETE
curl -X DELETE http://127.0.0.1:5018/items/1
```

### 実行方法

```bash
python 008_request/example/app1.py
```

### 動作確認：メソッドごとに返る内容と、許可されていないメソッドの挙動

| 確認する操作 | 確認したいこと |
|---|---|
| `curl http://127.0.0.1:5018/items` | `GET: アイテム一覧を取得`と表示される |
| `curl -X POST http://127.0.0.1:5018/items` | `POST: アイテムを新規作成`と表示される |
| `curl -X PUT http://127.0.0.1:5018/items/1` | `PUT: アイテム 1 を更新（全体置換）`と表示される |
| `curl -X DELETE http://127.0.0.1:5018/items/1` | `DELETE: アイテム 1 を削除`と表示される |
| `curl -i -X POST http://127.0.0.1:5018/items/1`（`/items/<id>`にPOSTを送ってみる） | ボディは表示されず`405 METHOD NOT ALLOWED`が返る（`/items/<int:item_id>`は`PUT`と`DELETE`しか`methods`に指定していないため） |
| `curl -X GET http://127.0.0.1:5018/method-check`と`curl -X POST http://127.0.0.1:5018/method-check`を続けて実行する | `リクエストメソッド: `の後ろが`GET`→`POST`と、実際に送ったメソッドに応じて変わる |

**正常な状態の見分け方**：`methods`引数で許可していないメソッドでアクセスすると、200 OKではなく`405 Method Not Allowed`が返るのが正しい挙動です。想定外のメソッドでも200が返ってしまう場合は、`methods=[...]`の指定漏れを疑ってください。

---

## 2. クエリパラメータでの絞り込み

> [example/app2.py](example/app2.py)

`request.args.get()`を使い、クエリパラメータでデータを絞り込む実践的な例です。パラメータが無ければ全件を返します。

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

books = [
    {"id": "1", "title": "python", "category": "technical"},
    {"id": "3", "title": "進撃の巨人", "category": "comics"},
]

@app.route('/books/')
def get_books():
    category = request.args.get('category')

    if category is None:
        result = books
    else:
        result = [book for book in books if book["category"] == category]

    return jsonify(result)
```

### jsonifyとは

`jsonify()`は、Pythonの辞書やリストを正しい形式のJSONレスポンスに変換するFlaskの関数です。単に文字列に変換するだけでなく、レスポンスの`Content-Type`ヘッダーを自動で`application/json`に設定してくれます。ブラウザやAPIクライアントに「これはJSONです」と正しく伝えるために必要です。

### ポイント

| 要素 | 説明 |
|---|---|
| `request.args.get('category')` | クエリパラメータを取得。無ければ `None` |
| `category is None` | 未指定時は全件、指定時は絞り込みという分岐 |
| リスト内包表記 | `[book for book in books if ...]` で条件に合う要素だけ抽出 |
| `jsonify(result)` | Pythonのリスト/辞書をJSONレスポンスに変換して返す |

### 確認方法

```bash
curl http://127.0.0.1:5019/books/
# => 全件

curl "http://127.0.0.1:5019/books/?category=comics"
# => category が comics の書籍のみ
```

### 動作確認：カテゴリ指定の有無で結果がどう変わるか

```bash
cd 008_request/example
python app2.py
```

| 確認する操作 | 確認したいこと |
|---|---|
| `curl http://127.0.0.1:5019/books/` | `books`の全6件がJSON配列で返る |
| `curl "http://127.0.0.1:5019/books/?category=comics"` | `category`が`comics`の2件（`進撃の巨人`・`DBおやじ`）だけが返る |
| `curl "http://127.0.0.1:5019/books/?category=technical"` | `category`が`technical`の2件（`python`・`はじめてのプログラミング`）だけが返る |
| `curl "http://127.0.0.1:5019/books/?category=novel"`（存在しないカテゴリ） | 空の配列`[]`が返る（該当する本が無いだけでエラーにはならない） |
| `curl -i "http://127.0.0.1:5019/books/"`でレスポンスヘッダーを確認する | `Content-Type: application/json`になっている（`jsonify()`が自動で設定するヘッダー） |

**正常な状態の見分け方**：`category`を指定しなければ常に全件、指定すれば一致する件数だけが返り、一致が0件でもエラーにならず空配列`[]`が返るのが正しい挙動です。

---

## 3. パスパラメータでの1件取得

> [example/app3.py](example/app3.py)

`3. Dynamic Routing Sample`（`004_flask_basic`）で学んだパスパラメータを使い、IDを指定して1件のデータを取得する実践的な例です。該当データが無い場合は404を返します。

```python
from flask import Flask, jsonify

app = Flask(__name__)

users = {
    1: "Tom",
    2: "Ken",
    3: "John",
}

@app.route('/users/<int:user_id>')
def get_user(user_id):
    username = users.get(user_id)

    if username is None:
        return jsonify({"detail": "User not found"}), 404

    return jsonify({"user_id": user_id, "username": username})
```

### ポイント

| 要素 | 説明 |
|---|---|
| `<int:user_id>` | パスパラメータを`int`として受け取る |
| `jsonify({...})` | 辞書をJSONレスポンスに変換する |
| `return ..., 404` | タプルの第2要素でステータスコードを指定する |

`2. クエリパラメータでの絞り込み`が「一覧の絞り込み」だったのに対し、こちらは「IDを指定して1件だけ取得する」パターンです。どちらもJSON APIの基本形で、`022_flask_api`ではこれをさらに発展させます。

### 確認方法

```bash
curl http://127.0.0.1:5020/users/1
# => {"user_id":1,"username":"Tom"}

curl -i http://127.0.0.1:5020/users/99
# => 404 Not Found
```

### 実行方法

```bash
python 008_request/example/app3.py
```

### 動作確認：存在するIDと存在しないIDでレスポンスがどう変わるか

| 確認する操作 | 確認したいこと |
|---|---|
| `curl http://127.0.0.1:5020/users/1` | `{"user_id":1,"username":"Tom"}`が返る |
| `curl http://127.0.0.1:5020/users/3` | `{"user_id":3,"username":"John"}`が返る |
| `curl -i http://127.0.0.1:5020/users/99`（存在しないID） | ステータス行が`404 NOT FOUND`になり、ボディは`{"detail":"User not found"}` |
| `curl -i http://127.0.0.1:5020/users/abc`（整数に変換できない値） | `<int:user_id>`のルール自体に一致しないため、この`get_user`には到達せず`404 NOT FOUND`（Flask標準のエラーページ）が返る |

**正常な状態の見分け方**：存在するIDなら`200`でユーザー情報、存在しないIDなら`404`で`{"detail": "User not found"}`が返るのが正しい挙動です。存在しないIDなのに`200`が返る、または存在するIDなのに`404`になる場合は`users.get(user_id)`の判定を疑ってください。

---

## 4. 練習問題

> [challenge/challenge.py](challenge/challenge.py) — 問題 ｜ [challenge/answer/challenge.py](challenge/answer/challenge.py) — 解答

### 問題：メモ一覧をカテゴリで絞り込めるようにしよう

`007_with`で作ったメモ一覧・詳細ページ・リダイレクト（`challenge/challenge.py`にすでに実装済み。メモデータは`memos.json`から読み込み）に、カテゴリで絞り込むクエリパラメータを追加します。`top.html`はすでに`{% for %}`でメモ一覧をループ表示するようになっているので、Python側で渡す`memos`の中身を絞り込むだけです。

```bash
python 008_request/challenge/challenge.py
```

#### 仕様

| エンドポイント | メソッド | 処理 |
|---|---|---|
| `/` | GET | クエリパラメータ`category`が指定されていれば、そのカテゴリのメモだけに絞り込んで表示する |
| `/?category=仕事` | GET | カテゴリが「仕事」のメモ（1件）のみ表示する |
| `/`（`category`指定なし） | GET | 全件表示する |

#### ヒント

- `request.args.get('category')`でクエリパラメータを取得する（無ければ`None`）
- `category`が`None`でなければ、リスト内包表記で`memos`を絞り込む（`2. クエリパラメータでの絞り込み`と同じ考え方）
- テンプレート側の`{% for %}`はすでに実装済みなので変更不要

### 動作確認：カテゴリ絞り込みが一覧ページに反映されるか

```bash
python 008_request/challenge/challenge.py
```

| 確認する操作 | 確認したいこと |
|---|---|
| `http://127.0.0.1:5021/`にアクセスする | `category`を指定していないので、`memos.json`の全件が表示される |
| `http://127.0.0.1:5021/?category=仕事`にアクセスする | カテゴリが「仕事」のメモだけに絞り込まれて表示される |
| 存在しないカテゴリ（例: `?category=旅行`）を指定する | 該当するメモが無いため、一覧が空（0件）になる |
| 絞り込んだ状態からメモの詳細ページに遷移し、一覧に戻る | 一覧ページに戻ると絞り込みが解除され、再び全件表示になる（`category`はURLのクエリパラメータとして保持されないため） |

**正常な状態の見分け方**：URLの`?category=...`の値と、実際に表示されているメモのカテゴリが一致していれば正常です。指定したカテゴリ以外のメモが混ざって表示される場合は、絞り込みのリスト内包表記の条件を疑ってください。
