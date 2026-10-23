# 02 セマンティックHTMLとフォーム

> フロントエンド編 ／ 前の章：[01_html_basics](../01_html_basics/) ／ 次の章：[03_css_basics](../03_css_basics/)

[01_html_basics](../01_html_basics/)で学んだタグを使って、**ページ全体の構造**を意味の伝わる形で組み立てる方法（セマンティックHTML）と、ユーザーの入力を受け取る**フォーム**を学びます。

章の最後の制作課題では、自分を紹介するオリジナルHPのHTMLを書きます。見た目は素っ気なくて構いません。このHTMLに[04_css_layout](../04_css_layout/)でスタイルを付け、[06_js_events](../06_js_events/)・[08_js_render](../08_js_render/)で動きを付けて完成させていきます。

## 目次

1. [セマンティックHTMLとアクセシビリティ](#1-セマンティックhtmlとアクセシビリティ)
2. [フォーム](#2-フォーム)
- [制作課題：オリジナルHP（ステップ1）](#制作課題オリジナルhpステップ1)

---

## フォルダ構成

```
01_frontend/02_html_semantic_form/
├── README.md
├── example/                      サンプル（1つのサンプル＝1つのフォルダ）
│   ├── 01_semantic/              セマンティックHTML（header/nav/main/article/section/aside/footer）
│   │   ├── index.html
│   │   └── img/sample.png
│   └── 02_form/                  フォーム（input の種類・fieldset・検証属性）
│       └── index.html
├── question/                     練習問題（2問。問題文はREADMEの各節の最後）
│   ├── 01_semantic_blog/         練習問題1：divだらけのページをセマンティックHTMLに書き換える
│   │   ├── index.html
│   │   └── img/sample.png
│   ├── 02_register_form/         練習問題2：ユーザー登録フォームのHTMLを書く
│   │   └── index.html
│   └── answer/                   解答（問題と同じ名前のフォルダ。中のファイル構成も問題と同じ）
│       ├── 01_semantic_blog/
│       └── 02_register_form/
└── challenge/               制作課題（オリジナルHP）ステップ1：4ページのHTMLの雛形（TODOを書く）
    └── answer/              完成例
```

---

## 1. セマンティックHTMLとアクセシビリティ

> [example/01_semantic/index.html](example/01_semantic/index.html)

**セマンティック（semantic）**＝「意味のある」。`div`だけでもページは作れますが、内容に合った意味を持つタグを使うと、検索エンジン・読み上げソフト・他の開発者に「どこが何か」が伝わります。

```html
<header>
    <p><strong>サイト名</strong></p>
    <nav>
        <ul>
            <li><a href="#">ホーム</a></li>
            <li><a href="#">記事一覧</a></li>
        </ul>
    </nav>
</header>

<main>
    <article>
        <h1>記事タイトル</h1>
        <p>公開日：<time datetime="2026-10-01">2026年10月1日</time></p>
        <section>
            <h2>節の見出し</h2>
            <p>本文</p>
        </section>
    </article>
    <aside>関連記事など</aside>
</main>

<footer><small>&copy; 2026 サイト名</small></footer>
```

### ポイント

| タグ | 意味 | よくある使い場所 | 書き方（使い方） |
|---|---|---|---|
| `<header>` | 導入部分 | サイト名・ナビゲーション | `<header>`<br>`  <p><strong>サイト名</strong></p>`<br>`  <nav>…</nav>`<br>`</header>` |
| `<nav>`（navigation） | 主要なナビゲーション | メニューのリンク群（中身は`ul`/`li`で書く） | `<nav>`<br>`  <ul>`<br>`    <li><a href="#">ホーム</a></li>`<br>`  </ul>`<br>`</nav>` |
| `<main>` | ページの主な内容。**1ページに1つ** | ページ固有の内容全体 | `<main>`<br>`  …ページの内容…`<br>`</main>` |
| `<article>` | それ単体で完結する内容 | ブログ記事・ニュース・**1件のメモカード** | `<article>`<br>`  <h1>記事タイトル</h1>`<br>`  …`<br>`</article>` |
| `<section>` | 見出しを持つ内容のまとまり | 記事の章・節 | `<section>`<br>`  <h2>節の見出し</h2>`<br>`  <p>本文</p>`<br>`</section>` |
| `<aside>` | 本文の補足 | サイドバー・関連リンク | `<aside>`<br>`  <h2>関連記事</h2>`<br>`  …`<br>`</aside>` |
| `<footer>` | 締めくくり | 著作権表示・問い合わせ先 | `<footer>`<br>`  <small>&copy; 2026 サイト名</small>`<br>`</footer>` |
| `<time datetime="...">` | 日時 | 投稿日・期限 | `<time datetime="2026-10-01">2026年10月1日</time>`<br>`datetime`に機械が読める形式の日付、中に読みやすい表記 |
| `<figure>`<br>`<figcaption>`（figure caption） | 図とその説明 | 画像＋キャプション | `<figure>`<br>`  <img src="img/sample.png" alt="…">`<br>`  <figcaption>図の説明</figcaption>`<br>`</figure>` |

**迷ったら**：「スタイルを当てるためだけの箱」なら`div`、「意味のあるまとまり」ならセマンティックタグ。

### 文字・見出し・画像まわりの補足

| 項目 | 説明 |
|---|---|
| `<strong>`と`<b>` | `strong`は「意味として重要」な部分に使う。`b`は見た目が太字になるだけで意味を持たない。重要な語句には`strong`を使う（練習問題1の「とても大事」） |
| `<small>` | 著作権表示・注意書きなどの**細かい補足文**に使う（`<footer><small>&copy; 2026 サイト名</small></footer>`）。文字を小さくするためのタグではない |
| `h1`は1ページに1つ | `h1`はそのページの主題（記事ページなら記事タイトル）。サイト名は見出しではなく、`<p><strong>サイト名</strong></p>`のように書く。その下の見出しは`h2`→`h3`の順に、レベルを飛ばさず使う |
| `aside`の中にも見出しを付ける | 「関連記事」のような補足のまとまりにも見出しを付ける。`h1`は使い済みなので`h2`にする |
| `img`の`width`・`height` | 画像の表示サイズ（px）。書いておくと、画像の読み込み前から場所が確保され、読み込み時にレイアウトがずれにくい |

### アクセシビリティの基本

アクセシビリティ（a11y）とは、障害の有無や利用環境に関わらず誰でも使えるようにすることです。特別なことより、まず**正しいHTMLを書くこと**が一番の対策です。

| やること | 理由 |
|---|---|
| `<html lang="ja">`を書く | 読み上げソフトが日本語として発音する |
| 見出しレベルを飛ばさない | 読み上げソフト利用者は見出しで目次のように移動する |
| `img`に`alt`を書く（装飾だけの画像は`alt=""`） | 画像が見えない人に内容を伝える。空の`alt`は「読み飛ばしてよい」の意味 |
| 押して動くものは`<button>`、ページ移動は`<a>` | `div`にクリック処理を付けると、キーボード（Tabキー）で操作できない |
| フォームには`<label>`を付ける（2節） | 入力欄が何かを読み上げられる。ラベルクリックで入力欄を選べる |
| リンク文字を「こちら」にしない | リンクだけを読み上げたときに行き先がわからない |

### 動作確認：構造を確かめる

| 確認する操作 | 確認したいこと |
|---|---|
| `01_semantic/index.html`を開く | 各領域に点線の枠と`<header>`などのラベルが表示され、ページがどのタグで構成されているかがわかる |
| ページをクリックしてから`Tab`キーを何回か押す | リンクに順番にフォーカスが移る（`a`や`button`は何もしなくてもキーボードで操作できる） |
| 開発者ツールのElementsで`<main>`を折りたたむ | `header`・`main`・`footer`の3つの大きなまとまりでページが構成されていることがわかる |


### 練習問題1：divだらけのページをセマンティックHTMLに書き換える

> 問題：[question/01_semantic_blog/index.html](question/01_semantic_blog/index.html) ｜ 解答：[question/answer/01_semantic_blog/index.html](question/answer/01_semantic_blog/index.html)

<details>
<summary>問題の内容を開く</summary>

`01_semantic_blog/index.html`は、見た目は問題ありませんが、すべて`div`で書かれているため、検索エンジンや読み上げソフトには「どこがナビで、どこが本文か」が伝わりません。次のとおりにタグを書き換えます。

| # | 書き換える部分 | 書き換え後 |
|---|---|---|
| 1 | ページ上部（サイト名とメニュー）の`div` | `header` |
| 2 | メニュー（リンクが並ぶ部分）の`div` | `nav`。中のリンクは`ul`/`li`のリストにする |
| 3 | ページの主な内容全体を囲む`div` | `main` |
| 4 | 記事1件を囲む`div` | `article` |
| 5 | 記事タイトル（大きな文字の`div`） | 適切なレベルの見出し（ページで1つの`h1`） |
| 6 | 小見出し（やや大きな文字の`div`） | `h2`。小見出しとその本文を`section`で囲む |
| 7 | 日付 | `time`要素（`datetime`属性に`2026-10-01`） |
| 8 | 関連記事の`div` | `aside` |
| 9 | ページ最下部（著作権表示）の`div` | `footer` |
| 10 | 「とても大事」の部分 | `strong` |
| 11 | 画像 | 内容を説明する`alt`を付ける |

| 確認する操作 | 確認したいこと |
|---|---|
| 開発者ツールのElementsを見る | タグが書き換わっている |
| 書き換える前と見比べる | 見た目がほぼ変わらない（CSSは元のまま、タグだけを書き換えているため） |

</details>

---

## 2. フォーム

> [example/02_form/index.html](example/02_form/index.html)

フォームは、ユーザーの入力をサーバーに送る仕組みです。ここで作るお問い合わせフォームは`02_backend/09_forms`の練習問題と同じ項目構成で、`02_backend/08_request`・`02_backend/09_forms`ではFlask側でこの値を受け取ります。

```html
<form action="#" method="post">
    <div>
        <label>お名前（必須）
            <input type="text" name="name" required maxlength="50">
        </label>
    </div>

    <div>
        <label>メールアドレス（必須）
            <input type="email" name="email" required>
        </label>
    </div>

    <fieldset>
        <legend>ご希望の連絡方法</legend>
        <label><input type="radio" name="contact" value="email" checked> メール</label>
        <label><input type="radio" name="contact" value="tel"> 電話</label>
    </fieldset>

    <div>
        <label>メッセージ（必須・10文字以上）
            <textarea name="message" rows="5" required minlength="10"></textarea>
        </label>
    </div>

    <button type="submit">送信</button>
</form>
```

### form と送信の仕組み

| 属性 | 説明 |
|---|---|
| `action` | 送信先のURL。省略すると今のページに送信される |
| `method="get"` | 入力値がURLの後ろに`?name=値&email=値`の形で付く。検索フォームなど、URLを共有したいときに使う |
| `method="post"` | 入力値はリクエストの本文に入りURLには出ない。データの登録・変更に使う |
| `name` | サーバーに送られるときの**項目名**。`name`が無い入力欄は**送信されない** |
| `value` | 送信される値。ラジオボタン・チェックボックス・`option`では必須 |

### label：入力欄の説明を付ける

入力欄には、何を入力するのかを示す`<label>`を付けます。**`<label>`で入力欄を包む**と、ラベルの文字をクリックしたときに入力欄が選ばれ、読み上げソフトも入力欄の名前を読み上げます。

```html
<label>メールアドレス
    <input type="email" name="email">
</label>
```

### name・value：送信される項目名と値

似た名前の属性が並ぶので、**何のための属性か**を整理します。

| 属性 | 誰が使う？ | 役割 |
|---|---|---|
| `name` | **サーバー** | 送信されるときの項目名。Flaskでは`request.form["name"]`のように、この名前で値を取り出す |
| `value` | **サーバー** | 送信される値。テキスト欄は入力した文字が値になるので書かない |

送信されるのは「`name`＝値」の組です。上のメールアドレスの入力欄に`taro@example.com`と入力して送信すると、`email=taro@example.com`がサーバーに届きます。`name`を書き忘れると、この欄は**まるごと送られません**。

ラジオボタンとチェックボックスでは、`name`と`value`の両方が大切です。

```html
<label><input type="radio" name="contact" value="email" checked> メール</label>
<label><input type="radio" name="contact" value="tel"> 電話</label>
```

- ラジオボタンは**`name`が同じもの同士が1つのグループ**になり、グループの中から1つしか選べません。`name`を変えると別グループになり、両方選べてしまいます。
- 画面に見える文字（「メール」「電話」）と、送られる値（`email`・`tel`）は別です。選んだものの`value`が送られるので、上で「メール」を選んで送信すると`contact=email`が届きます。
- ラジオボタンやチェックボックスも`<label>`で包むと、文字をクリックして選べます。
- チェックボックスは、チェックを入れたときだけ`name=value`が送られます。チェックを外したままだと、その`name`自体が送られません。

### 入力部品

| 部品 | 用途 | 書き方（使い方） |
|---|---|---|
| `<label>` | 入力欄の説明。入力欄を包む。クリックで入力欄が選ばれる | `<label>メールアドレス`<br>`  <input type="email" name="email">`<br>`</label>` |
| `<input type="text">` | 1行テキスト | `<input type="text" name="name">` |
| `<input type="email">`<br>`<input type="tel">`<br>`<input type="url">` | 形式に合わせたチェックとスマホのキーボードの切り替え | `<input type="email" name="email">`<br>`<input type="tel" name="tel">`<br>`<input type="url" name="site">` |
| `<input type="password">` | 入力が伏せ字になる | `<input type="password" name="password">` |
| `<input type="number">`<br>`<input type="date">` | 数値 / 日付（ブラウザが専用の入力UIを出す） | `<input type="number" name="age">`<br>`<input type="date" name="date">` |
| `<input type="radio">` | `name`を揃えたグループの中から1つを選ぶ。`checked`を付けると最初から選ばれた状態になる | `<label><input type="radio" name="contact" value="email" checked> メール</label>`<br>`<label><input type="radio" name="contact" value="tel"> 電話</label>` |
| `<input type="checkbox">` | 複数選べる / オン・オフ。`checked`で最初からチェック済みにできる。`value`は送られる値で、`yes`など意味が通れば何でもよい | `<label><input type="checkbox" name="agree" value="yes"> 同意する</label>` |
| `<select>`<br>`<option>` | ドロップダウン。`selected`で初期選択（ラジオボタン・チェックボックスの`checked`に当たる） | `<select name="category">`<br>`  <option value="general">一般</option>`<br>`  <option value="support" selected>サポート</option>`<br>`</select>` |
| `<textarea>`（text area） | 複数行テキスト。`rows`で表示する行数を指定する | `<textarea name="message" rows="5"></textarea>`<br>`<input>`と違って終了タグが必要 |
| `<fieldset>`<br>`<legend>` | 関連する入力欄のグループとそのタイトル（ラジオボタンのまとまりに必須） | `<fieldset>`<br>`  <legend>ご希望の連絡方法</legend>`<br>`  …ラジオボタンなど…`<br>`</fieldset>` |
| `<button>` | 送信。`type="reset"`は初期化、`type="button"`は何もしない（JavaScript用） | `<button type="submit">送信</button>`<br>`<button type="reset">リセット</button>` |

### ブラウザによる入力チェック（検証属性）

| 属性 | 意味 | 書き方（使い方） |
|---|---|---|
| `required` | 必須 | `<input type="text" name="name" required>` |
| `minlength`<br>`maxlength` | 文字数の下限 / 上限 | `<input type="text" name="name" minlength="2" maxlength="50">` |
| `min`<br>`max`<br>`step` | 数値・日付の範囲と刻み | `<input type="number" name="age" min="0" max="120" step="1">` |
| `pattern="[0-9]{10,11}"` | 正規表現で形式を指定 | `<input type="tel" name="tel" pattern="[0-9]{10,11}" title="ハイフンなしの10〜11桁">`<br>`title`はエラー時のヒントとして表示される |
| `placeholder` | 入力例。**ラベルの代わりにはしない**（入力を始めると消えるため） | `<input type="email" name="email" placeholder="taro@example.com">` |
| `autocomplete="..."` | ブラウザの自動入力のヒント。値で「何の欄か」を伝える（下表） | `<input type="email" name="email" autocomplete="email">` |

`required`・`checked`・`selected`のように**値を持たない属性**は、`required="required"`とは書かず、`required`だけを書きます（書いてあればオン、無ければオフ）。

`autocomplete`によく使う値：

| 値 | 使う欄 |
|---|---|
| `username` | ユーザー名・ログインID。保存済みの情報が候補に出る |
| `email` | メールアドレス |
| `new-password` | **新規登録**のパスワード。ブラウザが強いパスワードを提案してくれる |
| `current-password` | **ログイン**のパスワード。保存済みのパスワードが入力される |

> ⚠️ これらは**ブラウザ側だけ**のチェックです。開発者ツールで属性を消せば簡単にすり抜けられるため、`02_backend/09_forms`で必ず**サーバー（Python）側でも検証**します。

### 動作確認：送信とブラウザの入力チェック

| 確認する操作 | 確認したいこと |
|---|---|
| `02_form/index.html`を開き、「お名前」のラベルをクリックする | 「お名前」の入力欄にカーソルが移る（`label`で入力欄を包んでいる） |
| 何も入力せずに「送信」を押す | ページ遷移せず、「このフィールドを入力してください」などの吹き出しが出る（`required`） |
| メールアドレスに`abc`と入れて送信 | 「@を含めてください」などの吹き出しが出る（`type="email"`） |
| 電話番号に`090-1234`と入れて送信 | `title`に書いたヒントが吹き出しに表示される（`pattern`） |
| 「メール」と「電話」のラジオボタンを交互に押す | 同時には選べない（`name`が同じ） |
| `method="post"`を`method="get"`に変え、すべて正しく入力して送信（確認後は戻す） | URLの後ろに`?name=...&email=...`が付く。チェックを入れなかったチェックボックスは送られていない |
| 開発者ツールで「お名前」の`required`を削除して空欄で送信 | 送信できてしまう（ブラウザのチェックだけでは不十分な理由） |


### 練習問題2：ユーザー登録フォームのHTMLを書く

> 問題：[question/02_register_form/index.html](question/02_register_form/index.html) ｜ 解答：[question/answer/02_register_form/index.html](question/answer/02_register_form/index.html)

<details>
<summary>問題の内容を開く</summary>

この先の`02_backend/15_login`で作る「ユーザー登録」画面のHTMLを先に作ります。見た目は[04_css_layoutの練習問題4](../04_css_layout/#練習問題4フォームを装飾する)で整えるので、ここでは「正しい部品・属性を選ぶ」ことに集中します。`02_register_form/index.html`の`form`の中に、次の項目を作ります。

| 項目 | name | 種類・条件 |
|---|---|---|
| ユーザー名 | `username` | テキスト / 必須 / 最大50文字 |
| メールアドレス | `email` | メール形式 / 必須 |
| パスワード | `password` | パスワード / 必須 / 4文字以上。下に「4文字以上で入力してください」のヒント |
| パスワード（確認） | `confirm` | パスワード / 必須 / 4文字以上 |
| 主な用途 | `purpose` | ラジオボタン（仕事 / 勉強 / プライベート）、`fieldset`＋`legend` |
| お知らせメール | `newsletter` | チェックボックス1つ（「お知らせメールを受け取る」） |
| 登録ボタン | - | `type="submit"` |

| # | ルール |
|---|---|
| 1 | 各項目は`<div>`で囲む（`fieldset`は除く） |
| 2 | 項目名は`<label>`で入力欄を包んで付ける |
| 3 | パスワードの下に、ヒントの`<p>`を置く（`div`の中、`label`の外） |
| 4 | ラジオボタン・チェックボックスには`value`を付ける。ラジオボタンは「仕事」を最初から選択しておく |
| 5 | `autocomplete`も付ける（`username` / `email` / `new-password`） |

<details>
<summary>ヒント：使うタグ</summary>

| タグ・属性 | 使う場所 |
|---|---|
| `<div>` | 各項目を囲む |
| `<label>項目名 <input ...></label>` | 項目名（入力欄を`label`で包む） |
| `<input type="text">` / `type="email"` / `type="password"` | ユーザー名 / メールアドレス / パスワード |
| `required` / `maxlength` / `minlength` | 必須 / 最大文字数 / 最小文字数 |
| `autocomplete="username"` など | ブラウザの自動入力 |
| `<fieldset>` / `<legend>` | ラジオボタンのまとまり / その見出し「主な用途」 |
| `<input type="radio" value="..." checked>` | 主な用途（`name`をそろえる。「仕事」に`checked`） |
| `<input type="checkbox" value="...">` | お知らせメール |
| `<button type="submit">` | 登録ボタン |

ラジオボタン・チェックボックスも、`<label><input ...> 仕事</label>`のように`label`で囲むと、文字をクリックして選べます。

</details>

| 確認する操作 | 確認したいこと |
|---|---|
| ラベルをクリックする | 対応する入力欄にカーソルが移る |
| 空欄のまま登録ボタンを押す | ブラウザが入力を求める吹き出しを出す |
| パスワードに3文字だけ入れて登録ボタンを押す | 文字数が足りない旨の吹き出しが出る |
| ラジオボタンを順に押す | 1つしか選べない |

「パスワードと確認が一致するか」はHTMLだけではチェックできません（`02_backend/09_forms`でPython側に実装します）。

</details>

---

## 制作課題：オリジナルHP（ステップ1）

> [challenge/](challenge/) — 雛形 ｜ [challenge/answer/](challenge/answer/) — 完成例 ｜ 自分のHP：[00_my_homepage/](../00_my_homepage/)

フロントエンド編のゴールは、**自分を紹介するオリジナルのHP**を完成させることです。練習問題が「決められたものを正確に作る」練習なのに対し、こちらは「学んだことを使って自分で考えて作る」練習です。各章の最後に少しずつ作り進めます。

ステップ1では、HPの**HTMLだけ**を書きます。見た目はまだ気にしません。自分のHPに取りかかる前に、[00_my_homepage/](../00_my_homepage/)のREADMEの「個人情報についての注意」を必ず読んでください。

制作課題は、毎回次の2段階で進めます。

1. **`challenge/`で練習する**：架空の人物「山田 太郎」のサイトを題材に、ファイルの中のTODOコメントに沿って書きます。書けたら`challenge/answer/`の完成例と見比べます。
2. **自分のHPに反映する**：同じことを、[00_my_homepage/](../00_my_homepage/)の自分のサイトに行います。こちらは文章・配色・レイアウトを自分で考えて作ります。下の「必須要件」は、自分のHPで満たすべき要件です。

### challenge/ の内容

| ファイル | 内容 |
|---|---|
| `index.html`・`about.html`・`works.html`・`contact.html` | `<head>`の一部と、`header`・`main`・`footer`の枠だけが書いてある。TODOコメントに、書く要素が指定してある |
| `img/avatar.png` | ホームで使うアイコン画像 |

### 必須要件

| 要件 | 使う節 |
|---|---|
| 4ページ以上（ホーム `index.html`・プロフィール `about.html`・制作実績 `works.html`・お問い合わせ `contact.html`）。作品がまだ無ければ、制作実績の代わりに「好きなもの紹介」などでもよい | 01_html_basics 1 |
| 全ページで同じ`header`（サイト名＋`nav`の中にリンクの`ul`）と`footer`を持つ | 01_html_basics 2・1 |
| 各ページに`<title>`があり、ページごとに内容が違う | 01_html_basics 1 |
| `h1`は各ページ1つ。見出しレベルを飛ばさない | 01_html_basics 2・1 |
| 画像を1枚以上使い、内容を説明する`alt`を付ける | 01_html_basics 2 |
| 表（`table`・`caption`・`th scope`）を1つ以上使う（スキル一覧など） | 01_html_basics 3 |
| `main`・`section`・`article`などのセマンティックタグで構造を表す | 1 |
| お問い合わせページに、`label`付きのフォーム（3項目以上・`required`などの検証属性付き） | 2 |
| [W3C Validator](https://validator.w3.org/#validate_by_input)で全ページのエラーが0件 | 01_html_basics 0 |

### 進め方のヒント

1. まず紙やメモに、各ページに載せる内容を箇条書きにする（ホームに何を置くか、プロフィールで何を伝えるか）
2. ホームの`header`・`footer`を書き、残りのページにコピーしてから中身を書く
3. CSSが無い状態で開いて、上から順に読んで意味が通るか確認する
4. 自分のHPでは、`challenge/answer/`の構造を参考にしてよいが、文章は自分のものにする

### 動作確認：challenge/

| 確認する操作 | 確認したいこと |
|---|---|
| `challenge/index.html`をブラウザで開き、ナビのリンクで4ページを行き来する | どのページにも同じヘッダーとフッターがあり、リンクで移動できる |
| CSSが無い状態で、各ページを上から読む | 見出し・リスト・表・フォームの順に、内容が読み取れる |
| 開発者ツールのElementsで各ページを見る | `header`・`nav`・`main`・`section`・`footer`が使われている |
| [W3C Validator](https://validator.w3.org/#validate_by_input)に4ページを貼り付ける | エラーが0件 |
| `challenge/answer/`と見比べる | 構造が同じになっている（文章は違っていてよい） |

## 次のステップ

続きは [03_css_basics](../03_css_basics/) です。CSSの書き方と、文字と色・セレクタ・背景と装飾などの基本のルールを学びます。
