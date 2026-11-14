# 06 DOMの最小限：要素を取得して、書き換える

> フロントエンド編 ／ 前の章：[05_js_basics](../05_js_basics/) ／ 次の章：[07_js_events](../07_js_events/)

[05_js_basics](../05_js_basics/)で学んだ文法を使って、**JavaScriptでページの要素を取得し、文字を書き換える**ところだけを、先に試します。この章では、まだ**イベント（クリックや入力）は使いません**。

ブラウザは、読み込んだHTMLを、JavaScriptから操作できる形で持っています。これを**DOM**（Document Object Model）と呼びます。DOMの操作は、次の2ステップでできています。

```
① 取得      動かしたい要素を見つける      document.getElementById('message')
② 書き換え  要素の文字を入れ替える        message.textContent = 'JavaScriptで書き換えました'
```

この章では、①の「取得」の方法（`getElementById`・`getElementsBy…`・`querySelector`）と、②の`textContent`の使い方を、順に厚くしていきます。

| 節 | 学ぶこと | 練習問題 |
|---|---|---|
| 1 | `getElementById`で取得し、`textContent`で書き換える | 練習問題1・2 |
| 2 | 要素を取得する方法：`getElementById`・`getElementsBy…`・`querySelector` | 練習問題3〜5 |
| 3 | `textContent`を使いこなす：読み取り・追記・数値への変換 | 練習問題6〜8 |
| 4 | 動かないときの調べ方 | 練習問題9 |

この章の練習問題は、**1問に1つのこと**だけを書く小さな問題に分けています。画面の状態を調べるテストが付いているので、Consoleの ✅ を目安に進められます。

学習の順番は、次のとおりです。

| 章 | 学ぶこと |
|---|---|
| **06_js_dom_basics（この章）** | DOMの最小限：要素を取得して、`textContent`で書き換える |
| [07_js_events](../07_js_events/) | その書き換えを、クリックや入力に反応して実行する（イベント） |
| [08_js_forms](../08_js_forms/) | フォームの送信を止めて、入力をチェックする |
| [09_js_dom](../09_js_dom/) | 属性の読み書き・要素の作成・`innerHTML`とXSSなど、DOMの応用 |

## 前提

| チャプター | 使う知識 |
|---|---|
| 01_html_basics | `id`属性 |
| 03_css_basics | `class`・`id`・タグのセレクタ（`querySelector`でそのまま使う） |
| 05_js_basics | 変数・テンプレートリテラル・配列の`length`・`for`・`forEach`・デバッグの方法（0節） |

## 目次

