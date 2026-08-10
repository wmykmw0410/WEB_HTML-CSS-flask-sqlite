# 006 Jinja2

Flaskの標準テンプレートエンジン**Jinja2**の文法・テンプレート継承・フィルターを学びます。`render_template`の基本は`004_flask_basic`、`redirect()`と組み合わせた`url_for()`（クエリパラメータへのフォールバック・テンプレート内での利用を含む）は`005_redirect`で学んだ前提で進みます。

## 目次

1. [Jinja2 文法基礎](#1-jinja2-文法基礎) — 変数展開・for・if
2. [テンプレート継承](#2-テンプレート継承) — `extends` / `block` / `super()`
3. [練習問題](#3-練習問題) — メモ一覧アプリ（1〜2の総合）

> **Appendix** — [フィルター（組み込み・カスタム）](appendix/filter/) — 学習の優先度は低いため補足として分離

---

## フォルダ構成

```
006_jinja2/
├── README.md
├── example/
│   ├── app1/        Jinja2 文法基礎（変数・for・if）
│   └── app2/        テンプレート継承（extends / block / super）
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

> [example/app1/](example/app1/)

Jinja2 はHTMLの中に Python の値や制御構造を埋め込むテンプレートエンジンです。

### 用語：デリミタ

| 記法 | 用途 |
|---|---|
| `{{ }}` | 変数や式を展開して出力する |
| `{% %}` | 制御文（for・if など）を書く |
| `{# #}` | コメント（HTML に出力されない） |

### 2-1. 変数展開

> [example/app1/templates/vars.html](example/app1/templates/vars.html)

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

> [example/app1/templates/for.html](example/app1/templates/for.html)

```html
{% for item in items %}
<tr>
    <td>{{ item.id }}</td>
    <td>{{ item.name }}</td>
</tr>
{% endfor %}
```

### 2-3. if / elif / else

> [example/app1/templates/if.html](example/app1/templates/if.html)

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

> [example/app1/templates/for_if.html](example/app1/templates/for_if.html)

```html
{% for item in items %}
    {% if show_id == item.id %}
    <tr><td>{{ item.id }}</td><td>{{ item.name }}</td></tr>
    {% endif %}
{% endfor %}
```

### 動作確認：変数展開・for・ifの表示を確認する

```bash
cd 006_jinja2/example/app1
python app.py
```

| 確認する操作 | 確認したいこと |
|---|---|
| `http://127.0.0.1:5011/vars`にアクセスする | 辞書型は`Template Engine / Jinja2`、リスト型は`AAA`・`BBB`・`CCC`の3行、クラス型は`Tom / 20`と表示される（`.`と`[]`のどちらの書き方でも同じ値になることを確認する） |
| `http://127.0.0.1:5011/for`にアクセスする | テーブルに`1 Curry`・`2 Rice`・`3 Pan`の3行が表示される |
| `http://127.0.0.1:5011/if/red`にアクセスする | 赤字で`Red`と表示される |
| `http://127.0.0.1:5011/if/blue`にアクセスする | 青字で`Blue`と表示される |
| `http://127.0.0.1:5011/if/`（色を指定せずにアクセス） | `color`のデフォルト値`'colorless'`はどの`elif`にも一致しないため、`その他の色`と表示される |
| `http://127.0.0.1:5011/for-if/2`にアクセスする | `items`のうち`id`が`2`の行（`ID: 2` / `名前: Rice`）だけが表示される |

**正常な状態の見分け方**：`/if/<color>`はURLの`<color>`部分を変えるたびに表示される文言と色が切り替わり、`/for-if/<id>`はテーブルの行数が常に1行だけになるのが正しい状態です。行数が0行や2行以上になる場合は`if`の比較条件を疑ってください。

---

## 2. テンプレート継承

> [example/app2/](example/app2/)

共通レイアウトを `base.html` に書き、各ページが `{% extends %}` で継承します。ページごとに異なる部分だけ `{% block %}` で上書きします。

```
base.html（共通レイアウト）
├── top.html     {% extends "base.html" %}
├── list.html    {% extends "base.html" %}
└── detail.html  {% extends "base.html" %}
```

### 3-1. base.html — ブロックを定義する

> [example/app2/templates/base.html](example/app2/templates/base.html)

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

> [example/app2/templates/top.html](example/app2/templates/top.html)

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

> [example/app2/templates/detail.html](example/app2/templates/detail.html)

```html
{% block footer %}
    {{ super() }}
    <a href="{{ url_for('item_list') }}">一覧画面へ</a>
{% endblock %}
```

`{{ super() }}` で親ブロックのデフォルト内容を維持しながら追加コンテンツを加えられます。

### 動作確認：継承・上書き・super()の効果を見比べる

```bash
cd 006_jinja2/example/app2
python app.py
```

| 確認する操作 | 確認したいこと |
|---|---|
| `http://127.0.0.1:5012/`にアクセスする | タイトルバーが`TOP`になり、`トップ：画面`という見出しと「商品一覧画面へ」のリンクが表示される。**footerのリンクが無い**（`top.html`が`{% block footer %}{% endblock %}`で空に上書きしているため） |
| ページのソースを表示する（ブラウザで右クリック→ページのソースを表示） | `base.html`の`<!DOCTYPE html>`〜`</html>`の構造はそのまま残り、`{% block %}`の中身だけが子テンプレートの内容に置き換わっている |
| 「商品一覧画面へ」のリンクをクリックし`/list`に遷移する | タイトルが`LIST`になり、団子・肉まん・どら焼きの3行の表が表示される。**footerには`TOP画面へ`のリンクが表示される**（`list.html`は`footer`ブロックを上書きしていないため、`base.html`のデフォルトがそのまま出る） |
| `/list`の商品名のリンク（例:`1`）をクリックして`/detail/1`に遷移する | `商品詳細：画面`という見出しの下に`商品ID : 1`・`商品名 : アイテム-1`が表示され、footerには`TOP画面へ`のリンクに加えて**`一覧画面へ`のリンクも追加表示される**（`{{ super() }}`で親のデフォルト内容を残しつつ追記しているため） |
| `/detail/2`・`/detail/3`のように`id`を変えてアクセスする | 表示される`商品ID`と`商品名`の数字だけが連動して変わる |

**正常な状態の見分け方**：`top.html`だけfooterのリンクが消えていて、`list.html`と`detail.html`ではfooterにリンクが残っている（`detail.html`はさらにリンクが1本多い）のが、`block`の上書きと`super()`が正しく効いている証拠です。

---

## 3. 練習問題

> [challenge/templates/](challenge/templates/) — 問題 ｜ [challenge/answer/templates/](challenge/answer/templates/) — 解答

### 問題：メモ一覧・詳細ページをテンプレート継承 + forループで書き直そう

`005_redirect`で作ったメモ一覧・詳細ページ・リダイレクト（`challenge/challenge.py`にすでに実装済み）は、そのままです。この章の主役は**テンプレート側**なので、Python側の変更はありません。

`challenge/templates/`の3ファイル（`base.html`・`top.html`・`detail.html`）は、それぞれTODOコメントだけが書かれた状態です。TODOコメントの指示に従って、`005_redirect/challenge/answer/templates/`にあった「ハードコードされた5枚のカード」「header/nav/footerの重複」を、テンプレート継承と`{% for %}`ループを使った書き方に置き換えてください。

```bash
python 006_jinja2/challenge/challenge.py
```

#### 仕様

| ファイル | やること |
|---|---|
| `base.html` | `header`・`nav`・`footer`など共通レイアウトを持ち、`title`ブロックと`content`ブロックを用意する |
| `top.html` | `base.html`を継承し、`content`ブロックの中で`memos`を`{% for %}`でループしてカード一覧を表示する |
| `detail.html` | `base.html`を継承し、`title`ブロックを上書きしつつ、`content`ブロックの中にメモ詳細を表示する |

#### ヒント

- `{% extends "base.html" %}`は必ずファイルの先頭に書く（セクション2）
- `memo_list()`から渡される`memos`は`[{"id": 1, "title": ..., "category": ..., "body": ...}, ...]`という辞書のリスト。`{% for memo in memos %}`でループし、`memo.id`・`memo.title`のように参照する（セクション1）
- カードのリンク先は`href="/memos/{{ memo.id }}"`、カテゴリは`<span class="tag">{{ memo.category }}</span>`
- 完成したら、ブラウザで`http://127.0.0.1:5014/`と`http://127.0.0.1:5014/memos/1`を開き、`005_redirect`の頃と見た目が変わっていないことを確認する（中身の書き方だけが変わっている）

### 動作確認：仕上がったテンプレートが以前と同じに見えるか

```bash
python 006_jinja2/challenge/challenge.py
```

| 確認する操作 | 確認したいこと |
|---|---|
| `http://127.0.0.1:5014/`にアクセスする | `005_redirect`のときと同じ5枚のメモカード（買い物リスト・企画会議メモ・読書メモ：銀河鉄道の夜・アプリのアイデア・旅行の持ち物リスト）が表示される。カード数は`memos`辞書の要素数と連動しているので、`{% for %}`が正しく回っていれば5枚、ループが壊れていれば0枚や決め打ちの枚数になる |
| カードのリンク（例:`買い物リスト`）をクリックして詳細ページに遷移する | `http://127.0.0.1:5014/memos/1`に遷移し、タイトル・カテゴリ・本文が表示される |
| 存在しないID、例えば`http://127.0.0.1:5014/memos/99`にアクセスする | 「メモID 99 は見つかりません」と表示される（`memo_detail`側のPythonコードはこの章で変更していないため、`005_redirect`と同じ挙動になる） |
| `base.html`・`top.html`・`detail.html`のいずれかで`{% extends %}`を一時的にコメントアウトする（確認後は必ず戻す） | 共通レイアウトが適用されなくなり、見た目が崩れる。これで継承が実際に効いていることを逆から確認できる |

**正常な状態の見分け方**：見た目が`005_redirect`のときと完全に同じであれば成功です。書き方（テンプレート継承 + forループ）だけが変わり、画面に出る情報は一切変わらないのがこの練習問題のゴールです。

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

### 動作確認：組み込みフィルター・カスタムフィルターの出力を見る

```bash
cd 006_jinja2/appendix/filter
python app.py
```

| 確認する操作 | 確認したいこと |
|---|---|
| `http://127.0.0.1:5013/filter`にアクセスする | `[No Filter]`の下は`This is a pen.`のまま、`[Filter]`の下は`{% filter upper %}`によって`THIS IS A PEN.`と大文字に変換されて表示される |
| `http://127.0.0.1:5013/filter2`にアクセスする | `[First User]`は先頭ユーザー（`Name:Tom Age:20`）、`[Last User]`は末尾ユーザー（`Name:Anna Age:60`）、`[Number of Users]`は`5`、`[Join User]`は5人が`=>`区切りで連結されて表示される |
| `/filter2`を何度かリロードする | `[Random User]`の行だけ表示されるユーザーがリロードのたびにランダムに変わる（`\| random`フィルターのため） |
| `http://127.0.0.1:5013/filter3`にアクセスする | `show_word1`（`寿限無`、3文字）は`truncate`のデフォルト長10文字以下なのでそのまま表示され、`truncate(2)`を指定すると2文字+`...`に短縮される。`show_word2`（15文字の長い文字列）は10文字+`...`に短縮される |
| `http://127.0.0.1:5013/abort`にアクセスする | `404.html`のエラーページが表示される（`@app.errorhandler(NotFound)`が効いている証拠） |

**正常な状態の見分け方**：`truncate`は文字数が指定した長さ以下ならそのまま、超えていれば`...`付きで切り詰められるのが正しい動作です。文字数に関係なく常に切り詰められる、または常にそのまま表示される場合は`if len(value) > length`の判定ミスを疑ってください。
