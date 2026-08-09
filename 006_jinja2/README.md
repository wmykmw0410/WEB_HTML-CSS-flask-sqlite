# 006 Jinja2

Flaskの標準テンプレートエンジン**Jinja2**の文法・テンプレート継承・フィルターを学びます。`render_template`の基本は`004_flask_basic`、`redirect()`と組み合わせた`url_for()`（クエリパラメータへのフォールバック・テンプレート内での利用を含む）は`005_redirect`で学んだ前提で進みます。

## 目次

1. [Jinja2 文法基礎](#1-jinja2-文法基礎) — 変数展開・for・if
2. [テンプレート継承](#2-テンプレート継承) — `extends` / `block` / `super()`
3. [練習問題](#3-練習問題) — 書籍一覧アプリ（1〜2の総合）

> **Appendix** — [フィルター（組み込み・カスタム）](appendix/filter/) — 学習の優先度は低いため補足として分離

---

## フォルダ構成

```
006_jinja2/
├── README.md
├── example/
│   ├── app2/        Jinja2 文法基礎（変数・for・if）
│   └── app3/        テンプレート継承（extends / block / super）
├── appendix/
│   └── filter/      Jinja2 フィルター（組み込み・カスタム）
└── challenge/         # 005_redirectの続き（000_my_appに組み込む機能の追加分）
    ├── challenge.py    # 完成済み（このチャプターの主役はテンプレート側）
    ├── static/
    ├── templates/     # TODO：extends・block・forを使って完成させる
    │   ├── base.html
    │   ├── top.html
    │   └── detail.html
    └── answer/
        ├── challenge.py
        ├── static/
        └── templates/
            ├── base.html
            ├── top.html
            └── detail.html
```

---

## 1. Jinja2 文法基礎

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

## 2. テンプレート継承

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

## 3. 練習問題

> [challenge/templates/](challenge/templates/) — 問題 ｜ [challenge/answer/templates/](challenge/answer/templates/) — 解答

### 問題：書籍一覧・詳細ページをテンプレート継承 + forループで書き直そう

`005_redirect`で作った書籍一覧・詳細ページ・リダイレクト（`challenge/challenge.py`にすでに実装済み）は、そのままです。この章の主役は**テンプレート側**なので、Python側の変更はありません。

`challenge/templates/`の3ファイル（`base.html`・`top.html`・`detail.html`）は、それぞれTODOコメントだけが書かれた状態です。TODOコメントの指示に従って、`005_redirect/challenge/answer/templates/`にあった「ハードコードされた5枚のカード」「header/nav/footerの重複」を、テンプレート継承と`{% for %}`ループを使った書き方に置き換えてください。

```bash
python 006_jinja2/challenge/challenge.py
```

#### 仕様

| ファイル | やること |
|---|---|
| `base.html` | `header`・`nav`・`footer`など共通レイアウトを持ち、`title`ブロックと`content`ブロックを用意する |
| `top.html` | `base.html`を継承し、`content`ブロックの中で`books`を`{% for %}`でループしてカード一覧を表示する |
| `detail.html` | `base.html`を継承し、`title`ブロックを上書きしつつ、`content`ブロックの中に書籍詳細を表示する |

#### ヒント

- `{% extends "base.html" %}`は必ずファイルの先頭に書く（セクション2）
- `book_list()`から渡される`books`は`[{"id": 1, "title": ..., "author": ..., "price": ..., "image": ...}, ...]`という辞書のリスト。`{% for book in books %}`でループし、`book.id`・`book.title`のように参照する（セクション1）
- カードのリンク先は`href="/books/{{ book.id }}"`、画像は`src="/static/img/{{ book.image }}"`
- 完成したら、ブラウザで`http://127.0.0.1:5014/`と`http://127.0.0.1:5014/books/1`を開き、`005_redirect`の頃と見た目が変わっていないことを確認する（中身の書き方だけが変わっている）

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
