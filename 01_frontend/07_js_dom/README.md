# 07 DOM操作

> フロントエンド編 ／ 前の章：[06_js_events](../06_js_events/) ／ 次の章：[08_js_render](../08_js_render/)

[06_js_events](../06_js_events/)では、`getElementById`で要素を取得し、`textContent`で書き換えて、ブラウザ上の動きを作りました。この章では、その土台になっている**DOM**を整理して、`querySelector`・属性の読み書き・要素の作成と削除・ユーザーの入力を安全に表示する方法を学びます。

この先の[08_js_render](../08_js_render/)では、ここで学ぶ要素の作成を使って、配列のデータから一覧の画面を作ります。

## 前提

| チャプター | 使う知識 |
|---|---|
| 02_html_semantic_form | `id`・`class`・`data-*`属性 |
| 05_js_basics | 変数・関数・`forEach`・コールバック関数 |
| 06_js_events | `getElementById`・`addEventListener`・`textContent`・`classList.toggle` |

## 目次

1. [DOM操作](#1-dom操作)

---

## フォルダ構成

```
01_frontend/07_js_dom/
├── README.md
├── example/                      サンプル（1つのサンプル＝1つのフォルダ）
│   └── 01_dom/                   DOM操作（querySelector・属性・要素の作成・XSS）
│       ├── index.html
│       └── script.js
└── question/                     練習問題（1問。問題文はREADMEの各節の最後）
    ├── 01_build_list/            練習問題1：JavaScriptで要素を作って書き換える
    │   ├── index.html
    │   └── script.js
    └── answer/                   解答（問題と同じ名前のフォルダ。中のファイル構成も問題と同じ）
        └── 01_build_list/
```

---

## 1. DOM操作

> [example/01_dom/index.html](example/01_dom/index.html) / [example/01_dom/script.js](example/01_dom/script.js)

ブラウザは読み込んだHTMLを、JavaScriptから操作できる**DOM**（Document Object Model：要素の木構造）に変換して保持しています。JavaScriptでDOMを書き換えると、画面にすぐ反映されます。06章で使った`getElementById`も`textContent`も、このDOMの操作でした。

### DOM操作は「取得」と「書き換え」の2ステップ（おさらい）

```
<body>                               ① 取得：document.getElementById('count')
 ├─ <textarea id="body">                     → 書き換えたい要素（のオブジェクト）が手に入る
 └─ <p>
     └─ <span id="count">0</span>    ② 書き換え：counter.textContent = 10
                                              → 画面の表示がすぐ変わる
```

どの操作も「**要素を取得する → その要素のプロパティやメソッドを使って書き換える**」の形です。06章で使った書き方は、この2ステップのうち、`getElementById`（取得）と`textContent`・`classList.toggle`（書き換え）です。この章では、取得と書き換えの方法をさらに増やします。


### `querySelector`：CSSのセレクタで要素を取得する

```javascript
document.querySelector('a.doc-link');                 // クラス
document.querySelector('#count');                     // ID
document.querySelector('meta[name="csrf-token"]');    // 属性セレクタ
document.querySelectorAll('.card');                   // 一致するものすべて
```

| メソッド | 取得するもの | 見つからないとき |
|---|---|---|
| `getElementById('id')` | `id`が一致する要素1つ | `null` |
| `querySelector('セレクタ')` | 一致する**最初の**要素1つ | `null` |
| `querySelectorAll('セレクタ')` | 一致する要素**すべて**（`NodeList`） | 空の`NodeList`（`length`が`0`） |

`01_frontend/03_css_basics`で学んだセレクタがそのまま使えます。

### 属性の読み書き

```javascript
link.getAttribute('href');                      // 属性の値を読む
link.setAttribute('target', '_blank');          // 属性を追加・変更する
link.dataset.lang;                              // data-lang="..." の値（data-* 属性専用）
button.setAttribute('aria-expanded', 'true');   // 制作課題のハンバーガーメニューで使う
```

`data-*`属性は、名前のハイフンが**キャメルケース**に変わって`dataset`のプロパティになります。

| HTML | JavaScript |
|---|---|
| `data-lang="ja"` | `el.dataset.lang` |
| `data-tags="HTML CSS"` | `el.dataset.tags` |
| `data-theme-color="blue"` | `el.dataset.themeColor`（`-c`が`C`に変わる） |

`dataset`で読んだ値は、数字に見えても**文字列**です。

### 要素を作って追加する

```javascript
const li = document.createElement('li');   // 1. 要素を作る（まだ画面には無い）
li.className = 'card';                     // 2. class を設定する
li.textContent = memo.title;               //    中身を設定する
list.append(li);                           // 3. 画面上の要素に追加して、初めて表示される

li.remove();                               // 要素を消す
list.textContent = '';                     // 子要素をすべて消す
```

### `textContent`と`innerHTML`の違い（XSSに注意）

| プロパティ | 文字列の扱い | 安全性 |
|---|---|---|
| `textContent` | **ただの文字**として表示する | 安全 |
| `innerHTML` | **HTMLとして解釈**して表示する | ユーザーの入力を入れると危険 |

```javascript
const userInput = `<img src=x onerror="alert('乗っ取り')">`;
el.textContent = userInput;   // 文字列がそのまま表示される
el.innerHTML = userInput;     // <img> として解釈され、onerror のスクリプトが実行される
```

ユーザーが入力した文字列を`innerHTML`に入れると、悪意のあるタグやスクリプトがページ内で実行されてしまいます。これを**XSS（クロスサイトスクリプティング）**と呼びます。**ユーザーの入力やサーバーから受け取ったデータを表示するときは`textContent`を使う**のが原則です。`02_backend/06_jinja2`では、Jinja2が`{{ }}`の中身を自動でエスケープ（`<`などの記号を、タグとして働かない形に変換）して、同じ攻撃を防いでいることを学びます。


### 道具箱：必要になったときに見る

練習問題や制作課題で必要になったとき、ここに戻って確かめます。最初にすべて覚える必要はありません。

| 要素・メソッド | 説明 |
|---|---|
| `要素.classList.add('クラス名')` / `remove('クラス名')` | クラスを付ける / 外す（条件に関係なく） |
| `要素.classList.contains('クラス名')` | その要素にクラスが付いているか（`true`/`false`） |
| `要素.hidden = true` / `false` | 要素を隠す / 表示する（HTMLの`hidden`属性と同じ。見た目は`display: none`になる） |
| `要素.style.プロパティ名 = '値'` | CSSを直接書き込む（`el.style.width = '50%'`）。`background-color`のようにハイフンのあるプロパティは`backgroundColor`とキャメルケースで書く。色や幅など、JavaScriptで計算した値を入れたいときに使い、ふだんの見た目はクラスの付け外しで切り替える |
| `要素.disabled = true` / `false` | ボタンや入力欄を押せなく / 押せるようにする（HTMLの`disabled`属性と同じ） |
| `要素.focus()` | その要素にフォーカス（キーボード操作の対象）を移す |


### よくあるエラー

| 画面・Consoleの様子 | 原因 |
|---|---|
| `Cannot read properties of null (reading 'addEventListener')` | `getElementById`の`id`の綴りが違う／HTMLに`id`が無い／`<script>`が`</body>`より前にある（[05_js_basicsの0節](../05_js_basics/#0-javascriptの読み込み方とデバッグ)） |
| 表示が`undefined`になる | `lenght`のようにプロパティ名を打ち間違えている |
| 文字を変えたのに画面が変わらない | 取得した要素が別の要素になっている（`id`の重複・取得した変数を間違えている） |


### 実行方法

`example/01_dom/index.html`をブラウザで直接開いてください。

### 動作確認：DOMを操作できているか

| 確認する操作 | 確認したいこと |
|---|---|
| 「1. querySelector と属性の読み書き」を見る | `href=...`・`data-lang=ja`・`target=_blank（JavaScriptで追加）`と表示される。MDNのリンクをクリックすると新しいタブで開く |
| 「2. 要素を作って追加する」を見る | HTMLには空の`<ul>`しか書いていないのに、カテゴリのバッジ付きでメモが3件表示される。ElementsパネルでJavaScriptが作った`<li>`を確認できる |
| 「3. textContent と innerHTML の違い」を見る | textContentの欄には`<img ...>`という文字列がそのまま表示される |
| `01_dom/script.js`の`innerHTML`の行のコメントを外してリロードする（確認後は戻す） | 「乗っ取り」というアラートが出る（入力した文字列の中のスクリプトが実行された） |

### 練習問題1：JavaScriptで要素を作って書き換える

> 問題：[question/01_build_list/index.html](question/01_build_list/index.html)・[question/01_build_list/script.js](question/01_build_list/script.js) ｜ 解答：[question/answer/01_build_list/index.html](question/answer/01_build_list/index.html)・[question/answer/01_build_list/script.js](question/answer/01_build_list/script.js)

<details>
<summary>問題の内容を開く</summary>

`01_build_list/index.html`のHTMLとCSSは完成しています。`01_build_list/script.js`の`TODO 1`〜`TODO 4`を書いて、ページを完成させます。

| # | やること | ヒント |
|---|---|---|
| 1 | `memos`（3件）を、`#memo-list`の中に`li`として追加する。各`li`は、`<span class="tag">カテゴリ</span>`のあとにタイトルが続く形にする | `document.createElement()` / `要素.className` / `要素.textContent` / `要素.append()` |
| 2 | `a.doc-link`を取得し、新しいタブで開くようにする（`target="_blank"`と`rel="noopener noreferrer"`を付ける） | `document.querySelector()` / `要素.setAttribute()` |
| 3 | `a.doc-link`の`data-lang`の値を読み、`#lang-output`に「言語：ja」と表示する | `要素.dataset.lang` |
| 4 | `userInput`（タグを含む文字列）を`#user-output`に表示する。HTMLとして解釈されない、安全な方法を使う | `textContent`（`innerHTML`は使わない） |

| 確認する操作 | 確認したいこと |
|---|---|
| ブラウザで開く | 「1. メモの一覧」にバッジ付きの3件が表示され、「言語：ja」が表示される |
| 「3. ユーザーが入力した文字」を見る | `<img src=x onerror=...>`という文字列がそのまま表示され、アラートは出ない |
| MDNのリンクをクリックする | 新しいタブで開く |
| 4のコードを`innerHTML`に変えてみる（確認後は戻す） | アラートが出る（XSS） |

</details>

---

## 次のステップ

続きは [08_js_render](../08_js_render/) です。配列のデータから、DOM操作で一覧の画面を作ります。配列メソッド（`map`・`filter`・`find`・`includes`）も、そこで学びます。
