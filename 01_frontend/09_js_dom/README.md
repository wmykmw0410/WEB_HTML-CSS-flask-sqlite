# 09 DOM操作

> フロントエンド編 ／ 前の章：[08_js_forms](../08_js_forms/) ／ 次の章：[10_js_render](../10_js_render/)

[06_js_dom_basics](../06_js_dom_basics/)では、`getElementById`・`querySelector`などで要素を取得し、`textContent`で書き換える「DOMの最小限」を学び、[07_js_events](../07_js_events/)・[08_js_forms](../08_js_forms/)では、それをクリックや入力・送信などの**イベント**で動かしました。この章では、その土台になっている**DOM**を整理して、属性の読み書き・要素の作成と削除・親要素でまとめてイベントを受け取る方法（イベント委譲）・ユーザーの入力を安全に表示する方法を学びます。

この先の[10_js_render](../10_js_render/)では、ここで学ぶ要素の作成を使って、配列のデータから一覧の画面を作ります。

## 前提

| チャプター | 使う知識 |
|---|---|
| 02_html_semantic_form | フォーム部品 |
| 03_css_basics | `class`・`id`属性 |
| 05_js_basics | 変数・関数・`forEach`・コールバック関数 |
| 06_js_dom_basics | `getElementById`・`querySelector`・`querySelectorAll`・`textContent`・`Number()` |
| 07_js_events・08_js_forms | `addEventListener`・`classList.toggle`・`event.type`・`preventDefault()` |

## 目次

