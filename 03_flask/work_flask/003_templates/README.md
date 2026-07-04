# 003 テンプレート

`render_template` と `url_for` の基本から始まり、Jinja2 の文法・テンプレート継承・応用フィルターまでを順番に学べます。

## 目次

1. [render_template / url_for](#1-render_template--url_for) — テンプレートの描画と URL 生成
2. [Jinja2 文法基礎](#2-jinja2-文法基礎) — 変数展開・for・if
3. [テンプレート継承](#3-テンプレート継承) — `extends` / `block` / `super()`
4. [練習問題](#練習問題) — 書籍一覧アプリ（1〜3の総合）

> **Appendix** — [フィルター（組み込み・カスタム）](appendix/filter/) — 学習の優先度は低いため補足として分離

---

## フォルダ構成

```
003_templates/
├── README.md
├── example/
│   ├── app1/   render_template + url_for
│   ├── app2/   Jinja2 文法基礎（変数・for・if）
│   └── app3/   テンプレート継承（extends / block / super）
└── appendix/
    └── filter/ Jinja2 フィルター（組み込み・カスタム）
```

---

## 1. render_template / url_for

> [example/app1/](example/app1/)

### 1-1. render_template

`render_template('ファイル名')` で `templates/` フォルダ内のHTMLを描画してレスポンスとして返します。

```python
from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('top.html')

@app.route("/list")
def item_list():
    return render_template('list.html')
```

```
app1/
├── app.py
├── url_for.py
└── templates/
    ├── top.html
    ├── list.html
    └── detail.html
```

**値を渡す場合** はキーワード引数で渡し、テンプレート内で `{{ キー名 }}` として参照します。

```python
@app.route("/detail/<int:id>")
def item_detail(id):
    return render_template('detail.html', show_id=id)
```

```html
<th>{{ show_id }}</th>
```

### 1-2. url_for

> [example/app1/url_for.py](example/app1/url_for.py)

`url_for('ビュー関数名')` でURL文字列をハードコードせず動的に生成します。ルートのパスを変更してもリンク側の修正が不要になります。

**Python 側での使い方**

```python
with app.test_request_context():
    print(url_for('show_index'))              # /
    print(url_for('show_hello'))              # /hello/
    print(url_for('show_hello', name='Tom'))  # /hello/Tom

    # パスパラメータに存在しないキーはクエリパラメータになる
    print(url_for('show_index', page=2))                # /?page=2
    print(url_for('show_hello', name='Tom', lang='ja')) # /hello/Tom?lang=ja
```

**テンプレート側での使い方**

```html
<!-- url_for で関数名から URL を逆引き -->
<a href="{{ url_for('item_list') }}">商品一覧へ</a>

<!-- パスパラメータ付き -->
<a href="{{ url_for('item_detail', id=1) }}">詳細へ</a>

<!-- クエリパラメータ付き（パスに存在しないキーは ?key=value になる） -->
<a href="{{ url_for('item_list', page=2) }}">次のページ</a>
```

### ポイント

| 書き方 | 生成される URL | 説明 |
|---|---|---|
| `url_for('関数名')` | `/path` | パスのみ |
| `url_for('関数名', id=1)` | `/path/1` | パスパラメータに対応するキーはパスに埋め込まれる |
| `url_for('関数名', page=2)` | `/path?page=2` | パスにないキーはクエリパラメータになる |
| `url_for('関数名', id=1, lang='ja')` | `/path/1?lang=ja` | 両方の組み合わせも可能 |

---

## 2. Jinja2 文法基礎

> [example/app2/](example/app2/)

Jinja2 はHTMLの中に Python の値や制御構造を埋め込むテンプレートエンジンです。

### 用語：デリミタ

| 記法 | 用途 |
|---|---|
| `{{ }}` | 変数や式を展開して出力する |
| `{% %}` | 制御文（for・if など）を書く |
| `{# #}` | コメント（HTML に出力されない） |

### 2-1. 変数展開

> [example/app2/templates/vars.html](example/app2/templates/vars.html)

`render_template()` で渡した値を `{{ 変数名 }}` で表示します。

**辞書型** — `.` でも `[]` でもアクセスできます。

```html
<p>{{ key.temp }} / {{ key['jinja'] }}</p>
```

**リスト型** — インデックスも `.` か `[]` で指定します。

```html
<li>{{ words.0 }}</li>
<li>{{ words[1] }}</li>
```

**クラス型** — 属性名で直接アクセスします。

```html
<p>{{ user.name }} / {{ user.age }}</p>
```

### 2-2. for ループ

> [example/app2/templates/for.html](example/app2/templates/for.html)

```html
{% for item in items %}
<tr>
    <td>{{ item.id }}</td>
    <td>{{ item.name }}</td>
</tr>
{% endfor %}
```

### 2-3. if / elif / else

> [example/app2/templates/if.html](example/app2/templates/if.html)

```html
{% if color == 'red' %}
    <p style="color:red;">Red</p>
{% elif color == 'blue' %}
    <p style="color:blue;">Blue</p>
{% else %}
    <p>その他の色</p>
{% endif %}
```

### 2-4. for + if の組み合わせ

> [example/app2/templates/for_if.html](example/app2/templates/for_if.html)

```html
{% for item in items %}
    {% if show_id == item.id %}
    <tr><td>{{ item.id }}</td><td>{{ item.name }}</td></tr>
    {% endif %}
{% endfor %}
```

---

## 3. テンプレート継承

> [example/app3/](example/app3/)

共通レイアウトを `base.html` に書き、各ページが `{% extends %}` で継承します。ページごとに異なる部分だけ `{% block %}` で上書きします。

```
base.html（共通レイアウト）
├── top.html     {% extends "base.html" %}
├── list.html    {% extends "base.html" %}
└── detail.html  {% extends "base.html" %}
```

### 3-1. base.html — ブロックを定義する

> [example/app3/templates/base.html](example/app3/templates/base.html)

```html
<!DOCTYPE html>
<html lang="ja">
<head>
    <title>{% block title %}タイトル{% endblock %}</title>
</head>
<body>
    {% block header %}ヘッダー{% endblock %}
    {% block content %}内容{% endblock %}
    <hr>
    {% block footer %}<a href="{{ url_for('index') }}">TOP画面へ</a>{% endblock %}
</body>
</html>
```

### 3-2. 子テンプレート — ブロックを上書きする

> [example/app3/templates/top.html](example/app3/templates/top.html)

```html
{% extends "base.html" %}

{% block title %}TOP{% endblock %}

{% block header %}<h1>トップ：画面</h1>{% endblock %}

{% block content %}<a href="{{ url_for('item_list') }}">商品一覧画面へ</a>{% endblock %}

{% block footer %}{% endblock %}
```

| 要素 | 説明 |
|---|---|
| `{% extends "base.html" %}` | 継承元を指定。必ずファイルの先頭に書く |
| `{% block name %}...{% endblock %}` | 親のブロックを上書きする |
| `{% block name %}{% endblock %}` | 空にすることで親のデフォルト出力を消す |

### 3-3. super() — 親の内容を残しつつ追記する

> [example/app3/templates/detail.html](example/app3/templates/detail.html)

```html
{% block footer %}
    {{ super() }}
    <a href="{{ url_for('item_list') }}">一覧画面へ</a>
{% endblock %}
```

`{{ super() }}` で親ブロックのデフォルト内容を維持しながら追加コンテンツを加えられます。

---

## 練習問題

### 問題：書籍一覧アプリを再現しよう

1. 以下のコマンドで [answer/app.py](answer/app.py) を実行してアプリの動作を確認する

```bash
python answer/app.py
```
2. `answer/` を見ずに、同じ機能のアプリを自分で作成する

#### 確認ポイント

`answer/app.py` を実行したとき、以下の動作になることを確認してください。

| URL | 表示内容 |
|---|---|
| `/` | トップページ（書籍一覧へのリンクあり） |
| `/books` | 書籍一覧テーブル（在庫状況つき） |

#### ヒント

- `url_for` でナビゲーションリンクを生成する（セクション 1）
- `{% for %}` / `{% if %}` でリストと在庫状況を表示する（セクション 2）
- `base.html` を継承して共通レイアウトを実装する（セクション 3）

---

## Appendix. フィルター

> [appendix/filter/](appendix/filter/)

フィルターは初学段階では必須ではありません。フォームや DB 連携を学んだ後、表示の整形が必要になった段階で参照してください。実務でよく使う `| safe` は WTForms とのセットで登場します。

### 組み込みフィルター

```html
{{ users | first }}      {# 先頭要素 #}
{{ users | last }}       {# 末尾要素 #}
{{ users | length }}     {# 要素数 #}
{{ users | join('=>') }} {# 結合 #}
{{ field(...) | safe }}  {# HTML をエスケープせずそのまま出力（WTForms で使用） #}
```

### カスタムフィルター

`@app.template_filter('フィルター名')` でオリジナルのフィルターを定義します。日付フォーマットや金額のカンマ区切りなど、表示ロジックをテンプレートから分離する用途で使われます。

```python
@app.template_filter('truncate')
def str_truncate(value, length=10):
    if len(value) > length:
        return value[:length] + '...'
    return value
```
