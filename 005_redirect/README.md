# 005 リダイレクト

`redirect()`でブラウザを別のURLへ転送する方法を学びます。`url_for()`と組み合わせることで、URLを`"/new"`のように直接書かずに、関数名から動的に生成できます。

各章は「機能の学習」と「`000_my_app`を完成させるための機能追加」の2部構成です。前者は`example/`で単体のサンプルとして学び、後者は`challenge/`でメモ帳アプリを組み立てながら取り組みます。

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

### 動作確認：アドレスバーとステータスコードで転送を確認する

| 確認する操作 | 確認したいこと |
|---|---|
| `http://127.0.0.1:5008/old`にアクセスする | 画面には`New Page`と表示され、**アドレスバーが`/new`に変わっている**（`/old`のまま表示だけ変わるのではなく、URL自体が転送されている） |
| 開発者ツールのネットワークタブで`/old`へのリクエストを見る | ステータスコードが`302 FOUND`になっており、レスポンスヘッダーの`Location`に`/new`が入っている |
| `http://127.0.0.1:5008/new`に直接アクセスする | `/old`を経由しなくても同じ`New Page`が表示される（`/new`は独立したルートとして存在する） |

**正常な状態の見分け方**：`/old`にアクセスした後、アドレスバーが自動的に`/new`へ書き換わっていれば`redirect()`が正しく機能しています。アドレスバーが`/old`のままなら、`return redirect(...)`ではなく通常の文字列を返してしまっている可能性があります。

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

### 動作確認：内部リダイレクトとの違い

| 確認する操作 | 確認したいこと |
|---|---|
| `http://127.0.0.1:5008/go-flask`にアクセスする | Flaskの公式サイト（`https://flask.palletsprojects.com/`）に転送される。アドレスバーが**自分のアプリのURL（`127.0.0.1:5008`）ではなくなる**点が「1. 内部URLへのリダイレクト」との違い |
| Flaskアプリ側のログ（ターミナル）を見る | `/go-flask`へのアクセスがログに残るが、転送先の外部サイトの中身はこのアプリでは一切関知していないことがわかる |

**正常な状態の見分け方**：内部リダイレクト（セクション1）はアドレスバーが自分のアプリ内のURLのまま変わるのに対し、外部リダイレクトはアドレスバーのホスト名ごと別サイトに変わります。この違いが確認できていればOKです。

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

### 動作確認：渡した引数の値がURLに反映されるか

| 確認する操作 | 確認したいこと |
|---|---|
| `http://127.0.0.1:5008/go-item/42`にアクセスする | `/items/42`に転送され、`Item 42`と表示される |
| URLの`42`を`7`に変えて`http://127.0.0.1:5008/go-item/7`にアクセスする | 転送先も`/items/7`に変わり、`Item 7`と表示される（渡した`item_id`の値がそのままリダイレクト先のURLに反映される） |
| `go_item`の`url_for('item_detail', item_id=item_id)`を、引数名を`id=item_id`のように**わざと間違えて**書き換えて実行する（確認後は元に戻す） | `BuildError`（`werkzeug.routing.exceptions.BuildError`）が発生する。パラメータ名の一致が必須であることが確認できる |

**正常な状態の見分け方**：`/go-item/<数値>`にアクセスするたびに、その数値がそのまま`/items/<数値>`に引き継がれていれば正常です。`BuildError`が出る場合はルート側の`<int:item_id>`と`url_for()`のキーワード引数名が一致しているか確認してください。

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

### 動作確認：url_for()が生成するURLの違いを見る

このスクリプトはサーバーを起動せず、`test_request_context()`の中で`print(url_for(...))`をそのまま実行して終了します。

| 確認する行 | 確認したいこと |
|---|---|
| `print(url_for('show_index'))` | `/`と出力される（引数無しならパスだけ） |
| `print(url_for('show_hello'))` | `/hello/`と出力される（`name`は`None`がデフォルトなのでパスパラメータ無しの方のルートが使われる） |
| `print(url_for('show_hello', name='Tom'))` | `/hello/Tom`と出力される（`name`がパスパラメータに埋め込まれる） |
| `print(url_for('show_index', page=2))` | `/?page=2`と出力される（`show_index`のルートに`page`というパスパラメータは無いため、自動的にクエリパラメータになる） |
| `print(url_for('show_hello', name='Tom', lang='ja'))` | `/hello/Tom?lang=ja`と出力される（`name`はパスに、`lang`はクエリパラメータになる） |

**正常な状態の見分け方**：ルートに定義されているキーワードはURLの「パスの一部」に、定義されていないキーワードは「`?key=value`のクエリパラメータ」になっていれば正常です。想定と違う形式で出力される場合は、対象のルートに`<変数名>`が定義されているかを確認してください。

---

## 5. 練習問題

> [challenge/challenge.py](challenge/challenge.py) — 問題 ｜ [challenge/answer/challenge.py](challenge/answer/challenge.py) — 解答

### 問題：旧URLからのリダイレクトを追加しよう

`004_flask_basic`で作ったメモ一覧・詳細ページ（`challenge/challenge.py`にすでに実装済み）に、旧URLからのリダイレクトを追加します。

```bash
python 005_redirect/challenge/challenge.py
```

#### 仕様

| エンドポイント | メソッド | 処理 |
|---|---|---|
| `/old-memos` | GET | メモ一覧ページ（`/`）へリダイレクトする |

#### ヒント

- `redirect()`と`url_for()`を使う。`url_for('関数名')`の関数名には、`/`に対応するビュー関数名（`memo_list`）を指定する

### 動作確認：旧URLからのリダイレクトが機能しているか

```bash
python 005_redirect/challenge/challenge.py
```

| 確認する操作 | 確認したいこと |
|---|---|
| `http://127.0.0.1:5009/old-memos`にアクセスする | **アドレスバーが`/`に変わり**、メモ一覧ページが表示される（`302 Found`での内部リダイレクト） |
| ブラウザの開発者ツールの「Network」タブで`/old-memos`へのリクエストを確認する | ステータスコードが**302**で、レスポンスヘッダーの`Location`が`/`になっている |
| `/`（メモ一覧）に直接アクセスする | こちらはリダイレクトされず、そのまま**200**でメモ一覧が表示される（`/old-memos`だけが転送対象） |

**正常な状態の見分け方**：`/old-memos`にアクセスしたときだけURLが自動的に`/`へ変わることが正しい状態です。URLが`/old-memos`のまま変わらない場合は`redirect()`の呼び出し忘れ、`/`以外の場所に飛ぶ場合は`url_for()`に渡す関数名の指定ミスを疑ってください。