1. [取得して、書き換える](#1-取得して書き換える)
2. [要素を取得する方法](#2-要素を取得する方法)
3. [textContentを使いこなす](#3-textcontentを使いこなす)
4. [動かないときの調べ方](#4-動かないときの調べ方)

---

## フォルダ構成

```
01_frontend/06_js_dom_basics/
├── README.md
├── example/                      サンプル（1つのサンプル＝1つのフォルダ）
│   ├── 01_dom_basics/            ページの文字を書き換える（getElementById・textContent）
│   │   ├── index.html
│   │   └── script.js
│   ├── 02_select_elements/       要素を取得する方法（getElementsBy…・querySelector・querySelectorAll）
│   │   ├── index.html
│   │   └── script.js
│   └── 03_text_content/          textContentを使いこなす（読み取り・追記・Number()）
│       ├── index.html
│       └── script.js
└── question/                     練習問題（9問。問題文はREADMEの各節の最後）
    ├── 01_get_and_set/           練習問題1：取得して書き換える
    ├── 02_template/              練習問題2：変数や計算結果を表示する
    ├── 03_query_selector/        練習問題3：querySelectorで1つ取得する
    ├── 04_get_all/               練習問題4：複数の要素を取得して、数える・取り出す
    ├── 05_query_selector_all/    練習問題5：複数の要素をまとめて書き換える
    ├── 06_read_number/           練習問題6：文字を読み取って計算する
    ├── 07_append_clear/          練習問題7：追記する・消す・置き換える
    ├── 08_select_elements/       練習問題8：要素を取得して書き換える（まとめ）
    ├── 09_debug_dom/             練習問題9：書き換わらないページを直す（デバッグ）
    └── answer/                   解答（問題と同じ名前のフォルダ）
        ├── 01_get_and_set/
        ├── 02_template/
        ├── 03_query_selector/
        ├── 04_get_all/
        ├── 05_query_selector_all/
        ├── 06_read_number/
        ├── 07_append_clear/
        ├── 08_select_elements/
        └── 09_debug_dom/
```

各練習問題のフォルダには、`index.html`と`script.js`があります。

---

## 1. 取得して、書き換える

> [example/01_dom_basics/index.html](example/01_dom_basics/index.html) / [example/01_dom_basics/script.js](example/01_dom_basics/script.js)

```html
<p id="message">まだ書き換わっていません</p>
```

```javascript
const message = document.getElementById('message');   // ① HTMLの id="message" の要素を取得する
message.textContent = 'JavaScriptで書き換えました';       // ② 要素の文字を書き換える
```

### ポイント

| 書き方 | 説明 |
|---|---|
| `document.getElementById('id')` | HTMLの`id`が一致する要素を1つ取得する。**`#`は付けず、`id`の名前だけ**を書く |
| `要素.textContent` | 要素の中の文字。代入すると**書き換え**になり、画面にすぐ反映される。代入せずに読むと、現在の文字が取り出せる |
| `` `${price * count}円` `` | [05_js_basics](../05_js_basics/)のテンプレートリテラル。変数や計算結果も、そのまま文字にできる |

この2ステップは、**どの要素でも同じ**です。見出し・段落・ボタンなど、`id`を付けた要素なら、同じ書き方で書き換えられます。

`<script>`は、書き換える要素より**後**（`</body>`の直前）に置きます（[05_js_basicsの0節](../05_js_basics/#0-javascriptの読み込み方とデバッグ)）。

### 動作確認

`example/01_dom_basics/index.html`をブラウザで開いて確認します。

| 確認する操作 | 確認したいこと |
|---|---|
| ページを開く | 「1.」の段落が、HTMLに書いた「まだ書き換わっていません」ではなく、「JavaScriptで書き換えました」になっている。見出しも書き換わっている |
| 「2.」を見る | `300円 × 4個 = 1200円`と表示されている（計算結果を表示できている） |
| Consoleに、「3.」に書いてある1行を貼り付けてEnterを押す | 「3.」の段落が「Consoleから書き換えました」に変わる |
| Consoleを見る | `JavaScriptで書き換えました`と出力されている（`textContent`を読み取った値） |

ここまでの書き換えは、ページを開いたとき（または、Consoleに打ち込んだとき）に**1回だけ**実行されます。この章では、このあと取得と書き換えの方法を増やします。[07_js_events](../07_js_events/)では、書き換えを**「ボタンが押されたとき」に実行する**方法（イベント）を学びます。

### 練習問題1：取得して書き換える

> 問題：[question/01_get_and_set/index.html](question/01_get_and_set/index.html)・[question/01_get_and_set/script.js](question/01_get_and_set/script.js) ｜ 解答：[question/answer/01_get_and_set/index.html](question/answer/01_get_and_set/index.html)・[question/answer/01_get_and_set/script.js](question/answer/01_get_and_set/script.js)

<details>
<summary>問題の内容を開く</summary>

`01_get_and_set/script.js`の`TODO 1`・`TODO 2`に、2ステップ（取得→書き換え）を書きます。`01_get_and_set/index.html`をブラウザで開くと、ページの下のテストが実行され、Consoleに ✅（正しい）／❌（間違い）が表示されます。**1問ずつ**書いてリロードし、その問題が ✅ になるのを確かめてから、次に進みます（まだ書いていない問題が ❌ になるのは正常です）。

| # | やること | 取得する要素の`id` |
|---|---|---|
| 1 | 文字を「はじめてのDOM」にする | `title` |
| 2 | 文字を「JavaScriptで書き換えました」にする | `message` |

| # | ヒント |
|---|---|
| 1・2 | `document.getElementById('id')`で取得し、`textContent`に文字を代入する。`id`に`#`は付けない |

</details>

### 練習問題2：変数や計算結果を表示する

> 問題：[question/02_template/index.html](question/02_template/index.html)・[question/02_template/script.js](question/02_template/script.js) ｜ 解答：[question/answer/02_template/index.html](question/answer/02_template/index.html)・[question/answer/02_template/script.js](question/answer/02_template/script.js)

<details>
<summary>問題の内容を開く</summary>

`02_template/script.js`の`TODO 1`〜`TODO 3`に、変数（`userName`・`price`・`quantity`・`memos`）の値を、画面に表示する処理を書きます。`02_template/index.html`をブラウザで開くと、ページの下のテストが実行され、Consoleに ✅（正しい）／❌（間違い）が表示されます。**1問ずつ**書いてリロードし、その問題が ✅ になるのを確かめてから、次に進みます（まだ書いていない問題が ❌ になるのは正常です）。

| # | やること | 取得する要素の`id` | 表示する文字 |
|---|---|---|---|
| 1 | `userName`の値を埋め込む | `name-output` | `山田さん` |
| 2 | `price`と`quantity`から計算して埋め込む | `total-output` | `1350円` |
| 3 | `memos`の件数を埋め込む | `count-output` | `3件` |

| # | ヒント |
|---|---|
| 1〜3 | `` `${ }` ``の中に、変数や計算を書く（テンプレートリテラル） |
| 3 | 配列の件数は`memos.length`（`()`を付けない） |

</details>

---

## 2. 要素を取得する方法

> [example/02_select_elements/index.html](example/02_select_elements/index.html) / [example/02_select_elements/script.js](example/02_select_elements/script.js)

1節では、`id`で1つの要素を取得する`getElementById`を使いました。ページの要素を取得する方法は、ほかにもあります。

| メソッド | 取得するもの | 戻り値 | 見つからないとき |
|---|---|---|---|
| `getElementById('id')` | `id`が一致する要素**1つ** | 要素 | `null` |
| `querySelector('セレクタ')` | セレクタに一致する**最初の**要素1つ | 要素 | `null` |
| `getElementsByClassName('クラス名')` | クラスが一致する要素**すべて** | `HTMLCollection` | 空（`length`が`0`） |
| `getElementsByTagName('タグ名')` | タグ名が一致する要素**すべて** | `HTMLCollection` | 空（`length`が`0`） |
| `querySelectorAll('セレクタ')` | セレクタに一致する要素**すべて** | `NodeList` | 空（`length`が`0`） |

### 1つの要素を取得する

```javascript
document.getElementById('heading');        // <h2 id="heading"> を取得する（# は付けない）
document.querySelector('#heading');        // 同じ要素。id は # で指定する
document.querySelector('.note');           // クラスは . で指定する
document.querySelector('h1');              // タグ名はそのまま書く
```

`querySelector`の引数は、[03_css_basics](../03_css_basics/)で学んだ**CSSのセレクタ**そのものです。

| セレクタ | 意味 | 例 |
|---|---|---|
| `#heading` | `id`が`heading`の要素 | `<h2 id="heading">` |
| `.note` | クラスが`note`の要素 | `<p class="note">` |
| `h1` | `<h1>`タグの要素 | `<h1>` |
| `.item .name` | `.item`の**中にある**`.name`（子孫セレクタ） | `<li class="item"><span class="name">` |
| `ul > li` | `ul`の**直下の**`li`（子セレクタ） | `<ul><li>` |

`getElementById`では`#`を付けませんが、`querySelector`では必ず付けます（`.`も同じ）。`getElementsByClassName('.name')`のように、`getElementsBy…`に`.`を付けると、何も見つかりません。

### 複数の要素を取得する

複数の要素を取得する方法は、どれも**配列に似たもの**を返します。

```javascript
const names = document.getElementsByClassName('name');   // HTMLCollection
names.length;                  // 3（要素の数）
names[0].textContent;          // 最初の要素の文字（番号は0から）

for (let i = 0; i < names.length; i++) {       // for 文で1つずつ処理する
    names[i].textContent = `${i + 1}. ${names[i].textContent}`;
}

const prices = document.querySelectorAll('.price');      // NodeList
prices.forEach((price) => {                    // querySelectorAll の結果は forEach が使える
    price.textContent += '円';
});
```

| 書き方 | 説明 |
|---|---|
| `.length` | 要素の数 |
| `[0]`・`[1]`・`[i]` | 最初・2番目・`i`番目の要素（**番号は0から**） |
| `for (let i = 0; i < 要素.length; i++)` | 1つずつ処理する（`HTMLCollection`でも`NodeList`でも使える） |
| `NodeList.forEach((x) => { ... })` | 1つずつ処理する。**`querySelectorAll`の結果だけ**で使える（`HTMLCollection`には`forEach`が無い） |

#### 🐍 Pythonとの違い

```python
# Python
names = ['りんご', 'バナナ', 'みかん']
len(names)          # 3
names[0]            # 'りんご'
for name in names:
    print(name)
```

| | Python | JavaScript |
|---|---|---|
| 要素の数 | `len(names)` | `names.length`（**関数ではなくプロパティ**） |
| 最初の要素 | `names[0]` | `names[0]`（同じ） |
| 1つずつ処理 | `for name in names:` | `for`文または`forEach`（`HTMLCollection`は`for`文のみ） |

### どれを使えばよいか

| 取得したいもの | おすすめ |
|---|---|
| `id`の付いた1つの要素 | `getElementById('id')`。短く書けて、このカリキュラムの基本の書き方 |
| `id`以外で1つ（クラス・タグ・複雑な条件） | `querySelector('セレクタ')` |
| 複数の要素 | `querySelectorAll('セレクタ')`。`forEach`が使えるので扱いやすい |
| `getElementsByClassName`・`getElementsByTagName` | 古いコードでよく見かける。読めれば十分で、新しく書くなら`querySelectorAll`でよい |

### 見つからないとき

```javascript
document.getElementById('nothing');                // null
document.querySelector('.nothing');                // null
document.querySelectorAll('.nothing').length;      // 0（空。エラーにはならない）
document.getElementsByClassName('nothing').length; // 0
```

1つを取得する方法は`null`（「無い」ことを表す値。[05_js_basicsの5節](../05_js_basics/#5-発展nullと真偽の判定)）になり、その`textContent`を書き換えようとすると、`TypeError`になります（[4節](#4-動かないときの調べ方)）。複数を取得する方法は、見つからなくても空になるだけで、エラーにはなりません（何も起きないので、気づきにくくなります）。

### 動作確認

`example/02_select_elements/index.html`をブラウザで開いて確認します。

| 確認する操作 | 確認したいこと |
|---|---|
| 「1.」を見る | 見出しの下の文が「querySelector で取得して、書き換えました」になり、「見出しの文字：…／h1の文字：…」と表示される |
| 「2.」を見る | 商品名の頭に`1. `・`2. `・`3. `が付き、価格の後ろに`円`が付いている。「商品は3個です」と表示される |
| Consoleを見る | `true`・`3`・`りんご`の後に、`null`・`null`・`0`・`0`と出力されている |
| `script.js`の最後のコメントアウトされた行を、コメントから戻してリロードする | `TypeError: Cannot set properties of null`が出る（確認したら、コメントに戻す） |

### 練習問題3：querySelectorで1つ取得する

> 問題：[question/03_query_selector/index.html](question/03_query_selector/index.html)・[question/03_query_selector/script.js](question/03_query_selector/script.js) ｜ 解答：[question/answer/03_query_selector/index.html](question/answer/03_query_selector/index.html)・[question/answer/03_query_selector/script.js](question/answer/03_query_selector/script.js)

<details>
<summary>問題の内容を開く</summary>

`03_query_selector/script.js`の`TODO 1`〜`TODO 3`に、`querySelector`で3種類のセレクタを使って、要素を取得して書き換える処理を書きます。`03_query_selector/index.html`をブラウザで開くと、ページの下のテストが実行され、Consoleに ✅（正しい）／❌（間違い）が表示されます。**1問ずつ**書いてリロードし、その問題が ✅ になるのを確かめてから、次に進みます（まだ書いていない問題が ❌ になるのは正常です）。

| # | 取得する要素 | 書き換える文字 |
|---|---|---|
| 1 | `<h1>`（タグ） | `タグで取得しました` |
| 2 | `id`が`heading`の要素 | `idで取得しました` |
| 3 | クラスが`note`の要素 | `クラスで取得しました` |

| # | ヒント |
|---|---|
| 1 | タグ名はそのまま書く：`querySelector('h1')` |
| 2 | `id`は`#`を付ける：`querySelector('#heading')`（`getElementById`では`#`は付けなかった） |
| 3 | クラスは`.`を付ける：`querySelector('.note')` |

</details>

### 練習問題4：複数の要素を取得して、数える・取り出す

> 問題：[question/04_get_all/index.html](question/04_get_all/index.html)・[question/04_get_all/script.js](question/04_get_all/script.js) ｜ 解答：[question/answer/04_get_all/index.html](question/answer/04_get_all/index.html)・[question/answer/04_get_all/script.js](question/answer/04_get_all/script.js)

<details>
<summary>問題の内容を開く</summary>

`04_get_all/script.js`の`TODO 1`〜`TODO 4`に、複数の要素を取得して、数や特定の1つを表示する処理を書きます。`04_get_all/index.html`をブラウザで開くと、ページの下のテストが実行され、Consoleに ✅（正しい）／❌（間違い）が表示されます。**1問ずつ**書いてリロードし、その問題が ✅ になるのを確かめてから、次に進みます（まだ書いていない問題が ❌ になるのは正常です）。

| # | やること | 表示する要素の`id` | 表示する文字 |
|---|---|---|---|
| 1 | クラスが`item`の要素の数（`getElementsByClassName`） | `count-output` | `3個` |
| 2 | タグが`li`の要素の数（`getElementsByTagName`） | `tag-count-output` | `3個` |
| 3 | クラスが`name`の要素の、最初の商品名 | `first-output` | `りんご` |
| 4 | 同じ要素の、最後の商品名 | `last-output` | `みかん` |

| # | ヒント |
|---|---|
| 1・2 | 結果の`.length`が数。`getElementsBy…`に渡すクラス名・タグ名には、`.`や`#`を付けない |
| 3 | `[0]`で最初の要素を取り出し、その`textContent`を読む |
| 4 | 最後の番号は`個数 - 1`：`names[names.length - 1]` |

</details>

### 練習問題5：複数の要素をまとめて書き換える

> 問題：[question/05_query_selector_all/index.html](question/05_query_selector_all/index.html)・[question/05_query_selector_all/script.js](question/05_query_selector_all/script.js) ｜ 解答：[question/answer/05_query_selector_all/index.html](question/answer/05_query_selector_all/index.html)・[question/answer/05_query_selector_all/script.js](question/answer/05_query_selector_all/script.js)

<details>
<summary>問題の内容を開く</summary>

`05_query_selector_all/script.js`の`TODO 1`・`TODO 2`に、複数の要素を1つずつ書き換える処理を書きます。`05_query_selector_all/index.html`をブラウザで開くと、ページの下のテストが実行され、Consoleに ✅（正しい）／❌（間違い）が表示されます。**1問ずつ**書いてリロードし、その問題が ✅ になるのを確かめてから、次に進みます（まだ書いていない問題が ❌ になるのは正常です）。

| # | やること |
|---|---|
| 1 | クラスが`fruit`の要素を`querySelectorAll`で取得し、`forEach`で、文字の前に「・」を付ける（`りんご` → `・りんご`） |
| 2 | クラスが`veg`の要素を`getElementsByClassName`で取得し、`for`文で、文字の前に番号を付ける（`にんじん` → `1. にんじん`。番号は1から） |

| # | ヒント |
|---|---|
| 1 | `` fruit.textContent = `・${fruit.textContent}`; ``のように、今の文字を使って作り直す |
| 2 | `HTMLCollection`には`forEach`が無いので、`for (let i = 0; i < 要素.length; i++)`と`要素[i]`を使う。表示する番号は`i + 1` |

</details>

---

## 3. textContentを使いこなす

> [example/03_text_content/index.html](example/03_text_content/index.html) / [example/03_text_content/script.js](example/03_text_content/script.js)

`textContent`は、読み取り・書き換えのほかに、追記や消去にも使えます。

| やりたいこと | 書き方 | 説明 |
|---|---|---|
| 読み取る | `const text = 要素.textContent;` | 要素の中の文字を取り出す。**常に文字列** |
| 書き換える | `要素.textContent = '新しい文字';` | 今の文字は消えて、置き換わる |
| 追記する | `要素.textContent += '追加の文字';` | 今の文字の**後ろ**に追加する（`a += b`は`a = a + b`） |
| 空にする | `要素.textContent = '';` | 中身を消す |
| 文字列を数値にする | `Number(要素.textContent)` | 計算に使うとき |

### 読み取った値は文字列：`Number()`

```javascript
const unitPrice = document.getElementById('unit-price');   // <span id="unit-price">1000</span>

unitPrice.textContent;                        // '1000'（文字列）
unitPrice.textContent + 500;                  // '1000500'（文字列の連結になってしまう）
Number(unitPrice.textContent) + 500;          // 1500（数値に変換してから足す）
```

`textContent`で読んだ値は、数字に見えても**文字列**です。計算に使うときは、`Number()`で数値に変換します。`textContent`に数値を代入するのは、そのままで構いません（文字として表示されます）。

#### 🐍 Pythonとの違い

| | Python | JavaScript |
|---|---|---|
| 文字列を数値にする | `int('1000')` / `float('1.5')` | `Number('1000')`（整数も小数も同じ） |
| 文字列 + 数値 | `'1000' + 500` → **エラー** | `'1000' + 500` → `'1000500'`（**エラーにならず、連結される**） |

JavaScriptは、文字列と数値を`+`で足してもエラーにならず、文字列として連結します。足し算のつもりで連結されても気づきにくいので、`Number()`を忘れないようにします。

### タグを入れても、文字として表示される

```javascript
element.textContent = '<b>太字</b>';    // 画面には <b>太字</b> という文字がそのまま表示される
```

`textContent`は、入れた文字列を**ただの文字**として扱います。タグとして解釈して入れる`innerHTML`は、ユーザーの入力を入れると危険（XSS）なので、[09_js_dom](../09_js_dom/)で学びます。

### 子要素ごと置き換わる

```html
<div id="box"><span>子要素1</span> <span>子要素2</span></div>
```

```javascript
box.textContent;                // '子要素1 子要素2'（子要素の文字もまとめて読める）
box.textContent = '全部置き換わる';   // 中の <span> もすべて消えて、文字だけになる
```

要素の`textContent`を書き換えると、**その中にあった子要素もすべて消えます**。文字を書き換えたい要素の中に、残したい子要素がないかに注意します。

### 動作確認

`example/03_text_content/index.html`をブラウザで開いて確認します。

| 確認する操作 | 確認したいこと |
|---|---|
| 「1.」を見る | 「3個買うと 3000円」と表示されている（`Number()`で数値にして、3倍している） |
| Consoleを見る | `1000`・`1000500`・`1500`・`子要素1 子要素2`の順に出力されている（`'1000500'`は文字列の連結になった例） |
| 「2.」を見る | 「1行目 / 2行目 / 3行目」と表示されている（`+=`で追記している） |
| 「3.」を見る | `<b>太字</b> を入れても…`と、`<b>`がそのまま文字で表示されている |
| 「4.」を見る | 2つの`<span>`が、1つの文字に置き換わっている |

### 練習問題6：文字を読み取って計算する

> 問題：[question/06_read_number/index.html](question/06_read_number/index.html)・[question/06_read_number/script.js](question/06_read_number/script.js) ｜ 解答：[question/answer/06_read_number/index.html](question/answer/06_read_number/index.html)・[question/answer/06_read_number/script.js](question/answer/06_read_number/script.js)

<details>
<summary>問題の内容を開く</summary>

`06_read_number/script.js`の`TODO 1`・`TODO 2`に、ページに書かれた数字を読み取って、計算する処理を書きます。`06_read_number/index.html`をブラウザで開くと、ページの下のテストが実行され、Consoleに ✅（正しい）／❌（間違い）が表示されます。**1問ずつ**書いてリロードし、その問題が ✅ になるのを確かめてから、次に進みます（まだ書いていない問題が ❌ になるのは正常です）。

| # | やること | 表示する要素の`id` | 表示する文字 |
|---|---|---|---|
| 1 | `unit-price`（単価）と`quantity`（数量）を読み取って掛け算する | `total-output` | `3000円` |
| 2 | 1の合計に、送料500円を足す | `shipping-output` | `3500円` |

| # | ヒント |
|---|---|
| 1 | `textContent`で読んだ値は文字列。`Number()`で数値に変換してから計算する |
| 2 | 合計が数値なら、`+`は足し算になる。文字列のままだと`'3000' + 500`は`'3000500'`になってしまう |

</details>

### 練習問題7：追記する・消す・置き換える

> 問題：[question/07_append_clear/index.html](question/07_append_clear/index.html)・[question/07_append_clear/script.js](question/07_append_clear/script.js) ｜ 解答：[question/answer/07_append_clear/index.html](question/answer/07_append_clear/index.html)・[question/answer/07_append_clear/script.js](question/answer/07_append_clear/script.js)

<details>
<summary>問題の内容を開く</summary>

`07_append_clear/script.js`の`TODO 1`〜`TODO 3`に、`textContent`で文字を追記・消去・置き換える処理を書きます。`07_append_clear/index.html`をブラウザで開くと、ページの下のテストが実行され、Consoleに ✅（正しい）／❌（間違い）が表示されます。**1問ずつ**書いてリロードし、その問題が ✅ になるのを確かめてから、次に進みます（まだ書いていない問題が ❌ になるのは正常です）。

| # | やること | 取得する要素の`id` | 結果 |
|---|---|---|---|
| 1 | 今の文字（`開始`）の後ろに、「 → 次」「 → 終了」を続けて追加する | `log-output` | `開始 → 次 → 終了` |
| 2 | 文字を消して、空にする | `temp-output` | （空） |
| 3 | 文字を「置き換えました」にする。中の`<span>`も消える | `box` | `置き換えました` |

| # | ヒント |
|---|---|
| 1 | `+=`で追記する（2回書く） |
| 2 | 空文字`''`を代入する |
| 3 | 親要素の`textContent`を書き換えると、子要素もすべて消える |

</details>

### 練習問題8：要素を取得して書き換える（まとめ）

> 問題：[question/08_select_elements/index.html](question/08_select_elements/index.html)・[question/08_select_elements/script.js](question/08_select_elements/script.js) ｜ 解答：[question/answer/08_select_elements/index.html](question/answer/08_select_elements/index.html)・[question/answer/08_select_elements/script.js](question/answer/08_select_elements/script.js)

<details>
<summary>問題の内容を開く</summary>

2節・3節のまとめです。`08_select_elements/script.js`の`TODO 1`〜`TODO 5`を書きます。`08_select_elements/index.html`をブラウザで開くと、ページの下のテストが実行され、Consoleに ✅（正しい）／❌（間違い）が表示されます。**1問ずつ**書いてリロードし、その問題が ✅ になるのを確かめてから、次に進みます（まだ書いていない問題が ❌ になるのは正常です）。

| # | やること | 取得する要素 |
|---|---|---|
| 1 | 見出しを「商品一覧」にする | `.page-title` |
| 2 | 商品の数を「3個」と表示する（HTMLに商品が増えても、数が合うように、数える） | `.item`の数 → `#count-output` |
| 3 | 最初の商品名を表示する | `.name`の最初 → `#first-output` |
| 4 | すべての価格を足して、「350円」と表示する | `.price`すべて → `#sum-output` |
| 5 | 3つの価格の後ろに、それぞれ「円」を付ける（「120円」「80円」「150円」） | `.price`すべて |

| # | ヒント |
|---|---|
| 1 | `document.querySelector('.page-title')`。クラスは`.`を付ける |
| 2 | `getElementsByClassName('item')`の`.length` |
| 3 | `getElementsByClassName('name')`の`[0]`の`textContent` |
| 4 | `querySelectorAll('.price')`を`forEach`で回し、合計を入れる変数は`let`で用意する。`textContent`で読んだ値は文字列なので、`Number()`で数値に変換してから足す |
| 5 | `+=`で追記する。**4の計算が終わってから**行う（先に「円」を付けると、`Number('120円')`は計算できない） |

5を4より前に書くと、合計金額が`NaN`（数値ではない）になります。確認したら戻します。

</details>

---

## 4. 動かないときの調べ方

書き換えがうまくいかないときは、[05_js_basicsの0節](../05_js_basics/#0-javascriptの読み込み方とデバッグ)の方法で原因を探します。この章でよく出る原因は、次のとおりです。

| 画面・Consoleの様子 | 原因 |
|---|---|
| `Cannot set properties of null (setting 'textContent')`<br>`Cannot read properties of null (reading 'textContent')` | `getElementById`の`id`の綴りが違う／HTMLに`id`が無い／`<script>`が書き換える要素より前（`<head>`）にある／`querySelector('message')`のように、`#`や`.`を付け忘れた（`message`という**タグ**を探してしまう）。取得できなかった要素は`null`になり、`null`の`textContent`は読み書きできない |
| エラーは出ないのに、画面が変わらない | `textcontent`のように、プロパティ名の**大文字小文字**が違う。存在しないプロパティに値を代入しただけなので、エラーにならない |
| エラーは出ないのに、複数の要素が書き換わらない | `getElementsByClassName('.name')`のように、`.`を付けている。何も見つからず、空のまま`for`文が1回も回らない |
| `Cannot read properties of undefined (reading 'textContent')` | `names[3]`のように、存在しない番号を指定した（3つなら、`[0]`〜`[2]`まで）。`[3]`は`undefined`になる |
| `names.forEach is not a function` | `getElementsByClassName`の結果（`HTMLCollection`）には`forEach`が無い。`for`文を使うか、`querySelectorAll`にする |
| 合計が`NaN`・連結された文字になる | `textContent`で読んだ値を、`Number()`で数値にしていない／「円」を付けた後の文字を数値にしようとしている |
| 表示が`undefined`になる | `lenght`のようにプロパティ名を打ち間違えて、読み取っている |

エラーが出ないのに画面が変わらないときは、`console.log(取得した変数)`で`null`や空でないかを確かめたり、Sourcesパネルのブレークポイントで変数の中身を見たりします。

### 練習問題9：書き換わらないページを直す

> 問題：[question/09_debug_dom/index.html](question/09_debug_dom/index.html)・[question/09_debug_dom/script.js](question/09_debug_dom/script.js) ｜ 解答：[question/answer/09_debug_dom/index.html](question/answer/09_debug_dom/index.html)・[question/answer/09_debug_dom/script.js](question/answer/09_debug_dom/script.js)

<details>
<summary>問題の内容を開く</summary>

`09_debug_dom/index.html`は、2つの段落をJavaScriptで書き換えるはずのページですが、書き換わりません。バグは3つあります（HTMLに1つ、`09_debug_dom/script.js`に2つ）。ConsoleのエラーメッセージとSourcesパネルのブレークポイントを使って、原因を見つけて直します。

| # | 進め方 |
|---|---|
| 1 | まずConsoleを開いてリロードし、赤字のエラーを読む（何行目の、何が`null`か） |
| 2 | エラーを1つ直したらリロードし、次のエラーを見る |
| 3 | エラーは出ないのに画面がおかしいときは、`console.log()`かブレークポイントで、変数の中身を確認する |

| 確認する操作 | 確認したいこと |
|---|---|
| ブラウザで開く | 上の段落が「JavaScriptで書き換えました」、下の段落が「合計：1200円」になっている |
| Consoleを見る | エラーが出ていない |

</details>

---

## 次のステップ

続きは [07_js_events](../07_js_events/) です。ここで書き換えた文字を、ボタンのクリックや入力に反応して書き換える方法（イベント）を学びます。