1. [DOM操作](#1-dom操作)

---

## フォルダ構成

```
01_frontend/09_js_dom/
├── README.md
├── example/                      サンプル（1つのサンプル＝1つのフォルダ）
│   └── 01_dom/                   DOM操作（属性・要素の作成・イベント委譲・XSS）
│       ├── index.html
│       └── script.js
└── question/                     練習問題（7問。問題文はREADMEの各テーマの後ろ）
    ├── 01_attributes/            練習問題1：属性を読み書きする
    ├── 02_create_element/        練習問題2：要素を1つ作って追加する
    ├── 03_build_list/            練習問題3：配列から一覧を作る
    ├── 04_remove/                練習問題4：要素を消す
    ├── 05_delegation/            練習問題5：親要素でまとめてイベントを受け取る
    ├── 06_safe_text/             練習問題6：textContentとinnerHTML
    ├── 07_toolbox/               練習問題7：道具箱（classList・disabled・hidden・focus）
    └── answer/                   解答（問題と同じ名前のフォルダ）
        ├── 01_attributes/
        ├── 02_create_element/
        ├── 03_build_list/
        ├── 04_remove/
        ├── 05_delegation/
        ├── 06_safe_text/
        └── 07_toolbox/
```

---

## 1. DOM操作

> [example/01_dom/index.html](example/01_dom/index.html) / [example/01_dom/script.js](example/01_dom/script.js)

この章の練習問題は、**1問に1つのこと**だけを書く小さな問題に分けています。各テーマの説明の直後にあります。

| テーマ | 練習問題 |
|---|---|
| 属性の読み書き | 練習問題1 |
| 要素を作って追加する・消す | 練習問題2〜4 |
| 親要素でまとめてイベントを受け取る | 練習問題5 |
| `textContent`と`innerHTML` | 練習問題6 |
| 道具箱 | 練習問題7 |

ブラウザは読み込んだHTMLを、JavaScriptから操作できる**DOM**（Document Object Model：要素の木構造）に変換して保持しています。JavaScriptでDOMを書き換えると、画面にすぐ反映されます。06章で使った`getElementById`も`textContent`も、このDOMの操作でした。

### DOM操作は「取得」と「書き換え」の2ステップ（おさらい）

```
<body>                               ① 取得：document.getElementById('count')
 ├─ <textarea id="body">                     → 書き換えたい要素（のオブジェクト）が手に入る
 └─ <p>
     └─ <span id="count">0</span>    ② 書き換え：counter.textContent = 10
                                              → 画面の表示がすぐ変わる
```

どの操作も「**要素を取得する → その要素のプロパティやメソッドを使って書き換える**」の形です。06〜08章で使った書き方は、この2ステップのうち、`getElementById`・`querySelector`など（取得）と`textContent`・`classList.toggle`（書き換え）です。この章では、**書き換えの方法**（属性・要素の作成と削除）をさらに増やします。


### 要素の取得のおさらい

要素の取得（`getElementById`・`querySelector`・`querySelectorAll`・`getElementsBy…`）は、[06_js_dom_basicsの2節](../06_js_dom_basics/#2-要素を取得する方法)で学びました。この章では、次のように使い分けます。

| 取得したいもの | 書き方 |
|---|---|
| `id`の付いた1つの要素 | `document.getElementById('id')` |
| それ以外の1つの要素 | `document.querySelector('セレクタ')`（見つからないときは`null`） |
| 複数の要素 | `document.querySelectorAll('セレクタ')`（`forEach`で1つずつ処理できる） |

### 属性の読み書き

```javascript
link.getAttribute('href');                      // 属性の値を読む
link.setAttribute('target', '_blank');          // 属性を追加・変更する
link.dataset.lang;                              // data-lang="..." の値（data-* 属性専用）
```

`data-*`属性は、名前のハイフンが**キャメルケース**に変わって`dataset`のプロパティになります。

| HTML | JavaScript |
|---|---|
| `data-lang="ja"` | `el.dataset.lang` |
| `data-tags="HTML CSS"` | `el.dataset.tags` |
| `data-theme-color="blue"` | `el.dataset.themeColor`（`-c`が`C`に変わる） |

`dataset`で読んだ値は、数字に見えても**文字列**です。

### 練習問題1：属性を読み書きする

> 問題：[question/01_attributes/index.html](question/01_attributes/index.html)・[question/01_attributes/script.js](question/01_attributes/script.js) ｜ 解答：[question/answer/01_attributes/index.html](question/answer/01_attributes/index.html)・[question/answer/01_attributes/script.js](question/answer/01_attributes/script.js)

<details>
<summary>問題の内容を開く</summary>

`01_attributes/script.js`の`TODO 1`〜`TODO 3`に書きます。`01_attributes/index.html`をブラウザで開き、ページ下の「テストを実行」ボタンを押すと、イベントが自動で起こされ、Consoleに ✅（正しい）／❌（間違い）が表示されます。自分でも画面を操作して、動きを確かめます。**1問ずつ**書いて確かめ、その問題が ✅ になってから、次に進みます（まだ書いていない問題が ❌ になるのは正常です）。

| # | やること |
|---|---|
| 1 | `a.doc-link`を`querySelector`で取得し、新しいタブで開くようにする（`target="_blank"`と`rel="noopener noreferrer"`を付ける） |
| 2 | `a.doc-link`の`href`属性の値を読み、`#href-output`に表示する |
| 3 | `a.doc-link`の`data-lang`の値を読み、`#lang-output`に「言語：ja」と表示する |

| # | ヒント |
|---|---|
| 1 | `document.querySelector()` / `要素.setAttribute('属性名', '値')` |
| 2 | `要素.getAttribute('href')` |
| 3 | `要素.dataset.lang` |

</details>

### 要素を作って追加する

```javascript
const li = document.createElement('li');   // 1. 要素を作る（まだ画面には無い）
li.className = 'card';                     // 2. class を設定する
li.textContent = memo.title;               //    中身を設定する
list.append(li);                           // 3. 画面上の要素に追加して、初めて表示される

li.remove();                               // 要素を消す
list.textContent = '';                     // 子要素をすべて消す
```

### 練習問題2：要素を1つ作って追加する

> 問題：[question/02_create_element/index.html](question/02_create_element/index.html)・[question/02_create_element/script.js](question/02_create_element/script.js) ｜ 解答：[question/answer/02_create_element/index.html](question/answer/02_create_element/index.html)・[question/answer/02_create_element/script.js](question/answer/02_create_element/script.js)

<details>
<summary>問題の内容を開く</summary>

`02_create_element/script.js`の`TODO 1`・`TODO 2`に書きます。HTMLには、空の`<ul id="memo-list">`だけがあります。`02_create_element/index.html`をブラウザで開き、ページ下の「テストを実行」ボタンを押すと、イベントが自動で起こされ、Consoleに ✅（正しい）／❌（間違い）が表示されます。自分でも画面を操作して、動きを確かめます。**1問ずつ**書いて確かめ、その問題が ✅ になってから、次に進みます（まだ書いていない問題が ❌ になるのは正常です）。

| # | やること |
|---|---|
| 1 | `li`要素を作り、文字を「買い物リスト」にして、`list`に追加する |
| 2 | もう1つ`li`要素を作り、文字を「企画会議メモ」、`class`を`done`にして、`list`に追加する |

| # | ヒント |
|---|---|
| 1・2 | `document.createElement('li')`で作り、`要素.textContent`で文字を設定し、`list.append(要素)`で追加して、初めて画面に表示される |
| 2 | `class`は`要素.className = 'done'` |

</details>

### 練習問題3：配列から一覧を作る

> 問題：[question/03_build_list/index.html](question/03_build_list/index.html)・[question/03_build_list/script.js](question/03_build_list/script.js) ｜ 解答：[question/answer/03_build_list/index.html](question/answer/03_build_list/index.html)・[question/answer/03_build_list/script.js](question/answer/03_build_list/script.js)

<details>
<summary>問題の内容を開く</summary>

`03_build_list/script.js`の`TODO 1`に書きます。`03_build_list/index.html`をブラウザで開き、ページ下の「テストを実行」ボタンを押すと、イベントが自動で起こされ、Consoleに ✅（正しい）／❌（間違い）が表示されます。自分でも画面を操作して、動きを確かめます。**1問ずつ**書いて確かめ、その問題が ✅ になってから、次に進みます（まだ書いていない問題が ❌ になるのは正常です）。

| # | やること |
|---|---|
| 1 | `memos`（3件）を、`#memo-list`の中に`li`として追加する。各`li`は、`<span class="tag">カテゴリ</span>`のあとにタイトルが続く形にする |

| # | ヒント |
|---|---|
| 1 | `memos.forEach((memo) => { ... })`の中で、`li`と`span`を`createElement`で作る。`li.append(tag, memo.title)`のように、複数まとめて追加できる |

</details>

### 練習問題4：要素を消す

> 問題：[question/04_remove/index.html](question/04_remove/index.html)・[question/04_remove/script.js](question/04_remove/script.js) ｜ 解答：[question/answer/04_remove/index.html](question/answer/04_remove/index.html)・[question/answer/04_remove/script.js](question/answer/04_remove/script.js)

<details>
<summary>問題の内容を開く</summary>

`04_remove/script.js`の`TODO 1`・`TODO 2`に書きます。`04_remove/index.html`をブラウザで開き、ページ下の「テストを実行」ボタンを押すと、イベントが自動で起こされ、Consoleに ✅（正しい）／❌（間違い）が表示されます。自分でも画面を操作して、動きを確かめます。**1問ずつ**書いて確かめ、その問題が ✅ になってから、次に進みます（まだ書いていない問題が ❌ になるのは正常です）。

| # | やること |
|---|---|
| 1 | `#memo-list`の中の、`class`が`old`の`li`を消す |
| 2 | `#temp-list`の中身（子要素）をすべて消す |

| # | ヒント |
|---|---|
| 1 | 消したい要素を`querySelector`で取得して、`要素.remove()` |
| 2 | `要素.textContent = ''`を代入すると、子要素もすべて消える |

</details>

### 親要素でまとめてイベントを受け取る（イベント委譲）

作った要素1つずつに`addEventListener`すると、一覧を作り直すたびに登録し直すことになります。イベントは**子要素から親要素へ伝わる**ので、親要素に1回だけ登録しておき、`event.target`で「どの要素で起きたか」を調べる書き方がよく使われます。

```javascript
const li = document.createElement('li');
li.dataset.category = memo.category;            // data-category 属性を付けておく

list.addEventListener('click', (event) => {       // 親の ul に1回だけ登録する
    const item = event.target.closest('li');      // クリックされた要素から、最も近い li を探す
    if (!item) {
        return;                                   // li の外（余白）がクリックされたときは何もしない
    }
    console.log(item.dataset.category);
});
```

| 書き方 | 説明 |
|---|---|
| `event.target` | イベントが**実際に起きた要素**。`li`の中のバッジ`<span>`をクリックしたときは、`li`ではなく`span`になる |
| `要素.closest('セレクタ')` | 自分または祖先から、セレクタに合う最も近い要素を探す。どこをクリックしても、`li`が手に入る。見つからないときは`null` |

`event.target`が子の`span`になることがあるため、`event.target`をそのまま使わず、`closest()`で「欲しい要素」を探し直します。

### 練習問題5：親要素でまとめてイベントを受け取る

> 問題：[question/05_delegation/index.html](question/05_delegation/index.html)・[question/05_delegation/script.js](question/05_delegation/script.js) ｜ 解答：[question/answer/05_delegation/index.html](question/answer/05_delegation/index.html)・[question/answer/05_delegation/script.js](question/answer/05_delegation/script.js)

<details>
<summary>問題の内容を開く</summary>

`05_delegation/script.js`の`TODO 1`に書きます。`05_delegation/index.html`をブラウザで開き、ページ下の「テストを実行」ボタンを押すと、イベントが自動で起こされ、Consoleに ✅（正しい）／❌（間違い）が表示されます。自分でも画面を操作して、動きを確かめます。**1問ずつ**書いて確かめ、その問題が ✅ になってから、次に進みます（まだ書いていない問題が ❌ になるのは正常です）。

| # | 仕様 |
|---|---|
| 1 | `li`1つずつではなく、親の`list`に`click`イベントを**1回だけ**登録する |
| 2 | クリックされた要素から、最も近い`li`を探し、その`li`の`data-category`の値を使って、`clickOutput`に「家事のメモがクリックされました」のように表示する |
| 3 | `li`の外（`list`の余白）がクリックされたときは、何もしない |

| # | ヒント |
|---|---|
| 2 | `event.target.closest('li')`。`li`の中のバッジ（`span`）をクリックしても、`li`が手に入る。`li`の`data-category`は`item.dataset.category` |
| 3 | `closest`が`null`を返したら、`return`で終わる |

</details>

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


### 練習問題6：textContentとinnerHTML

> 問題：[question/06_safe_text/index.html](question/06_safe_text/index.html)・[question/06_safe_text/script.js](question/06_safe_text/script.js) ｜ 解答：[question/answer/06_safe_text/index.html](question/answer/06_safe_text/index.html)・[question/answer/06_safe_text/script.js](question/answer/06_safe_text/script.js)

<details>
<summary>問題の内容を開く</summary>

`06_safe_text/script.js`の`TODO 1`・`TODO 2`に書きます。`06_safe_text/index.html`をブラウザで開き、ページ下の「テストを実行」ボタンを押すと、イベントが自動で起こされ、Consoleに ✅（正しい）／❌（間違い）が表示されます。自分でも画面を操作して、動きを確かめます。**1問ずつ**書いて確かめ、その問題が ✅ になってから、次に進みます（まだ書いていない問題が ❌ になるのは正常です）。

| # | やること |
|---|---|
| 1 | `userInput`（タグを含む文字列）を`#user-output`に表示する。HTMLとして解釈されない、安全な方法を使う |
| 2 | 自分で書いた固定のHTML「`<b>太字</b>の文字`」を、HTMLとして解釈して`#trusted-output`に表示する（太字になる） |

| # | ヒント |
|---|---|
| 1 | `textContent`（`innerHTML`は使わない） |
| 2 | `innerHTML`。ユーザーの入力や、サーバーから受け取ったデータには使わない |

1のコードを`innerHTML`に変えると、アラートが出ます（XSS）。確認したら、`textContent`に戻します。

</details>

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


### 練習問題7：道具箱：classList・disabled・hidden・focus

> 問題：[question/07_toolbox/index.html](question/07_toolbox/index.html)・[question/07_toolbox/script.js](question/07_toolbox/script.js) ｜ 解答：[question/answer/07_toolbox/index.html](question/answer/07_toolbox/index.html)・[question/answer/07_toolbox/script.js](question/answer/07_toolbox/script.js)

<details>
<summary>問題の内容を開く</summary>

`07_toolbox/script.js`の`TODO 1`〜`TODO 5`に書きます（道具箱の表を見て書きます）。`07_toolbox/index.html`をブラウザで開き、ページ下の「テストを実行」ボタンを押すと、イベントが自動で起こされ、Consoleに ✅（正しい）／❌（間違い）が表示されます。自分でも画面を操作して、動きを確かめます。**1問ずつ**書いて確かめ、その問題が ✅ になってから、次に進みます（まだ書いていない問題が ❌ になるのは正常です）。

| # | やること |
|---|---|
| 1 | `sendButton`を押せなくする |
| 2 | `notice`を隠す |
| 3 | `box`に`active`クラスを付け、`old`クラスを外す |
| 4 | `box`に`active`クラスが付いているかを調べ、`stateOutput`に「active：true」のように表示する |
| 5 | `nameInput`にフォーカス（キーボード操作の対象）を移す |

| # | ヒント |
|---|---|
| 1 | `要素.disabled = true` |
| 2 | `要素.hidden = true` |
| 3 | `要素.classList.add('クラス名')` / `要素.classList.remove('クラス名')`（`toggle`と違い、条件に関係なく） |
| 4 | `要素.classList.contains('クラス名')`は、`true` / `false`を返す |
| 5 | `要素.focus()` |

</details>

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
| 「1. 属性の読み書き」を見る | `href=...`・`data-lang=ja`・`target=_blank（JavaScriptで追加）`と表示される。MDNのリンクをクリックすると新しいタブで開く |
| 「2. 要素を作って追加する」を見る | HTMLには空の`<ul>`しか書いていないのに、カテゴリのバッジ付きでメモが3件表示される。ElementsパネルでJavaScriptが作った`<li>`を確認できる |
| 「3. 親要素でまとめてイベントを受け取る」で、2.の一覧のメモをクリックする | 「家事のメモがクリックされました（event.type = click）」のように表示される。カテゴリのバッジの部分をクリックしても同じ表示になる（`closest('li')`で`li`が手に入る） |
| 「4. textContent と innerHTML の違い」を見る | textContentの欄には`<img ...>`という文字列がそのまま表示される |
| `01_dom/script.js`の`innerHTML`の行のコメントを外してリロードする（確認後は戻す） | 「乗っ取り」というアラートが出る（入力した文字列の中のスクリプトが実行された） |

---

## 次のステップ

続きは [10_js_render](../10_js_render/) です。配列のデータから、DOM操作で一覧の画面を作ります。配列メソッド（`map`・`filter`・`find`・`includes`）も、そこで学びます。
