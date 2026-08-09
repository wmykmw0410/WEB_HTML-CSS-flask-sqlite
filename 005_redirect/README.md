# 005 リダイレクト

`redirect()`でブラウザを別のURLへ転送する方法を学びます。`url_for()`と組み合わせることで、URLを`"/new"`のように直接書かずに、関数名から動的に生成できます。

各章は「機能の学習」と「`000_my_app`を完成させるための機能追加」の2部構成です。前者は`example/`で単体のサンプルとして学び、後者は`challenge/`で`100_bookstore_api`を完成形の参考にしながら取り組みます。

## 目次

1. [内部URLへのリダイレクト](#1-内部urlへのリダイレクト)
2. [外部URLへのリダイレクト](#2-外部urlへのリダイレクト)
3. [url_for()に引数を渡す](#3-url_forに引数を渡す)
4. [url_for()の応用](#4-url_forの応用) — クエリパラメータへのフォールバック・テンプレート内での利用
5. [練習問題](#5-練習問題)

---

## フォルダ構成

```
005_redirect/
├── README.md
├── example/
│   ├── app1.py            # redirect・url_for（内部/外部/引数付き）
│   └── app2.py            # url_forの応用（クエリパラメータ・test_request_context）
└── challenge/               # 004_flask_basicの続き（000_my_appに組み込むルーティングの追加分）
    ├── challenge.py
    ├── static/
    ├── templates/
    └── answer/
        ├── challenge.py
        ├── static/
        └── templates/
```

---

## 1. 内部URLへのリダイレクト

> [example/app1.py](example/app1.py)

```python
from flask import Flask, redirect, url_for

app = Flask(__name__)

@app.route('/old')
def old_page():
    return redirect(url_for('new_page'))

@app.route('/new')
def new_page():
    return '<h1>New Page</h1>'
```

### ポイント

| 関数 | 説明 |
|---|---|
| `redirect(url)` | 指定したURLへリダイレクト（デフォルト: ステータスコード302） |
| `url_for('関数名')` | ビュー関数名からURLを逆引き生成する |

`redirect('/new')`のようにURLを直接書くこともできますが、`url_for('new_page')`を使うと、`@app.route()`のパスを後から変更してもリンク側の修正が不要になります（この利点は`006_jinja2`のテンプレート内リンクでも同じです）。

### 実行方法

```bash
python 005_redirect/example/app1.py
```

ブラウザで`http://127.0.0.1:5008/old`にアクセスし、`/new`に転送されることを確認してください。

---

## 2. 外部URLへのリダイレクト

> [example/app1.py](example/app1.py)

```python
@app.route('/go-flask')
def go_flask():
    return redirect('https://flask.palletsprojects.com/')
```

`url_for()`はアプリ内のビュー関数にしか使えません。外部サイトへリダイレクトする場合は、URLを直接文字列で渡します。

### 実行方法

`http://127.0.0.1:5008/go-flask`にアクセスすると、Flaskの公式サイトへ転送されます。

---

## 3. url_for()に引数を渡す

> [example/app1.py](example/app1.py)

`004_flask_basic`の動的ルーティングで学んだパスパラメータは、`url_for()`にも同じ名前の引数として渡せます。

```python
@app.route('/items/<int:item_id>')
def item_detail(item_id):
    return f'<h1>Item {item_id}</h1>'

@app.route('/go-item/<int:item_id>')
def go_item(item_id):
    return redirect(url_for('item_detail', item_id=item_id))
```

`url_for('item_detail', item_id=42)`は`/items/42`というURLを生成します。ルートのパスに含まれるパラメータ名（`<int:item_id>`）と、`url_for()`に渡すキーワード引数名（`item_id=`）が一致している必要があります。

### 実行方法

`http://127.0.0.1:5008/go-item/42`にアクセスすると、`/items/42`に転送されることを確認してください。

---

## 4. url_for()の応用

> [example/app2.py](example/app2.py)

`3. url_for()に引数を渡す`では、ルートのパスパラメータに対応する引数を渡しました。ここでは`url_for()`をもう少し詳しく見ていきます。

### ルートに無いキーはクエリパラメータになる

```python
print(url_for('show_index'))              # /
print(url_for('show_hello'))              # /hello/
print(url_for('show_hello', name='Tom'))  # /hello/Tom

# パスパラメータに存在しないキーはクエリパラメータになる
print(url_for('show_index', page=2))                 # /?page=2
print(url_for('show_hello', name='Tom', lang='ja'))   # /hello/Tom?lang=ja
```

`show_hello`のルート（`/hello/<name>`）は`name`という1つのパスパラメータしか持ちません。`lang`のようにルートに無いキーワード引数を渡すと、自動的に`?lang=ja`のようなクエリパラメータとして付加されます。

### リクエストの外でurl_forを使う：test_request_context()

`url_for()`は通常リクエスト処理中（ビュー関数の中）で使いますが、`app.test_request_context()`を使うと、サーバーを起動せずスクリプト単体でも動作確認できます。

```python
with app.test_request_context():
    print(url_for('show_index'))  # /
```

### テンプレートの中でのurl_for

`url_for()`はPythonコードだけでなく、テンプレート（`{{ }}`の中）でも使えます。

```html
<a href="{{ url_for('item_list') }}">商品一覧へ</a>
<a href="{{ url_for('item_detail', id=1) }}">詳細へ</a>
```

URLをテンプレートにハードコードしないことで、ルートのパスを変更してもリンク側の修正が不要になります。この書き方は`006_jinja2`のテンプレートでも随所に登場します。

### ポイント

| 書き方 | 生成されるURL | 説明 |
|---|---|---|
| `url_for('関数名')` | `/path` | パスのみ |
| `url_for('関数名', id=1)` | `/path/1` | パスパラメータに対応するキーはパスに埋め込まれる |
| `url_for('関数名', page=2)` | `/path?page=2` | パスに無いキーはクエリパラメータになる |
| `url_for('関数名', id=1, lang='ja')` | `/path/1?lang=ja` | 両方の組み合わせも可能 |

### 実行方法

```bash
python 005_redirect/example/app2.py
```

---

## 5. 練習問題

> [challenge/challenge.py](challenge/challenge.py) — 問題 ｜ [challenge/answer/challenge.py](challenge/answer/challenge.py) — 解答

### 問題：旧URLからのリダイレクトを追加しよう

`004_flask_basic`で作った書籍一覧・詳細ページ（`challenge/challenge.py`にすでに実装済み）に、旧URLからのリダイレクトを追加します。

```bash
python 005_redirect/challenge/challenge.py
```

#### 仕様

| エンドポイント | メソッド | 処理 |
|---|---|---|
| `/old-books` | GET | 書籍一覧ページ（`/`）へリダイレクトする |

#### ヒント

- `redirect()`と`url_for()`を使う。`url_for('関数名')`の関数名には、`/`に対応するビュー関数名（`book_list`）を指定する
- 動作確認は`http://127.0.0.1:5009/old-books`にアクセスし、`/`へ転送されることを確認する
