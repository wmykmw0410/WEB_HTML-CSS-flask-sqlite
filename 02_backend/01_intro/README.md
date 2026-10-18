# 01 イントロダクション：FlaskとSQLiteを1時間で体験する

> バックエンド編 ／ 前の章：[01_frontend/11_homepage](../../01_frontend/11_homepage/) ／ 次の章：[02_memo_app_frontend](../02_memo_app_frontend/)

バックエンド編の入り口です。このREADMEを上から読みながら、**サーバーを動かしたまま**コードを貼り付けていき、そのたびにブラウザで動きを確かめます。最後には、サーバー（Flask）とデータベース（SQLite）で動く小さなメモ帳ができあがります。

フロントエンド編で作ったページは、HTMLファイルをブラウザで開けば動きました。ここで作るのは、**サーバーのプログラムがHTMLを作って返し、メモをデータベースに保存する**アプリです。ブラウザを閉じても、別のブラウザから開いても、同じメモが表示されます。

1行ずつ理解できなくても大丈夫です。「こう書くと、こう動く」を体験して、バックエンド編の全体像をつかむことが目的です。それぞれのコードを詳しく学ぶ章は、最後の表にまとめています。

## 目次

- [Webのしくみ（最低限）](#webのしくみ最低限)（5分。コードは書かない）
0. [環境構築](#0-環境構築)（初回のみ・15分。手順は[00_docs/setup/backend.md](../../00_docs/setup/backend.md)）
1. [準備して起動する](#1-準備して起動する)（5分）
2. [データベースを用意する](#2-データベースを用意する)（10分）
3. [一覧を表示する](#3-一覧を表示する)（15分）
4. [追加する](#4-追加する)（10分）
5. [削除する](#5-削除する)（5分）
6. [ふりかえり](#6-ふりかえり)（10分）

うまく動かないときは、完成版の[answer/](answer/)と見比べてください。

---

## Webのしくみ（最低限）

コードを書く前に、この章で出てくる言葉だけを押さえておきます。詳しくは補足資料の[00_docs/web_basic](../../00_docs/web_basic/)にまとめています。

### リクエストとレスポンス

Webページは、**ブラウザ**（クライアント）が**サーバー**に「このページをください」という**リクエスト**を送り、サーバーが**レスポンス**（HTMLなど）を返すことで表示されます。

```
ブラウザ  ── リクエスト（GET /hello）──▶  サーバー（この章で作る Flask のプログラム）
         ◀── レスポンス（200 と HTML）──
```

フロントエンド編で作ったのは、ブラウザの中で動く部分（**フロントエンド**）です。この章からは、サーバーの中で動いてレスポンスを作る部分（**バックエンド**）を作ります。誰が見ても同じファイルを返すだけなら**静的サイト**ですが、メモ帳のように保存された内容によって毎回HTMLを作って返すものは**動的サイト**と呼ばれます。

### URLの読み方

```
http://127.0.0.1:5100/memos/3/delete
└┬─┘   └───┬───┘ └┬─┘└──────┬─────┘
スキーム  ホスト   ポート     パス
```

| 部分 | 意味 |
|---|---|
| `127.0.0.1`（`localhost`） | 「自分のパソコン自身」を指す特別な住所。自分のパソコンで動かしているサーバーにつなぐときに使う |
| `5100` | ポート番号。1台のパソコンで複数のサーバーを動かすときの「窓口の番号」。章ごとに違う番号を使う |
| `/memos/3/delete` | パス。サーバーの中の「どのページか」。Flaskでは`@app.route('/パス')`で、パスごとに呼ぶ関数を決める |

### メソッド：GETとPOST

リクエストには「何をしたいか」を表す**メソッド**が付いています。

| メソッド | 使う場面 | この章での例 |
|---|---|---|
| GET | ページを**見る**（URLを開く・リンクを押す） | 一覧のページ`/`を開く |
| POST | データを**送る**（フォームの送信） | 「追加」「削除」ボタン |

### ステータスコード

レスポンスには、結果を表す3桁の**ステータスコード**が付いています。

| コード | 意味 | この章で見る場面 |
|---|---|---|
| 200 | 成功 | ページが表示されたとき |
| 302 | リダイレクト（別のURLへ移動してほしい） | メモを追加・削除したあと、一覧へ戻すとき |
| 404 | 見つからない | まだ作っていないパスを開いたとき |
| 500 | サーバー内部のエラー | プログラムにエラーがあるとき（ターミナルにエラーの内容が出る） |

サーバーを動かしているターミナルには、届いたリクエストが1行ずつ表示されます。たとえば`"GET /hello HTTP/1.1" 200`は、「`/hello`をGETで要求され、200（成功）を返した」という意味です。この章では、ブラウザの画面と一緒に、この行も見ながら進めます。

---

## 0. 環境構築

まだ環境構築をしていない場合は、先に[00_docs/setup/backend.md](../../00_docs/setup/backend.md)の手順で、Python・仮想環境（`flaskenv`）・ライブラリ・VS Codeの拡張機能を用意してください（初回のみ・15分）。バックエンド編のすべての章で使います。

---

## 1. 準備して起動する

ターミナルで、仮想環境が有効（行の先頭に`(flaskenv)`）になっていることを確かめます。

作業は`work/`フォルダで行います。ターミナルで移動しておきます。

```bash
cd 02_backend/01_intro/work
```

`work/app.py`を作り、次のコードを貼り付けて保存します。

```python
# ---------- 1. 準備 ----------
from flask import Flask

app = Flask(__name__)


@app.route('/hello')
def hello():
    return 'Flaskが動いています！'


# ========== ここより上に、2. 〜 5. のコードを貼り付けていく ==========

if __name__ == '__main__':
    app.run(debug=True, port=5100)   # debug=True：保存すると自動で再起動する
```

ターミナルで起動します。

```bash
python app.py
```

`Running on http://127.0.0.1:5100`と表示されたら、ブラウザで <http://127.0.0.1:5100/hello> を開きます。

| 確認する操作 | 確認したいこと |
|---|---|
| <http://127.0.0.1:5100/hello> を開く | 「Flaskが動いています！」と表示される |
| <http://127.0.0.1:5100/> を開く | 「Not Found」（404）になる（`/`のページはまだ作っていない） |
| ターミナルを見る | `"GET /hello HTTP/1.1" 200`のように、ブラウザから届いたリクエストが1行ずつ表示されている |

`@app.route('/hello')`は、「`/hello`というURLにリクエストが来たら、すぐ下の関数を呼ぶ」という意味です。関数の戻り値が、レスポンスとしてブラウザに返ります（冒頭の「[Webのしくみ（最低限）](#webのしくみ最低限)」の「リクエストとレスポンス」を、自分で書いたプログラムが返しています）。

**ここからの進め方**：サーバーは**起動したまま**にしておきます。この先の2〜5のコードは、`app.py`の`# ========== ここより上に…`の行の**上**に、順に貼り付けていきます。保存すると、サーバーが自動で再起動します（`debug=True`のため。ターミナルに`Restarting`と表示される）。ブラウザを再読み込みすれば、すぐに結果を確かめられます。

貼り付けたコードに間違いがあると、ターミナルにエラーが表示されてサーバーが止まることがあります。そのときは、エラーの行を直して保存し、もう一度`python app.py`で起動します。サーバーを止めるときは`Ctrl + C`です。

---

## 2. データベースを用意する

メモを保存する**データベース**（SQLite）を用意します。次のコードを、`# ========== ここより上に…`の行の上に貼り付けて保存します。

```python
# ---------- 2. データベース ----------
import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), 'memos.db')   # app.py と同じフォルダの memos.db


def get_db():
    """データベースにつなぐ"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row   # row['text'] のように、列の名前で取り出せるようにする
    return conn


def init_db():
    """memos テーブルが無ければ作る"""
    conn = get_db()
    conn.execute('CREATE TABLE IF NOT EXISTS memos (id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT NOT NULL)')
    conn.commit()
    conn.close()


init_db()   # このファイルが読み込まれたときに、テーブルを用意する
```

| 確認する操作 | 確認したいこと |
|---|---|
| 保存してから、`work/`フォルダを見る | `memos.db`というファイルができている（これがデータベース） |

最初の2行は、Python標準の`sqlite3`（データベースを使う道具）と、ファイルの場所を組み立てる`os`を読み込む行です。この章では、どの道具をどこで使うかがわかるように、**使う直前に読み込んで**います（ふつうのプログラムでは、`import`はファイルの先頭にまとめて書きます）。

`init_db()`は、メモを入れる表（**テーブル**）を作ります。テーブル`memos`は、`id`（番号。自動で1, 2, 3…と付く）と`text`（メモの文字）の2つの列だけです。`'CREATE TABLE …'`のような文字列は、**SQL**というデータベースへの命令の言葉で、`conn.execute()`で送って実行します。

---

## 3. 一覧を表示する

`/`を開いたときに、メモの一覧のページを返すようにします。先に、ページのHTMLとCSSを作ります。`templates/`と`static/`のフォルダは自分で作ります（Flaskは、HTMLを`templates/`、CSSを`static/`から探す決まりです）。

```
work/
├── app.py
├── memos.db
├── templates/
│   └── index.html
└── static/
    └── style.css
```

**`work/templates/index.html`**を作り、まるごと貼り付けます。

```html
<!doctype html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>メモ帳</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <h1>メモ帳</h1>

    <!-- 追加フォーム：入力した text を、POST で /memos に送る -->
    <form class="add" method="post" action="/memos">
        <input type="text" name="text" placeholder="メモを入力" required>
        <button type="submit">追加</button>
    </form>

    <!-- 一覧：Python から渡された memos を、1件ずつ表示する -->
    <ul class="memos">
        {% for memo in memos %}
        <li>
            <span>{{ memo['text'] }}</span>
            <!-- 削除ボタン：POST で /memos/番号/delete に送る -->
            <form method="post" action="/memos/{{ memo['id'] }}/delete">
                <button type="submit" class="delete">削除</button>
            </form>
        </li>
        {% else %}
        <li>メモはまだありません</li>
        {% endfor %}
    </ul>
</body>
</html>
```

**`work/static/style.css`**を作り、まるごと貼り付けます。

```css
body {
    max-width: 560px;
    margin: 32px auto;
    padding: 0 16px;
    font-family: sans-serif;
    color: #262b33;
    background: #f4f6f9;
}

.add {
    display: flex;
    gap: 8px;
    margin-bottom: 16px;
}

.add input {
    flex: 1;
}

input,
button {
    padding: 8px;
    font: inherit;
}

button {
    border: none;
    border-radius: 6px;
    background: #3f6fd1;
    color: #ffffff;
    cursor: pointer;
}

.memos {
    padding: 0;
    list-style: none;
}

.memos li {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 8px;
    padding: 10px 14px;
    border-radius: 8px;
    background: #ffffff;
}

.memos form {
    margin: 0;
}

.delete {
    background: #d1495b;
}
```

最後に、`app.py`の`# ========== ここより上に…`の行の上に、次のコードを貼り付けて保存します。

```python
# ---------- 3. 一覧を表示する ----------
from flask import render_template


@app.route('/')
def index():
    conn = get_db()
    memos = conn.execute('SELECT * FROM memos ORDER BY id DESC').fetchall()   # 新しい順
    conn.close()
    return render_template('index.html', memos=memos)
```

| 確認する操作 | 確認したいこと |
|---|---|
| <http://127.0.0.1:5100/> を再読み込みする | 「メモ帳」のページが表示され、「メモはまだありません」と出る |
| メモを入力して「追加」を押す | 「Not Found」（404）になる（送り先の`/memos`を受け取る関数を、まだ作っていない）。ブラウザの戻るボタンで戻る |
| ページのソースを表示する（右クリック→ページのソースを表示） | `{% for %}`などは消えていて、ふつうのHTMLになっている |

データベースからメモを全部取り出し（`SELECT … ORDER BY id DESC`：新しい順）、`render_template()`で`index.html`に渡しています。`index.html`の中の`{{ … }}`や`{% for %}`は、HTMLではなく**Jinja2**というテンプレートの書き方です。サーバーがこの部分をデータで埋め、完成したHTMLにしてからブラウザに返します。

---

## 4. 追加する

フォームから送られたメモを受け取って、データベースに保存します。`# ========== ここより上に…`の行の上に貼り付けて保存します。

```python
# ---------- 4. 追加する ----------
from flask import redirect, request, url_for


@app.route('/memos', methods=['POST'])
def add_memo():
    text = request.form['text'].strip()
    if text:
        conn = get_db()
        conn.execute('INSERT INTO memos (text) VALUES (?)', (text,))
        conn.commit()   # 変更を確定する（これを忘れると保存されない）
        conn.close()
    return redirect(url_for('index'))   # 一覧に戻る
```

| 確認する操作 | 確認したいこと |
|---|---|
| メモを2〜3件追加する | 新しいものが上に表示される |
| ターミナルを見る | `"POST /memos HTTP/1.1" 302`の後に`"GET / HTTP/1.1" 200`が続いている（追加してから、一覧のページに移動させている） |
| 別のブラウザ（またはシークレットウィンドウ）で開く | 同じメモが表示される（メモはブラウザではなく、サーバーのデータベースにある） |
| 「削除」を押す | まだ「Not Found」（404）になる（次の5.で作る） |

`request.form['text']`で、フォームの`name="text"`の入力欄に入っていた文字を受け取ります。`INSERT`で保存し、`commit()`で確定して、`redirect()`で一覧のページに戻します。`url_for('index')`は、関数`index`のURL（`/`）を作ります。

SQLの`?`の部分には、後ろの`(text,)`の値が入ります。入力された文字を直接SQLの文字列につなげず`?`で渡すのは、入力した文字がSQLとして実行されてしまう攻撃（SQLインジェクション）を防ぐためです。

---

## 5. 削除する

`# ========== ここより上に…`の行の上に貼り付けて保存します。

```python
# ---------- 5. 削除する ----------
@app.route('/memos/<int:memo_id>/delete', methods=['POST'])
def delete_memo(memo_id):
    conn = get_db()
    conn.execute('DELETE FROM memos WHERE id = ?', (memo_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))
```

| 確認する操作 | 確認したいこと |
|---|---|
| 「削除」を押す | そのメモが消える |
| サーバーを止めて（`Ctrl + C`）から、ブラウザを再読み込みする | 「接続できません」になる（ページもメモも、サーバーが返していた） |
| もう一度`python app.py`で起動して、再読み込みする | メモが残っている（`memos.db`に保存されている） |

URLの`<int:memo_id>`の部分（`/memos/3/delete`なら`3`）が、関数の`memo_id`に入ります。1つの関数で、どのメモでも削除できます。

これでメモ帳の完成です。完成した`app.py`は[answer/app.py](answer/app.py)です。試しに、3.の`ORDER BY id DESC`を`ORDER BY id`に変えて保存すると、古い順に並びます。

---

## 6. ふりかえり

### 作ったものと、詳しく学ぶ章

| コード | していること | 詳しく学ぶ章 |
|---|---|---|
| `@app.route('/')` | URLと関数を結びつける | [03_function](../03_function/)（`@`の正体）・[04_flask_basic](../04_flask_basic/) |
| `render_template()`・`{% for %}` | Pythonのデータを入れてHTMLを作る | [04_flask_basic](../04_flask_basic/)・[06_jinja2](../06_jinja2/) |
| `os.path.join()` | ファイルの場所を決める | [07_with](../07_with/) |
| `request.form`・`methods=['POST']` | フォームから送られた内容を受け取る | [08_request](../08_request/) |
| `redirect()`・`url_for()` | 別のページに移動させる | [05_redirect](../05_redirect/) |
| `sqlite3`・`CREATE TABLE`・`SELECT`・`INSERT`・`DELETE` | データベースを操作する | [10_sql](../10_sql/)・[11_sqlite](../11_sqlite/) |
| `/memos/<int:memo_id>/delete` | URLの一部を関数で受け取る | [04_flask_basic](../04_flask_basic/) |

### このアプリに足りないもの

1時間で作ったので、実際に使うには足りないものがあります。それを1つずつ足していくのが、バックエンド編です。

| 足りないもの | 困ること | 学ぶ章 |
|---|---|---|
| 入力チェック・CSRF対策 | 長すぎる文字を保存できてしまう。ほかのサイトから勝手にフォームを送られる | [09_forms](../09_forms/) |
| SQLを書かずにデータを扱う仕組み（ORM）・テーブルの変更の管理 | SQLの文字列を毎回書く必要がある。列を増やすときに困る | [12_sqlalchemy](../12_sqlalchemy/)〜[14_flask_migrate](../14_flask_migrate/) |
| ログイン | 誰でもメモを追加・削除できてしまう | [15_login](../15_login/) |
| ファイルの分け方 | 機能が増えると`app.py`が長くなりすぎる | [17_blueprint](../17_blueprint/) |
| タイトル・カテゴリ・編集・絞り込みなど | メモ帳として機能が少ない | [02_memo_app_frontend](../02_memo_app_frontend/)・完成形の[100_memo_api](../100_memo_api/) |

完成形の[100_memo_api](../100_memo_api/)は、このメモ帳に、上の表の内容をすべて足したものです。一度起動して、ゴールのアプリを触っておくと、この先の章の目的がわかりやすくなります。

## 次のステップ

続きは [02_memo_app_frontend](../02_memo_app_frontend/) です。フロントエンド編で学んだJavaScriptで、まずブラウザだけで動くメモ帳を完成させ、「ブラウザだけでは何ができないのか」を確かめます。この章で体験した「サーバーに保存する」ことの意味が、そこではっきりします。
