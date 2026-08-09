# 002 HTML/CSSの基礎

Flaskに入る前に、Webページの土台となるHTML/CSSの基礎を学びます。Python・Flaskはまだ使いません。最後に、`100_bookstore_api`（完成形の参考例）のトップページ（書籍一覧）を**静的なHTML/CSSだけ**で再現する演習を行い、これを自分の統合アプリ[000_my_app](../000_my_app/)に組み込む最初のパーツにします。この静的なページに、この先の章でFlask・データベース・ログイン機能などを少しずつ組み込んでいくことで、`000_my_app`を`100_bookstore_api`と同等の完成形に育てていく、というのがこのカリキュラム全体の道のりです。

各章は「機能の学習」と「`000_my_app`を完成させるための機能追加」の2部構成です。前者は`example/`で単体のサンプルとして学び、後者は`challenge/`で`100_bookstore_api`を完成形の参考にしながら取り組みます。

## 目次

1. [HTMLの基本タグ](#1-htmlの基本タグ)
2. [CSSセレクタの基本](#2-cssセレクタの基本)
3. [CSSとボックスモデル](#3-cssとボックスモデル)
4. [Flexboxでナビゲーションを作る](#4-flexboxでナビゲーションを作る)
5. [Gridでカードを並べる](#5-gridでカードを並べる)
6. [レスポンシブ対応](#6-レスポンシブ対応)
7. [フォームの基本](#7-フォームの基本)
8. [演習：000_my_appのトップページを作る](#8-演習000_my_appのトップページを作る)

---

## フォルダ構成

```
002_html_css/
├── README.md
├── example/
│   ├── 01_basic.html        HTMLの基本タグ
│   ├── 02_selectors.html    CSSセレクタ（要素・クラス・ID・子孫）
│   ├── 03_box_model.html    ボックスモデル（padding/border/margin）
│   ├── 04_flexbox.html      Flexboxでのナビゲーション
│   ├── 05_grid.html         Gridでのカード配置
│   ├── 06_responsive.html   レスポンシブ対応（メディアクエリ）
│   ├── 07_form.html         フォームの基本（お問い合わせフォーム）
│   └── img/sample.png
└── challenge/                 000_my_appに組み込む機能の雛形（ここに書き込んでいく）
    ├── index.html
    ├── style.css
    ├── img/                   書籍の表紙画像5枚
    └── answer/                完成例（100_bookstore_apiと同じ見た目になる）
        ├── index.html
        ├── style.css
        └── img/
```

---

## 1. HTMLの基本タグ

> [example/01_basic.html](example/01_basic.html)

```html
<h1>見出し1</h1>
<h2>見出し2</h2>
<p>これは段落です。<a href="https://developer.mozilla.org/ja/">MDN</a>のようにリンクを貼れます。</p>

<ul>
    <li>順序なしリストの項目1</li>
</ul>

<ol>
    <li>順序ありリストの項目1</li>
</ol>

<img src="img/sample.png" alt="サンプル画像" width="150">

<div>
    <p>divは意味を持たない汎用ブロック要素。レイアウトのための箱として使う。</p>
</div>
```

### ポイント

| タグ | 役割 |
|---|---|
| `<h1>`〜`<h6>` | 見出し。数字が小さいほど重要度が高い |
| `<p>` | 段落 |
| `<a href="...">` | リンク |
| `<ul>` / `<ol>` / `<li>` | 順序なし／順序ありリスト |
| `<img src="..." alt="...">` | 画像。`alt`は画像が表示できないときの代替テキスト（アクセシビリティ上必須） |
| `<div>` | 意味を持たない汎用のブロック要素。CSSでレイアウトを組むための「箱」として使う |
| `<span>` | 意味を持たない汎用のインライン要素。文章の一部だけを装飾したいときに使う（`<div>`の行内版） |
| `<table>` / `<tr>` / `<th>` / `<td>` | 表。`<tr>`が行、`<th>`が見出しセル、`<td>`が通常セル。`100_bookstore_api`のカート画面で使われている |

入力フォーム系のタグ（`<input>`/`<label>`/`<button>`など）は「6. フォームの基本」で扱います。

### 実行方法

`example/01_basic.html` をブラウザで直接開いてください（`ファイルを開く`、またはVS Codeの拡張機能「Live Server」を使うと便利です）。

---

## 2. CSSセレクタの基本

> [example/02_selectors.html](example/02_selectors.html)

CSSは「どの要素に」「どんなスタイルを」適用するかを**セレクタ**で指定します。ここまでの`.card`や`.card-grid`のような書き方の意味がここでわかります。

```css
/* 要素セレクタ: すべての <p> に適用される */
p {
    color: red;
}

/* クラスセレクタ: class="highlight" を持つ要素に適用される（. から始まる） */
.highlight {
    background: yellow;
}

/* IDセレクタ: id="title" を持つ要素だけに適用される（# から始まる） */
#title {
    font-size: 32px;
}

/* 子孫セレクタ: .card の中にある <p> だけに適用される */
.card p {
    color: gray;
}
```

```html
<h1 id="title">タイトル</h1>
<p class="highlight">この段落だけ黄色くなる</p>
<div class="card"><p>この段落だけ子孫セレクタの対象になる</p></div>
```

### 使い分け

| セレクタ | 記法 | 使う場面 |
|---|---|---|
| 要素セレクタ | `p { }` | そのタグ全体に共通のスタイルを当てたいとき |
| クラスセレクタ | `.card { }` | 同じスタイルを複数の要素で使い回したいとき（**最もよく使う**） |
| IDセレクタ | `#title { }` | ページ内で1つだけの要素を指定したいとき |
| 子孫セレクタ | `.card p { }` | 「特定の親の中にある要素だけ」に絞りたいとき |

`100_bookstore_api`のCSSでも、`.card`・`.card-grid`・`.card img`（子孫セレクタ）のように、ほぼクラスセレクタと子孫セレクタだけで組まれています。

### 実行方法

`example/02_selectors.html` をブラウザで開き、それぞれの段落の色が変わることを確認してください。

---

## 3. CSSとボックスモデル

> [example/03_box_model.html](example/03_box_model.html)

CSSでは、すべての要素が**箱（ボックス）**として扱われます。

```
┌─────────────── margin（外側の余白） ───────────────┐
│  ┌───────────── border（枠線） ─────────────────┐  │
│  │  ┌───────── padding（内側の余白） ─────────┐  │  │
│  │  │              content（中身）              │  │  │
│  │  └────────────────────────────────────────┘  │  │
│  └────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────┘
```

```css
.box {
    width: 200px;
    padding: 20px;
    border: 4px solid #3f6fd1;
    margin: 30px;
}
```

### `box-sizing: border-box`

デフォルト（`content-box`）では`width`は中身だけの幅を指し、実際の見た目は`padding`と`border`の分だけ広がります。`box-sizing: border-box`を指定すると、`width`に`padding`と`border`を含めて計算するようになり、サイズ計算が直感的になります。実務ではほぼ必ず指定します。

```css
.box-border-box {
    width: 200px;      /* paddingとborderを含めた幅がちょうど200pxになる */
    padding: 20px;
    border: 4px solid #d1723f;
    box-sizing: border-box;
}
```

### 実行方法

`example/03_box_model.html` をブラウザで開き、2つの箱の実際の幅の違いを確認してください。

---

## 4. Flexboxでナビゲーションを作る

> [example/04_flexbox.html](example/04_flexbox.html)

```css
nav {
    display: flex;
    align-items: center;
    gap: 16px;
}

.spacer {
    flex: 1;
}
```

### ポイント

| プロパティ | 説明 |
|---|---|
| `display: flex` | 子要素を横並びにする |
| `align-items: center` | 交差軸（縦方向）を中央揃えにする |
| `gap` | 子要素同士の間隔 |
| `flex: 1` | 余ったスペースをその要素が埋める。ナビの右寄せレイアウトによく使う |

`100_bookstore_api`のヘッダーの`nav`は、まさにこの`flex`の仕組みで組まれています。

### 実行方法

`example/04_flexbox.html` をブラウザで開いてください。

---

## 5. Gridでカードを並べる

> [example/05_grid.html](example/05_grid.html)

```css
.card-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, 150px);
    justify-content: center;
    gap: 16px;
}
```

### ポイント

| プロパティ | 説明 |
|---|---|
| `display: grid` | 子要素を格子状に並べる |
| `grid-template-columns: repeat(auto-fill, 150px)` | 幅150pxの列を、画面幅に収まるだけ自動的に並べる |
| `justify-content: center` | 列全体を中央寄せにする |

ブラウザの幅を変えながら開くと、列数が自動的に増減することを確認できます。`100_bookstore_api`の書籍一覧（カードグリッド）もこの仕組みです。

### 実行方法

`example/05_grid.html` をブラウザで開き、ウィンドウ幅を変えて列数の変化を確認してください。

---

## 6. レスポンシブ対応

> [example/06_responsive.html](example/06_responsive.html)

画面の幅（PC・タブレット・スマホ）に応じてレイアウトを切り替える仕組みを**レスポンシブ対応**と呼びます。CSSの**メディアクエリ**（`@media`）を使うと、「画面幅が◯◯px以下のときだけ、このCSSを適用する」という条件分岐ができます。

```css
.box-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
}

/* 画面幅が768px以下になったら2列にする */
@media (max-width: 768px) {
    .box-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}

/* 画面幅が480px以下になったら1列にする */
@media (max-width: 480px) {
    .box-grid {
        grid-template-columns: repeat(1, 1fr);
    }
}
```

### `<meta name="viewport">`

レスポンシブ対応には、`<head>`内に以下のタグが必須です。

```html
<meta name="viewport" content="width=device-width, initial-scale=1">
```

このタグが無いと、スマホのブラウザは「PC用のページだろう」と判断してページ全体を縮小表示してしまい、メディアクエリが意図通りに機能しません。`width=device-width`で「実際の画面幅通りに表示する」ことを指定しています。

### ポイント

| 記法 | 説明 |
|---|---|
| `@media (max-width: 768px) { ... }` | 画面幅が768px以下のときだけ、中のCSSを適用する |
| ブレークポイント | スタイルが切り替わる幅の境目。`768px`＝タブレット、`480px`＝スマホ相当がよく使われる目安 |
| `<meta name="viewport" ...>` | モバイルブラウザに実際の画面幅通りに表示するよう伝える。無いとメディアクエリが正しく機能しない |

`100_bookstore_api`の書籍一覧も、`5. Grid`で学んだ`.card-grid`にこのメディアクエリを組み合わせて、タブレットで2列・スマホで1列に切り替えています。

### 実行方法

`example/06_responsive.html` をブラウザで開き、ウィンドウ幅を狭めながら列数が3列→2列→1列と変化することを確認してください（ブラウザの開発者ツールのデバイスツールバーを使うと、スマホ幅を再現できます）。

---

## 7. フォームの基本

> [example/07_form.html](example/07_form.html)

`<form>`と入力系タグを使って、お問い合わせフォームを作ります。ここで作るフォームは、`009_forms`の練習問題（お問い合わせフォームをFlask-WTFで作る）と**同じ項目構成**にしてあります。まずはPythonなしの見た目だけを作り、`009_forms`で実際に送信・バリデーションできるようにする、という流れです。

```html
<form method="post">
    <div class="field">
        <label for="name">お名前</label>
        <input id="name" type="text" name="name" required>
    </div>

    <div class="field">
        <label for="category">お問い合わせ種別</label>
        <select id="category" name="category">
            <option value="general">一般</option>
            <option value="support">サポート</option>
        </select>
    </div>

    <div class="field">
        <label for="message">メッセージ</label>
        <textarea id="message" name="message" rows="5" required></textarea>
    </div>

    <button type="submit">送信</button>
</form>
```

### ポイント

| タグ・属性 | 役割 |
|---|---|
| `<form method="post">` | 入力内容をまとめて送信する箱。`method`は送信方法（`get`/`post`） |
| `<label for="name">` | `<input id="name">`と`for`/`id`を一致させると、ラベルクリックで入力欄にフォーカスが移る |
| `<input type="text">` | 1行のテキスト入力 |
| `<input type="email">` | メールアドレス用。ブラウザが簡易的に形式チェックしてくれる |
| `<select>` / `<option>` | ドロップダウンの選択肢 |
| `<textarea rows="5">` | 複数行の入力欄。`rows`で表示行数を指定 |
| `<button type="submit">` | フォームを送信するボタン |
| `required` | 入力必須にするHTML標準の属性（本格的な検証は`009_forms`でPython側にも実装する） |

### CSSでのフォーム整形

```css
label {
    display: block;      /* ラベルを input の上に配置する */
    margin-bottom: 4px;
}

input[type="text"],
input[type="email"],
select,
textarea {
    width: 100%;          /* 横幅いっぱいに広げる */
    box-sizing: border-box;
    padding: 6px;
}
```

`label`を`display: block`にすると、ラベルと入力欄が縦に並びます。属性セレクタ（`input[type="text"]`）を使うと、同じ`<input>`タグでも`type`ごとに別のスタイルを当てられます。

### 実行方法

`example/07_form.html` をブラウザで開いてください（`method="post"`ですが送信先が無いため、送信ボタンを押すとブラウザ上でページが再読み込みされるだけです。実際に送信処理を行うのは`009_forms`です）。

---

## 8. 演習：000_my_appのトップページを作る

> [challenge/](challenge/) — 演習の雛形 ｜ [challenge/answer/](challenge/answer/) — 完成例

ここまで学んだHTML/CSSの知識だけを使って、`000_my_app`のトップページ（書籍一覧画面）を静的なHTML/CSSで作ります。完成形の参考として`100_bookstore_api`のトップページと同じ見た目を目指します。Flask・Jinja・Pythonは一切使いません。

### 作るもの

| 部分 | 内容 |
|---|---|
| `<header>` | `<nav>`の中に、サイト名と「書籍一覧」リンク |
| `<main>` | `class="card-grid"`の中に、書籍カード（`class="card"`）を5つ |
| 各カード | 表紙画像・タイトル（`<h3>`）・著者（`<p>`）・価格（`<p>`） |
| `<footer>` | コピーライト表示 |
| レスポンシブ対応 | タブレット幅（768px以下）で2列、スマホ幅（480px以下）で1列になるようメディアクエリを追加する |

### 使う書籍データ

この先の章（`009_forms`など）のブックストアで繰り返し使う、以下の5冊を使います。

| タイトル | 著者 | 価格 | 画像ファイル |
|---|---|---|---|
| 吾輩は猫である | 夏目漱石 | ¥770 | `wagahai_neko.png` |
| 坊っちゃん | 夏目漱石 | ¥660 | `bocchan.png` |
| 羅生門 | 芥川龍之介 | ¥550 | `rashomon.png` |
| 銀河鉄道の夜 | 宮沢賢治 | ¥480 | `ginga_tetsudo.png` |
| 走れメロス | 太宰治 | ¥440 | `hashire_merosu.png` |

画像は`challenge/img/`に用意済みです。

### 進め方

1. `challenge/index.html`と`challenge/style.css`のTODOコメントに沿って実装する
2. ブラウザで開いて見た目を確認する（開発者ツールのデバイスツールバーでウィンドウ幅も狭めて、レスポンシブ対応まで確認する）
3. 一通り書けたら`challenge/answer/`の完成例と見比べる

### ヒント

- ヘッダーの配色・角丸は「4. Flexbox」で学んだ`nav`のスタイルがそのまま使える
- カードの並びは「5. Grid」で学んだ`.card-grid`がそのまま使える
- カード自体（`.card`）は白背景・枠線・角丸・軽い影（`box-shadow`）を付けると「カードらしく」見える
- 画像は`width: 100%; height: 160px; object-fit: cover;`で、サイズが不揃いでも綺麗に切り抜ける
- レスポンシブ対応は「6. レスポンシブ対応」で学んだ`@media (max-width: ...)`を`.card-grid`に追加すればよい
- 詰まったら[100_bookstore_api/app/static/style.css](../100_bookstore_api/app/static/style.css)と見比べてみる（完成形のCSSがそのまま置いてあります）

### この演習がこの先どうつながるか

作った静的ページは、この先の章で少しずつ`000_my_app`に機能を組み込んでいくための最初のパーツになります。

| 章 | この静的ページに何が加わるか |
|---|---|
| `004_flask_basic`〜 | Flaskでこのページを配信できるようにする |
| `006_jinja2` | `{% for %}`で書籍カードをループ処理し、ハードコードだった書籍データをPythonの変数から埋め込む |
| `009_forms`〜`015_login` | ログイン機能・DB連携を追加する |
| （最終形） | ここまでの集大成として、`000_my_app`が`100_bookstore_api`と同等の、実際に動くブックストアになる |

## 実行方法

```bash
cd 002_html_css/challenge
python -m http.server 8000
```

ブラウザで `http://localhost:8000` にアクセスしてください（`index.html`をブラウザで直接開くだけでも動作します）。
