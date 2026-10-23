# 03 CSSの基礎

> フロントエンド編 ／ 前の章：[02_html_semantic_form](../02_html_semantic_form/) ／ 次の章：[04_css_layout](../04_css_layout/)

CSS（Cascading Style Sheets）は、HTMLの要素に**見た目**を指定する言語です。

```css
セレクタ {
    プロパティ: 値;
    プロパティ: 値;
}
```

「**どの要素に**（セレクタ）」「**何を**（プロパティ）」「**どうする**（値）」の3つで1つのルールになります。

この章では、CSSの書き方・文字と色と単位・セレクタ（基本とclass/id）・背景の装飾を学びます。「どのルールが勝つか」を決めるカスケード・詳細度・継承は、章の最後の補足にまとめています。要素の大きさと余白を決めるボックスモデル、そして要素を横に並べる・格子状に並べる・画面幅に合わせるレイアウトは、次の[04_css_layout](../04_css_layout/)で扱います。

> 開発者ツールの使い方は[01_html_basicsの「0. はじめに」](../01_html_basics/#0-はじめに学習環境と開発者ツール)にまとめてあります。この章では特に、**Styles**パネルを使います。取り消し線（負けたルールがわかる）は、最後の補足で使います。

## 目次

1. [CSSの書き方](#1-cssの書き方)
2. [文字・色・単位](#2-文字色単位)
3. [基本のセレクタ](#3-基本のセレクタ)
4. [classとid](#4-classとid)
5. [背景・装飾](#5-背景装飾)
- [補足：カスケード・詳細度・継承](#補足カスケード詳細度継承)

---

## フォルダ構成

```
01_frontend/03_css_basics/
├── README.md
├── example/                      サンプル（1つのサンプル＝1つのフォルダ）
│   ├── 01_css_basics/            CSSの書き方（3つの場所）
│   │   ├── index.html
│   │   └── css/style.css
│   ├── 02_typography/            色・単位（px/%/em/rem/vw）・文字・行の高さ
│   │   └── index.html
│   ├── 03_selectors/             基本のセレクタ（要素・グループ化・子孫・:hover）
│   │   └── index.html
│   ├── 04_class_id/              classとid（クラスセレクタ・IDセレクタ・複数クラス）
│   │   └── index.html
│   ├── 05_decoration/            背景・グラデーション・角丸・影
│   │   └── index.html
│   └── 06_cascade/               （補足）カスケード・詳細度・継承
│       └── index.html
└── question/                     練習問題（5問。問題文はREADMEの各節の最後）
    ├── 01_units/                 練習問題1：単位と色を書き換える
    │   ├── index.html
    │   └── css/style.css
    ├── 02_basic_selectors/       練習問題2：基本のセレクタを書く
    │   └── index.html
    ├── 03_selectors/             練習問題3：プロパティに合うセレクタを書く
    │   └── index.html
    ├── 04_article_style/         練習問題4：記事ページを読みやすく装飾する
    │   └── index.html
    ├── 05_specificity_quiz/      練習問題5（補足）：何色になるか予想する（詳細度クイズ）
    │   └── index.html
    └── answer/                   解答（問題と同じ名前のフォルダ。中のファイル構成も問題と同じ）
        ├── 01_units/
        ├── 02_basic_selectors/
        ├── 03_selectors/
        ├── 04_article_style/
        └── 05_specificity_quiz/
```

---

## 1. CSSの書き方

> [example/01_css_basics/index.html](example/01_css_basics/index.html) ／ [example/01_css_basics/css/style.css](example/01_css_basics/css/style.css)

CSSは、「どの要素に（セレクタ）」「何を（プロパティ）」「どうする（値）」で1つのルールです。まず、そのルールを**どこに書くか**を学びます。ここでは、`h2`や`h3`などのタグ名をそのままセレクタに使います。

### CSSを書く3つの場所

```html
<!-- ① 外部ファイル（実務の基本） -->
<link rel="stylesheet" href="css/style.css">

<!-- ② <style>タグ（そのページだけのCSS） -->
<style>
    h3 { color: #d1723f; }   /* h3（見出し）を橙色にする */
</style>

<!-- ③ style属性（インラインスタイル） -->
<p style="color: #2f9e44;">...</p>
```

| 書き方 | 使いどころ |
|---|---|
| ① 外部ファイル | **基本はこれ**。複数ページで同じCSSを共有でき、HTMLと見た目を分離できる。Flaskでは`static/style.css`に置く |
| ② `<style>`タグ | 1ページだけのサンプル・試作（この章の`example/`はほぼこれ） |
| ③ `style`属性 | 原則使わない。使い回せず、優先度が強すぎて後から上書きしにくい（補足） |

### 動作確認：3つの書き方

| 確認する操作 | 確認したいこと |
|---|---|
| `01_css_basics/index.html`を開く | 見出し（h2）が青、見出し（h3）が橙、段落が緑で表示される（それぞれ別の場所に書いたCSSが効いている） |
| `01_css_basics/css/style.css`の`h2`の色を`red`に変えて保存・リロード | ①の見出し（h2）だけ赤くなる（外部ファイルが読み込まれている） |

---

## 2. 文字・色・単位

> [example/02_typography/index.html](example/02_typography/index.html)

文字の大きさや色は、書くとすぐ見た目が変わります。ここで、色と長さの書き方を学びます。

### 色の書き方

| 書き方 | 例 | 説明 |
|---|---|---|
| 色名 | `royalblue` | 決まった名前の色 |
| 16進数 | `#3f6fd1` | 赤・緑・青を2桁ずつ。最もよく使う |
| `rgb()` | `rgb(63 111 209)`、`rgb(63 111 209 / 0.5)` | `/ 0.5`で半透明 |
| `hsl()` | `hsl(220 62% 53%)` | 色相・彩度・明度。「同じ色で少し明るく」が作りやすい |

### 長さの単位

| 単位 | 基準 | 主な用途 |
|---|---|---|
| `px` | 画面上の1点 | 枠線・細かい余白 |
| `%` | 親要素のサイズ | 幅 |
| `em` | **その要素自身**の文字サイズ（`font-size`に使うと親の文字サイズ） | ボタンの内側余白など、文字の大きさに比例させたいもの |
| `rem` | **ルート（`html`）**の文字サイズ（通常16px） | **文字サイズ**・余白。入れ子の影響を受けないので計算しやすい |
| `vw` / `vh` | 画面の幅 / 高さの1% | 画面いっぱいの要素・流動的なサイズ |

文字サイズを`rem`で指定すると、ブラウザの設定で文字を大きくしたユーザーにも対応できます。

### 文字の書き方

```css
body {
    font-family: "Hiragino Sans", "Noto Sans JP", "Yu Gothic", sans-serif;
    font-size: 1rem;
    line-height: 1.7;
    color: #262b33;
}
```

| プロパティ | 説明 |
|---|---|
| `color` | 文字の色 |
| `font-family` | 候補を左から順に並べる（フォントスタック）。最後は総称ファミリー（`sans-serif`＝ゴシック体、`serif`＝明朝体）で終える |
| `font-size` / `font-weight` | 文字サイズ（`rem`推奨）/ 太さ（`400`＝標準、`700`＝太字） |
| `line-height` | 行の高さ。**単位なしの数値**で書く（文字サイズの何倍か）。日本語の本文は1.5〜1.8が読みやすい |
| `text-align` / `letter-spacing` | 揃え位置 / 字間 |
| `text-decoration` | 線の種類と形。`none`（線なし）・`underline`（下線）のほか、`underline dotted`（点線の下線）のように「位置 形」を並べて書ける（形は`solid`・`dotted`・`dashed`・`wavy`） |
| `white-space: nowrap` + `overflow: hidden` + `text-overflow: ellipsis` | 1行に収まらない文字を「…」で省略する3点セット |

### 動作確認

| 確認する操作 | 確認したいこと |
|---|---|
| `02_typography/index.html`を開く | 色見本（色名・16進数・`rgb()`・半透明・`hsl()`）が並ぶ |
| ウィンドウ幅を変える | `200px`のバーは変わらず、`50%`と`30vw`のバーは幅が変わる |
| `em`と`rem`の子要素の文字サイズを開発者ツールのComputedで確認 | `1.5em`は30px、`1.5rem`は24pxになっている |
| ゴシック体と明朝体、行間の広い段落と狭い段落を見比べる | 読みやすさの違いがわかる |
| 「はみ出した文字の省略」を見る | 長いタイトルの末尾が「…」になっている |


### 練習問題1：単位と色を書き換える

> 問題：[question/01_units/index.html](question/01_units/index.html)・[question/01_units/css/style.css](question/01_units/css/style.css) ｜ 解答：[question/answer/01_units/index.html](question/answer/01_units/index.html)・[question/answer/01_units/css/style.css](question/answer/01_units/css/style.css)

<details>
<summary>問題の内容を開く</summary>

`01_units/css/style.css`は、値が`px`で書かれたCSSです。ここでは値を書き換えるだけで、`.hero`などのセレクタは4節で学びます。`TODO 1`〜`TODO 5`の場所を、次のとおりに書き換えます。最後に、`index.html`の`<head>`に、`css/style.css`を読み込む`<link>`を書きます（`TODO 6`）。見た目はほぼ同じまま、ウィンドウの大きさや、ブラウザの文字サイズの設定に合わせて変わるようになります。

| # | 書く場所 | やること |
|---|---|---|
| 1 | `.hero` | 高さを「画面の高さの40%」にする（元は320px固定） |
| 2 | `.hero h1`・`.hero p`・`.content h2` | 文字サイズを`rem`で書く（元は40px・18px・24px。16px＝1rem） |
| 3 | `.notice` | 背景を`#3f6fd1`（＝`rgb(63 111 209)`）の15%の半透明にし、文字色を`#3f6fd1`にする（背景が薄くなったので、白い文字では読めない） |
| 4 | `.button` | 内側の余白を`em`で書く（文字サイズ16pxのとき、上下8px・左右16pxになるように） |
| 5 | `.button.large` | 文字サイズを`1.5rem`にする（余白は書かなくても、`em`なので一緒に大きくなる） |
| 6 | `01_units/index.html`の`<head>` | `css/style.css`を読み込む`<link>`を書く（1節の「CSSを書く3つの場所」の①） |

| 確認する操作 | 確認したいこと |
|---|---|
| ブラウザで開く | `<link>`を書く前は、CSSが読み込まれず装飾のないページになる。書くと、ヒーローの高さがウィンドウの高さに合わせて変わり、お知らせは薄い青の背景に青い文字になる |
| 開発者ツールのComputedで大きいボタンを見る | `padding`が`12px 24px`になっている |

</details>
---

## 3. 基本のセレクタ

> [example/03_selectors/index.html](example/03_selectors/index.html)

セレクタは、CSSで「どの要素に当てるか」を指定する書き方です。まず、タグの名前だけで書ける基本の4つを学びます。

| セレクタ | 記法 | 対象 |
|---|---|---|
| 要素（タイプ） | `p` | すべての`<p>` |
| グループ化 | `h1, h2` | カンマ区切りで複数に同じスタイル |
| 子孫 | `nav a` | `nav`の中にある`a`すべて（孫以下も）。間はスペース |
| `:hover` | `a:hover` | マウスが乗っているとき（疑似クラスの代表） |

```css
p             { line-height: 1.8; }          /* 要素 */
h1, h2        { color: #3f6fd1; }            /* グループ化 */
nav a         { text-decoration: none; }     /* 子孫：nav の中の a だけ */
nav a:hover   { background: #3f6fd1; }       /* :hover */
```

### 動作確認：セレクタごとの適用範囲

| 確認する操作 | 確認したいこと |
|---|---|
| `03_selectors/index.html`を開く | `p`は行の高さが広く、`h1`と`h2`は同じ青色になっている |
| 「子孫セレクタ」のリストを見る | `section`の中の`li`は、入れ子のリストも灰色になる。`section`の外の`li`は黒のまま |
| メニューにマウスを乗せる | `:hover`で背景が青くなる。本文中の`a`には、メニューのスタイルは当たらない |


### 練習問題2：基本のセレクタを書く

> 問題：[question/02_basic_selectors/index.html](question/02_basic_selectors/index.html) ｜ 解答：[question/answer/02_basic_selectors/index.html](question/answer/02_basic_selectors/index.html)

<details>
<summary>問題の内容を開く</summary>

`02_basic_selectors/index.html`のHTMLは完成しています。`<style>`の中はプロパティと値だけが書いてあり、セレクタが`TODO`になっています。`(1)`〜`(6)`のルールに、次の「対象」だけに当たるセレクタを書きます。HTMLは変更しません。

| # | 対象 | 確認したいこと |
|---|---|---|
| 1 | すべての`p` | すべての段落の行の間隔が広くなる |
| 2 | `h1`と`h2`の両方（1つのルールでまとめて） | `h1`と`h2`が青くなる（`h3`は黒のまま） |
| 3 | `article`の中にある`h3`だけ | 2つのメモのタイトル（`h3`）が灰色になる |
| 4 | `small` | 日付の2行が小さい文字になる |
| 5 | `nav`の**中にある**`a`だけ（最後の段落のMDNへのリンクは含まない） | 「メモ一覧」「メモを追加」「設定」の3つが、下線の無い丸いボタンの形になる。MDNへのリンクは普通のリンクのまま |
| 6 | `nav`の中の`a`に、マウスが乗っているとき | ボタンにマウスを乗せると、青背景・白文字になる |

あわせて、開発者ツールで要素を選び、Stylesパネルで意図したルールだけが当たっていることを確かめます。

</details>

---

## 4. classとid

> [example/04_class_id/index.html](example/04_class_id/index.html)

タグの名前だけでは、「同じ`p`でも、この段落だけ」のような指定ができません。そこで、HTMLの要素に**名前を付ける属性**（`class`・`id`）を使い、CSSからその名前で要素を選びます。

### HTMLの`class`と`id`：要素に名前を付ける属性

| 属性 | 書き方 | 説明 |
|---|---|---|
| `class` | `<td class="note">集計中</td>` | 同じ種類の要素に**何度でも**付けられる名前。空白で区切って複数付けられる（`class="button large"`）。CSSでは`.note`のように`.`を付けて選ぶ。**最もよく使う** |
| `id` | `<h2 id="steps">作り方</h2>` | ページの中で**1つだけ**の名前。同じ`id`を2か所に付けない。ページ内リンク（`href="#steps"`）の行き先や、`label`の`for`との対応、JavaScriptからの取得に使う。CSSでは`#steps`と書けるが、強すぎるので避ける（補足） |

```html
<p class="note">クラスを付けた段落</p>
<p class="note warning">クラスを2つ付けた段落</p>
<h2 id="steps">IDを付けた見出し</h2>
```

```css
.note    { color: gray; }   /* class="note" を持つ要素すべてに当たる */
#steps   { color: blue; }   /* id="steps" の要素1つに当たる */
```

`id`は、フォームでも使います。`<label for="email">`と`<input id="email">`のように、`label`の`for`と入力欄の`id`を同じ文字列にすると、ラベルと入力欄が対応します（02章で学んだ、`label`で入力欄を包む書き方と同じ効果です）。ページ内リンクは、`<a href="#steps">`で、同じページの`id="steps"`の要素へ移動します。

### クラスセレクタとIDセレクタ

| セレクタ | 記法 | 対象 |
|---|---|---|
| クラス | `.card` | `class="card"`を持つ要素（**最もよく使う**） |
| 複数クラス | `.button.large` | `class="button large"`のように**両方のクラスを持つ**要素。クラス名の間に**スペースを入れない**（スペースを入れると子孫セレクタになる） |
| ID | `#title` | `id="title"`の要素（ページ内で1つ）。詳細度が強すぎるのでCSSでは避け、ページ内リンクやJavaScript用に使うことが多い |

```css
.card         { border: 1px solid #e1e5eb; } /* クラス */
.menu a       { text-decoration: none; }     /* クラスと子孫：.menu の中の a だけ */
.button.large { font-size: 1.5rem; }         /* 複数クラス */
```

### 動作確認：classとid

| 確認する操作 | 確認したいこと |
|---|---|
| `04_class_id/index.html`を開き、段落を見比べる | `.highlight`は黄色の背景、`.note.warning`は左に橙の線、`.note`と`.tip`は文字が小さくなる。見出し（`id="title"`）は青色 |


### 練習問題3：プロパティに合うセレクタを書く

> 問題：[question/03_selectors/index.html](question/03_selectors/index.html) ｜ 解答：[question/answer/03_selectors/index.html](question/answer/03_selectors/index.html)

<details>
<summary>問題の内容を開く</summary>

3節の基本のセレクタと、この節のクラスセレクタだけで解けます。`03_selectors/index.html`のHTMLは完成しています。`<style>`の中はプロパティと値だけが書いてあり、セレクタが`TODO`になっています。`(1)`〜`(6)`のルールに、次の「対象」だけに当たるセレクタを書きます。IDセレクタ（`#...`）と`style`属性は使わず、HTMLも変更しません（クラスの追加もしない）。

| # | 対象 | 確認したいこと |
|---|---|---|
| 1 | すべての`p` | すべての段落の行の間隔が広くなる |
| 2 | `h1`と`h2`の両方（1つのルールでまとめて） | `h1`と`h2`が青くなる（`h3`は黒のまま） |
| 3 | `class="memo"`を持つ要素 | 2つのメモが、それぞれ角の丸い枠で囲まれる |
| 4 | `class="date"`を持つ要素 | 日付の2行だけが灰色・小さい文字になる |
| 5 | `.links`の**中にある**`a`だけ（最後の段落のMDNへのリンクは含まない） | 「メモ一覧」「メモを追加」「設定」の3つが、下線の無い丸いボタンの形になる。MDNへのリンクは普通のリンクのまま |
| 6 | `.links`の中の`a`に、マウスが乗っているとき | ボタンにマウスを乗せると、青背景・白文字になる |

確認は表の右の列のとおりです。あわせて、開発者ツールで要素を選び、Stylesパネルで意図したルールだけが当たっていることを確かめます。

</details>
---

## 5. 背景・装飾

> [example/05_decoration/index.html](example/05_decoration/index.html)

背景色・枠線・角丸・影など、要素の見た目を整える書き方です。

```css
body {
    background: #f4f6f9;
}

.card {
    border-radius: 8px;
    box-shadow: 0 1px 3px rgb(0 0 0 / 0.1);   /* 横のずれ 縦のずれ ぼかし 色 */
}

.tag {
    border-radius: 999px;   /* ピル型 */
}
```

| プロパティ | 説明 |
|---|---|
| `background` | 背景色・`linear-gradient()`でグラデーション |
| `linear-gradient(角度, 色1, 色2)` | 色が変わっていく背景。角度は`180deg`（上→下。省略時）・`90deg`（左→右）・`135deg`（左上→右下）。例：`linear-gradient(135deg, #3f6fd1, #7a5af8)` |
| `border` | 枠線。`太さ 線の種類 色`の順に書く（`1px solid #e1e5eb`）。種類は`solid`（実線）・`dashed`（破線）・`dotted`（点線）。`none`で枠線なし |
| `border-top`・`border-right`・`border-bottom`・`border-left` | 指定した**1辺だけ**に枠線を付ける。書き方は`border`と同じ（`border-left: 4px solid #3f6fd1`） |
| `border-radius` | 角丸。`999px`でピル型、`50%`で（正方形なら）正円 |
| `box-shadow` | 影。`横 縦 ぼかし 色`の順（`0 4px 12px rgb(0 0 0 / 0.1)`）。ぼかしの後ろに「広がり」の長さを足して`0 0 0 3px 色`とすると、ぼかし無しで外側に太さ3pxの輪が付く |
| `outline` | フォーカス時などに外側に出る線。`border`と違って場所を取らない。`outline: none`で消せる（消すときは代わりのフォーカス表示を必ず付ける） |
| `opacity` | 透明度。`1`（不透明）〜`0`（透明）。要素全体が薄くなる |
| `cursor` | マウスカーソルの形。`pointer`（指の形）はクリックできる要素で使う |

### 動作確認

| 確認する操作 | 確認したいこと |
|---|---|
| `05_decoration/index.html`を開く | 背景色・グラデーション・角丸・影のそれぞれの見え方がわかる |
| 開発者ツールで`.s-medium`の`box-shadow`の値を書き換える | 影の大きさ・濃さがその場で変わる |


### 練習問題4：記事ページを読みやすく装飾する

> 問題：[question/04_article_style/index.html](question/04_article_style/index.html) ｜ 解答：[question/answer/04_article_style/index.html](question/answer/04_article_style/index.html)

<details>
<summary>問題の内容を開く</summary>

`04_article_style/index.html`のHTMLは完成しています。`<style>`の`TODO 1`〜`TODO 12`を埋めて、次の完成イメージにします。

```
┌─────────────────────────────────────────────┐
│ ▓▓▓ 青→紫のグラデーションの帯 ▓▓▓▓▓▓▓▓▓▓▓▓▓ │  ← .hero（白い文字・中央揃え）
│      CSSで読みやすい文章を作る               │
│      2026年10月3日（字間を広めに）            │
└─────────────────────────────────────────────┘
  ┌───────────────────────────────────────┐
  │ 白いカード（角丸・薄い影）               │  ← .article
  │ (#HTML) (#CSS)  ← ピル型のタグ           │
  │ 本文（行間が広く読みやすい）              │
  │ ┃ ポイント：…  ← 左に青い線・薄い青背景    │  ← .point
  │ 関連記事：とても長いタイトルが1行で…       │  ← .related（はみ出しを「…」で省略）
  └───────────────────────────────────────┘
```

| # | 書く場所 | やること |
|---|---|---|
| 1 | `body` | フォントスタック。`"Hiragino Sans"`・`"Noto Sans JP"`・`"Yu Gothic"`の順に並べ、最後はゴシック体の総称ファミリー |
| 2 | `body` | 文字サイズは`1rem`、行の高さは文字サイズの1.8倍（単位なしの数値で） |
| 3 | `.hero` | 背景を、左上から右下（`135deg`）へ`#3f6fd1`→`#7a5af8`のグラデーションにする |
| 4 | `.hero` | 文字は白・中央揃え |
| 5 | `.hero h1` | 文字サイズ`2rem`・太さ`700`・行の高さ`1.3`（見出しは本文より詰める） |
| 6 | `.hero time` | 字間を`0.15em`空ける |
| 7 | `.article` | 角丸12px |
| 8 | `.article` | 影（横0・縦4px・ぼかし12px・黒の10%の半透明） |
| 9 | `.tag` | 両端が丸い「ピル型」にする |
| 10 | `.point` | 左側だけに4pxの青（`#3f6fd1`）の実線、背景は薄い青（`#eef3ff`） |
| 11 | `.article a` | 下線を「点線」にする（`text-decoration`に線の種類も書ける） |
| 12 | `.related` | 1行に収まらない部分を「…」で省略する（3点セット） |

| 確認する操作 | 確認したいこと |
|---|---|
| ブラウザで開く | 完成イメージのとおりに表示される |
| ウィンドウの幅を狭くする | 「関連記事」の行は折り返さず、末尾が「…」になる |

</details>
---

---

## 補足：カスケード・詳細度・継承

> [example/06_cascade/index.html](example/06_cascade/index.html)

この補足は、CSSを書いていて「書いたのに効かない」ときに読む内容です。最初は読み飛ばして、この章の最後まで進めてから戻っても構いません。

1つの要素に複数のルールが当たって値がぶつかったとき、**どれが勝つか**を決める仕組みが「カスケード（滝のように上から順に流れ落ちて決まる）」です。CSSで「書いたのに効かない」原因のほとんどはここにあります。

### 勝敗の決まり方（上から順に比べる）

| 順番 | 比べるもの | 説明 |
|---|---|---|
| 1 | `!important` | 付いている方が勝つ。**原則使わない**（後から上書きできなくなる） |
| 2 | `style`属性 | インラインスタイルはどのセレクタより強い |
| 3 | **詳細度** | セレクタの「具体的さ」。高い方が勝つ |
| 4 | 記述順 | 詳細度が同じなら**後に書いた方**が勝つ |

### 詳細度の数え方

`(IDの数, クラス・属性・疑似クラスの数, 要素・疑似要素の数)`の3桁で数え、**左の桁から**比べます。基本のセレクタだけなら、`(IDの数, クラスと:hoverの数, 要素の数)`と覚えれば十分です。

| セレクタ | 詳細度 |
|---|---|
| `p` | (0, 0, 1) |
| `.text` | (0, 1, 0) |
| `:hover`（疑似クラス） | (0, 1, 0) |
| `div p.text` | (0, 1, 2) |
| `.specificity .text` | (0, 2, 0) |
| `#special` | (1, 0, 0) |

`(0, 1, 2)`と`(0, 2, 0)`では、2桁目で決着するので`(0, 2, 0)`の勝ちです。要素セレクタをいくつ足しても、クラス1個の差は覆りません。

```css
.order { color: red; }
.order { color: blue; }          /* 同じ詳細度 → 後に書いた方（青）が勝つ */

.specificity p.text { color: green; }   /* (0,2,1) */
.specificity .text  { color: orange; }  /* (0,2,0) → 負ける */
```

### 継承

一部のプロパティは、親に指定した値が子に**引き継がれます**。

| 継承される | 継承されない |
|---|---|
| `color`・`font-*`・`line-height`・`text-align`・`letter-spacing`など文字に関するもの | `margin`・`padding`・`border`・`background`・`width`・`display`など箱に関するもの |

継承は「その要素に直接当たるルールが1つもないとき」だけ使われます。**どんなに詳細度の低いルールでも、直接当たっていれば継承より優先**されます。

### 実務でのコツ

- セレクタは**クラス1〜2個**程度に抑え、詳細度を低く揃える（上書きしやすくなる）
- IDセレクタ・`!important`・`style`属性はCSSの設計では使わない
- 「効かない」ときは開発者ツールのStylesで**取り消し線**が付いたルールを探し、何に負けているかを確認する

### 動作確認：勝ったルール・負けたルール

| 確認する操作 | 確認したいこと |
|---|---|
| `06_cascade/index.html`を開く | 各段落の色が説明どおり（青・灰・緑・紫・茶…）になっている |
| 開発者ツールで「→ 緑」の段落を選び、Stylesパネルを見る | `.specificity .text`の`color: orange`と`p`の`color: gray`に取り消し線が付いている |
| 「3. 継承」の`span`を選ぶ | Stylesに「Inherited from section.inherit」と表示され、親の`color`を継承している |
| `.inherit`の中の最初の`p`を選ぶ | 親の青ではなく灰色（直接当たる`p { color: gray }`が継承より優先） |


### 練習問題5：何色になるか予想する（詳細度クイズ）

> 問題：[question/05_specificity_quiz/index.html](question/05_specificity_quiz/index.html) ｜ 解答：[question/answer/05_specificity_quiz/index.html](question/answer/05_specificity_quiz/index.html)

<details>
<summary>問題の内容を開く</summary>

`05_specificity_quiz/index.html`の`<style>`には、9つのルールが書いてあります。HTMLの段落Q1〜Q6の文字色を、ブラウザで**開く前に**予想し、各段落の直前のコメント「予想：」の後ろに書き込みます。

| 確認する操作 | 確認したいこと |
|---|---|
| 予想を書き終えてからブラウザで開く | 予想と実際の色を比べる |
| 外れた段落を開発者ツールで選び、Stylesパネルを見る | どのルールが勝って、どのルールに取り消し線が付いているかがわかる |

使っているのは、3節・4節の基本のセレクタ（要素・クラス・子孫・ID）だけです。

ヒント：詳細度は`(IDの数, クラスの数, 要素の数)`。左の桁から比べ、同じ詳細度のときだけ後に書いた方が勝ちます。

</details>

---

## 次のステップ

続きは [04_css_layout](../04_css_layout/) です。ボックスモデルとdisplayを土台に、Flexbox・Gridでのレイアウトとレスポンシブ対応を学び、オリジナルHPに見た目を付けます。
