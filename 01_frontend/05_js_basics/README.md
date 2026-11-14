# 05 JavaScriptの基本文法

> フロントエンド編 ／ 前の章：[04_css_layout](../04_css_layout/) ／ 次の章：[06_js_dom_basics](../06_js_dom_basics/)

HTMLが「構造」、CSSが「見た目」を担当するのに対し、**JavaScript**はWebページの「動き」を担当する、ブラウザの中で動くプログラミング言語です。この章では、JavaScriptの読み込み方とデバッグの方法、変数・関数・条件分岐などの**最小限の基本文法**と、コールバック関数を学びます。

文法は、一度に覚えようとしません。この章は、**1つの節で1つのことだけ**を学び、そのたびにConsoleで結果を確かめ、**小問**（その節の文法だけを使う短い問題）で手を動かす順番になっています。小問のあとに、複数の文法を組み合わせる**練習問題**があります。

| 節 | 学ぶこと | 練習問題 |
|---|---|---|
| 1 | 変数とデータ型 | 小問1 |
| 2 | 関数 | 小問2 |
| 3 | 条件分岐・繰り返し・配列 | 小問3・練習問題1 |
| 4 | 関数を渡す（コールバック関数） | 練習問題2 |
| 5 | 発展：`null`と真偽の判定 | 練習問題3 |

1〜4節で、次の[06_js_dom_basics](../06_js_dom_basics/)に進むための文法は揃います。**5節は発展**です。次の章でも`null`が少し出てきますが、そこで説明するので、先に進み、`null`や真偽の判定が出てきたときに戻ってきても構いません。三項演算子・`trim()`・配列メソッドなどの残りの文法は、それが初めて必要になる章（[08_js_forms](../08_js_forms/)・[10_js_render](../10_js_render/)）で学びます。

## 目次

0. [JavaScriptの読み込み方とデバッグ](#0-javascriptの読み込み方とデバッグ)
1. [変数とデータ型](#1-変数とデータ型)
2. [関数](#2-関数)
3. [条件分岐・繰り返し・配列](#3-条件分岐繰り返し配列)
4. [関数を渡す：コールバック関数](#4-関数を渡すコールバック関数)
5. [発展：nullと真偽の判定](#5-発展nullと真偽の判定)
6. [まとめ：Pythonとの対応表](#まとめpythonとの対応表)

---

## フォルダ構成

```
01_frontend/05_js_basics/
├── README.md
├── example/                      サンプル（1つのサンプル＝1つのフォルダ）
│   ├── 00_first_click/           まず動かしてみる（ボタンを押すと文字が変わる）
│   │   └── index.html
│   ├── 01_variables/             変数・データ型・テンプレートリテラル
│   │   ├── index.html
│   │   └── script.js
│   ├── 02_functions/             関数・アロー関数
│   │   ├── index.html
│   │   └── script.js
│   ├── 03_control_flow/          条件分岐・繰り返し・配列
│   │   ├── index.html
│   │   └── script.js
│   ├── 04_callbacks/             関数は値・コールバック関数
│   │   ├── index.html
│   │   └── script.js
│   └── 05_null_and_truthy/       null・undefined・真偽の判定・==（発展）
│       ├── index.html
│       └── script.js
└── question/                     小問（3問）と練習問題（3問）。問題文はREADMEの各節の最後
    ├── 01_variables/             小問1：変数とデータ型
    │   ├── index.html
    │   └── script.js
    ├── 02_functions/             小問2：関数
    │   ├── index.html
    │   └── script.js
    ├── 03_control_flow/          小問3：条件分岐・繰り返し・配列
    │   ├── index.html
    │   └── script.js
    ├── 04_basic_functions/       練習問題1：基本文法で関数を書く
    │   ├── index.html
    │   └── script.js
    ├── 05_callbacks/             練習問題2：コールバック関数を書く
    │   ├── index.html
    │   └── script.js
    ├── 06_output_quiz/           練習問題3：何が出力されるか予想する
    │   ├── index.html
    │   └── script.js
    └── answer/                   解答（問題と同じ名前のフォルダ。中のファイル構成も問題と同じ）
        ├── 01_variables/
        ├── 02_functions/
        ├── 03_control_flow/
        ├── 04_basic_functions/
        ├── 05_callbacks/
        └── 06_output_quiz/
```

---

## 0. JavaScriptの読み込み方とデバッグ

### まず動かしてみる

> [example/00_first_click/index.html](example/00_first_click/index.html)

文法を学ぶ前に、JavaScriptがブラウザの中で動くところを見てみます。`example/00_first_click/index.html`をブラウザで開いて、ボタンを押してください。

```html
<button type="button" id="hello-button">押してみてください</button>
<p id="message"></p>

<script>
    document.getElementById('hello-button').addEventListener('click', () => {
        document.getElementById('message').textContent = 'JavaScriptが動きました！';
    });
</script>
```

ボタンを押すと、下に「JavaScriptが動きました！」と表示されます。これは、「ボタンが押されたら、段落の文字を書き換える」という、たった3行のプログラムです。**しくみは[06_js_dom_basics](../06_js_dom_basics/)（書き換え）と[07_js_events](../07_js_events/)（クリック）で学びます**。まずはこの章で、このプログラムを書くための最小限の文法（変数・関数・`if`など）を、**1つずつ小さく動かしながら**身につけます。

### `<script>`タグ

JavaScriptは、CSSと同じく別ファイル（`.js`）に書いてHTMLから読み込むのが基本です。

```html
<body>
    ...ページの内容...

    <!-- </body> の直前に書く -->
    <script src="script.js"></script>
</body>
```

| ポイント | 説明 |
|---|---|
| `src` | 読み込むJavaScriptファイルのパス（CSSの`<link href>`と同じく相対パスで書ける） |
| `</body>`の直前に置く | ブラウザはHTMLを上から順に読む。`<head>`で読み込むと、まだ存在しない要素をJavaScriptが探してしまい、`null`になって動かない |
| `<script defer src="...">` | `<head>`に書きたい場合は`defer`を付けると、HTMLを読み終えてから実行される（どちらの書き方でもよい） |

### コンソール

開発者ツール（`F12`／Mac：`Cmd + Option + I`）の**Console**タブには、`console.log()`で出力した値と、JavaScriptのエラーが表示されます。Consoleに直接`1 + 2`のように打ち込んで、その場でJavaScriptを試すこともできます。

### 動かないときの調べ方

JavaScriptは、エラーが起きるとその行で処理が止まり、それ以降のコードが実行されません。「動かない」ときは次の順に調べます。

1. **Consoleに赤字のエラーが出ていないか**を見る。エラー文の右端のファイル名と行番号をクリックすると、該当行に移動できる
2. エラーが出ていないのに動きがおかしいときは、**途中の値を確かめる**。`console.log(変数)`を入れるか、**Sources**パネルでファイルを開き、行番号をクリックして**ブレークポイント**を置く。その行で処理が一時停止し、変数にマウスを乗せると中身が見える（再開は▶ボタン）

よく出るエラーは次の3つです。

| エラー | 意味 | よくある原因 |
|---|---|---|
| `TypeError: Cannot read properties of null (reading 'addEventListener')` | `null`のプロパティを読もうとした | `getElementById`の綴り間違い・HTMLの`id`の付け忘れ・`<script>`を`<head>`で読み込んでいる |
| `ReferenceError: xxx is not defined` | 定義されていない変数を使った | 変数名の打ち間違い・宣言する前に使っている |
| `SyntaxError: Unexpected token` | 文法が間違っている | カッコ・引用符の閉じ忘れ、`,`の付け忘れ |

存在しないプロパティを読んだとき（`value.lenght`のような打ち間違い）は、エラーにならず`undefined`になります。表示に`undefined`と出たら、プロパティ名を疑いましょう。07_js_events の練習問題6で、実際に探してみます。

---

## 1. 変数とデータ型

> [example/01_variables/index.html](example/01_variables/index.html) / [example/01_variables/script.js](example/01_variables/script.js)

まず、値を入れておく「変数」と、値の種類（データ型）を確認します。ブラウザで`example/01_variables/index.html`を開き、開発者ツールのConsoleで結果を確認してください。

### 変数：let と const

```javascript
let count = 1;
count = 2;   // let は再代入できる

const name = 'メモ帳';
// name = '別の名前';   // const は再代入できないのでエラーになる
```

JavaScriptでは、変数を使う前に`let`か`const`で宣言します（Pythonなら`x = 1`だけで使えますが、JavaScriptでは宣言が必要です）。何が変わるか分からない場合はまず`const`を使い、再代入が必要になったら`let`に変えるのが一般的です。

`const`で禁止されるのは**再代入だけ**です。`const list = [];`と宣言した配列に`list.push(1)`で要素を足すのは、変数に別の値を入れ直しているわけではないので、エラーになりません。

#### 🐍 Pythonとの違い

```python
# Python：宣言は要らない。代入すれば変数ができる。書き換えも自由
count = 1
count = 2
NAME = 'メモ帳'   # 定数は「大文字で書く」という慣習だけで、実際には書き換えられる
```

| | Python | JavaScript |
|---|---|---|
| 変数の作り方 | `x = 1`（宣言なし） | `let x = 1;` / `const x = 1;`（**宣言が必要**） |
| 書き換えを禁止 | できない（慣習で大文字にするだけ） | `const`で言語が禁止してくれる |
| 文の終わり | 改行 | `;`（省略もできるが、このカリキュラムでは付ける） |
| 名前の付け方 | `snake_case`（`memo_list`） | `camelCase`（`memoList`） |
| コメント | `# コメント` | `// コメント` / `/* 複数行 */` |

### データ型

```javascript
const str = 'こんにちは';                    // 文字列
const num = 42;                              // 数値（整数と小数を区別しない）
const isDone = true;                         // 真偽値（true / false）
const list = [1, 2, 3];                      // 配列（Pythonのlistに相当）
const obj = { title: 'メモ', category: '仕事' };   // オブジェクト（Pythonのdictに相当）

obj.title;                // 'メモ'（値の取り出しは . で書く。obj['title'] も可）
obj.category = '家事';     // 値の書き換え
```

### テンプレートリテラル

バッククォート(`` ` ``)で文字列を囲むと、`${式}`で変数や計算結果を埋め込めます（Pythonのf文字列に相当）。

```javascript
const message = `${name}には${list.length}件のメモがあります`;
```

#### 🐍 Pythonとの違い

```python
# Python
name = 'メモ帳'
items = [1, 2, 3]                                   # list
memo = {'title': 'メモ', 'category': '仕事'}          # dict
message = f'{name}には{len(items)}件のメモがあります'    # f文字列
memo['title']                                       # 値の取り出しは []
```

| | Python | JavaScript |
|---|---|---|
| 文字列の引用符 | `'...'` でも `"..."` でもよい | 同じ。さらに `` `...` ``（テンプレートリテラル）で`${}`が使える |
| 文字列に値を埋め込む | `f'{name}さん'` | `` `${name}さん` `` |
| 数値 | `int`と`float`が別 | `number`のみ（`42`も`4.2`も同じ型） |
| 真偽値 | `True` / `False`（大文字始まり） | `true` / `false`（すべて小文字） |
| 辞書／オブジェクト | `dict`：キーは文字列のまま `{'title': 'メモ'}` | オブジェクト：キーは引用符なしで書ける `{ title: 'メモ' }` |
| 要素の取り出し | `memo['title']` | `memo.title`（`memo['title']`も可） |
| 配列の長さ | `len(items)` | `items.length`（**関数ではなくプロパティ**なので`()`を付けない） |

### 動作確認：コンソールに出力される値を確認する

| 確認する行 | 確認したいこと |
|---|---|
| `console.log(count, name);` | `2 メモ帳`と出力される（`let`で再代入した後の`count`の値が`2`になっている） |
| `console.log(str, num, isDone, list, obj);` | 5つの値がそれぞれ出力される。配列とオブジェクトは▶を押すと中身が開く |
| `console.log(obj.title);` と`console.log(obj);` | `メモ`が出力され、書き換えたあとの`obj`では`category`が`家事`になっている |
| `console.log(message);` | `メモ帳には3件のメモがあります`と出力される（`${name}`・`${list.length}`が埋め込まれている） |
| `name = '別の名前';`のコメントを外してリロード | Consoleに`TypeError: Assignment to constant variable.`と赤字で出る（確認したら、コメントに戻す） |

### 小問1：変数とデータ型

> 問題：[question/01_variables/index.html](question/01_variables/index.html)・[question/01_variables/script.js](question/01_variables/script.js) ｜ 解答：[question/answer/01_variables/index.html](question/answer/01_variables/index.html)・[question/answer/01_variables/script.js](question/answer/01_variables/script.js)

<details>
<summary>問題の内容を開く</summary>

`01_variables/script.js`の`TODO 1`〜`TODO 5`に、変数を書きます。`01_variables/index.html`を開くと、ファイルの一番下のテストが実行され、Consoleに ✅（正しい）／❌（間違い）が表示されます。**1問ずつ**書いてリロードし、その問題のテストが ✅ になるのを確かめてから、次に進みます（まだ書いていない問題が ❌ になるのは正常です）。

| # | やること | 期待する値 |
|---|---|---|
| 1 | `const`で`userName`を宣言し、`'山田'`を入れる | `userName` → `'山田'` |
| 2 | `let`で`score`を`50`で宣言し、そのあと`80`に書き換える（再代入） | `score` → `80` |
| 3 | `memo`オブジェクトを作り（`title`は`'会議'`、`pinned`は`false`）、そのあと`pinned`を`true`に書き換える | `memo.pinned` → `true` |
| 4 | `tags`配列を作る（`'仕事'`と`'重要'`） | `tags.length` → `2` |
| 5 | `message`に、テンプレートリテラルで「山田さんのタグは2個です」を入れる（`userName`と`tags.length`を埋め込む） | `message` → `'山田さんのタグは2個です'` |

| # | ヒント |
|---|---|
| 1 | 書き換えない値は`const` |
| 2 | 値を変えるので`let`。`score = 80;`と、変数にもう一度代入する（`const`ではできない） |
| 3 | オブジェクトの値は、ドット（`memo.pinned`）で書き換える。`const`でも、中身の書き換えはできる |
| 5 | バッククォート`` ` ``で囲み、`${ }`の中に変数や`tags.length`を書く |

</details>

---

## 2. 関数

> [example/02_functions/index.html](example/02_functions/index.html) / [example/02_functions/script.js](example/02_functions/script.js)

処理に名前を付けてまとめたものが関数です。`return`で結果を呼び出し元に返します。

```javascript
// function 宣言
function add(a, b) {
    return a + b;
}

// アロー関数（このカリキュラムで多用する書き方）
const addArrow = (a, b) => {
    return a + b;
};

// 処理が1行だけなら {} と return を省略できる
const addShort = (a, b) => a + b;
```

3つとも同じ働きで、呼び出しも同じです（`add(1, 2)` → `3`）。**このあとは、主にアロー関数を使います**。

#### 🐍 Pythonとの違い

```python
# Python：インデント（字下げ）でブロックを表す
def add(a, b):
    return a + b

add_short = lambda a, b: a + b     # lambda は1行の式しか書けない
```

| | Python | JavaScript |
|---|---|---|
| 関数の定義 | `def add(a, b):` | `function add(a, b) { ... }` または `const add = (a, b) => { ... };` |
| ブロックの範囲 | **インデント**（字下げ）で決まる | **`{ }`**で決まる（字下げは見やすさのためだけ） |
| 1行で書く関数 | `lambda a, b: a + b`（式1つだけ） | `(a, b) => a + b`（複数行の関数も`=>`で書ける） |
| 戻り値 | `return`（無ければ`None`） | `return`（無ければ`undefined`）。`{ }`を省略した`=>`の形では`return`も省略 |
| 呼び出し | `add(1, 2)` | `add(1, 2)`（同じ） |
| 引数の数 | 足りないとエラー | 足りない引数は`undefined`になり、**エラーにならない** |

### 動作確認：コンソールに出力される値を確認する

| 確認する行 | 確認したいこと |
|---|---|
| `console.log(add(1, 2), addArrow(1, 2), addShort(1, 2));` | `3 3 3`と出力される（3つとも同じ結果を返す関数であることが分かる） |
| `console.log(greet('山田'));` | `こんにちは、山田さん`と出力される（テンプレートリテラルを`return`している） |
| `console.log(noReturn(1));` | `undefined`と出力される（`return`が無い関数は、何も返さない） |

### 小問2：関数

> 問題：[question/02_functions/index.html](question/02_functions/index.html)・[question/02_functions/script.js](question/02_functions/script.js) ｜ 解答：[question/answer/02_functions/index.html](question/answer/02_functions/index.html)・[question/answer/02_functions/script.js](question/answer/02_functions/script.js)

<details>
<summary>問題の内容を開く</summary>

`02_functions/script.js`の`TODO 1`〜`TODO 5`に、関数の中身を書きます。`02_functions/index.html`を開くと、ファイルの一番下のテストが実行され、Consoleに ✅（正しい）／❌（間違い）が表示されます。**1問ずつ**書いてリロードし、その問題のテストが ✅ になるのを確かめてから、次に進みます（まだ書いていない問題が ❌ になるのは正常です）。

| # | 関数 | やること | 書き方 | 例 |
|---|---|---|---|---|
| 1 | `double(n)` | `n`を2倍にして返す | `function`宣言 | `double(4)` → `8` |
| 2 | `add(a, b)` | 合計を返す | アロー関数（`{ }`と`return`） | `add(1, 2)` → `3` |
| 3 | `square(n)` | `n`の2乗を返す | アロー関数（`{ }`と`return`を省略した1行） | `square(5)` → `25` |
| 4 | `greet(name)` | 「こんにちは、山田さん」のような文字を返す | アロー関数＋テンプレートリテラル | `greet('山田')` → `'こんにちは、山田さん'` |
| 5 | `average(a, b)` | `a`と`b`の平均を返す | アロー関数 | `average(2, 4)` → `3`、`average(1, 2)` → `1.5` |

| # | ヒント |
|---|---|
| 1・2 | 値を返すには`return`を書く |
| 3 | `=>`のあとに式を書くだけで、その値が戻り値になる（`return`は書かない） |
| 5 | 足し算を`( )`で囲んでから、`/ 2`で割る（`( )`が無いと、`b`だけが2で割られる） |

</details>

---

## 3. 条件分岐・繰り返し・配列

> [example/03_control_flow/index.html](example/03_control_flow/index.html) / [example/03_control_flow/script.js](example/03_control_flow/script.js)

条件によって処理を分ける`if`、同じ処理を繰り返す`for`、複数の値をまとめる配列の操作を確認します。

### 条件分岐と比較

```javascript
if (score >= 80) {
    console.log('合格');
} else if (score >= 50) {
    console.log('もう少し');
} else {
    console.log('不合格');
}
```

値が等しいかどうかは`===`、等しくないかどうかは`!==`で比べます。

```javascript
score === 80;    // true（等しい）
score !== 80;    // false（等しくない）
1 === '1';       // false（数値の1と文字列の'1'は、型が違うので等しくない）
```

`===`は値と**型**の両方が等しいかを比べます。JavaScriptには`==`もありますが、型を勝手に変換して思わぬ結果になるため（[5節](#5-発展nullと真偽の判定)）、**比較は常に`===`と`!==`を使います**。

#### 🐍 Pythonとの違い

```python
# Python
if score >= 80:
    print('合格')
elif score >= 50:
    print('もう少し')
else:
    print('不合格')
```

| | Python | JavaScript |
|---|---|---|
| 条件の書き方 | `if score >= 80:`（`:`とインデント） | `if (score >= 80) { ... }`（**条件を`( )`で囲み、`{ }`でブロック**） |
| 「そうでなければ、もし」 | `elif` | `else if`（2語） |
| 等しいか | `==` | `===`（`==`は使わない） |
| 画面に出力 | `print(...)` | `console.log(...)`（ブラウザのConsoleに出る） |

### 繰り返し：for

```javascript
for (let i = 0; i < 3; i++) {
    console.log(`ループ ${i} 回目`);
}
```

`for (let i = 0; i < 3; i++)`は、「`i`を0から始め、`i < 3`の間、1回終わるごとに`i`を1増やす」という意味で、Pythonの`range(3)`に当たります。

値を足していくときは、`+=`と`++`を使うと短く書けます。

| 書き方 | 意味 | 例 |
|---|---|---|
| `a += b` | `a = a + b`の省略。`-=`・`*=`も同様 | `total += i;` |
| `a++` / `a--` | `a`を1増やす / 1減らす | `count++;` |

```javascript
let total = 0;                       // 後で値を足すので let
for (let i = 1; i <= 3; i++) {
    total += i;
}
console.log(total);                  // 6
```

#### 🐍 Pythonとの違い

```python
# Python
for i in range(3):
    print(f'ループ {i} 回目')

total = 0
for i in range(1, 4):
    total += i
```

| | Python | JavaScript |
|---|---|---|
| 回数を決めた繰り返し | `for i in range(3):` | `for (let i = 0; i < 3; i++) { ... }`（初期値；続ける条件；毎回の更新） |
| 1増やす | `count += 1`（`count++`は**書けない**） | `count += 1;` も `count++;` も書ける |

### 配列

```javascript
const categories = ['家事', '仕事', '趣味'];

categories.length;              // 3（要素の数）
categories.push('勉強');         // 配列の最後に追加する（元の配列が変わる）

// 配列を1件ずつ処理する（Pythonの for x in list: に相当）
categories.forEach((category) => {
    console.log(category);
});
```

| 書き方 | 説明 | 例 |
|---|---|---|
| `配列.length` / `文字列.length` | 要素の数 / 文字数 | `[1, 2, 3].length` → `3` |
| `配列.push(値)` | 配列の**最後**に追加する（元の配列が変わる） | `list.push('仕事')` |
| `配列.forEach((x) => { ... })` | 要素を1件ずつ取り出して処理する | 上の例 |

`forEach`の`(category) => { ... }`は、「要素1つごとに呼び出してもらう関数」です。この仕組みは、[4節](#4-関数を渡すコールバック関数)で詳しく学びます。ここでは「こう書くと1件ずつ処理できる」と読み進めて構いません。

配列を加工する`map`・`filter`・`find`・`includes`などは[10_js_render](../10_js_render/)で、文字列を加工する`trim`は[08_js_forms](../08_js_forms/)、`split`は[10_js_render](../10_js_render/)で学びます。

#### 🐍 Pythonとの違い

| やりたいこと | Python | JavaScript |
|---|---|---|
| 要素の数・文字数 | `len(x)` | `x.length`（**関数ではなくプロパティ**なので`()`を付けない） |
| 最後に追加 | `list.append(v)` | `list.push(v)` |
| 配列を1件ずつ | `for x in list:` | `list.forEach((x) => { ... });` |
| 割り算 | `7 / 2` → `3.5`、`7 // 2` → `3` | `7 / 2` → `3.5`。整数にするには`Math.floor(7 / 2)`（[10_js_render](../10_js_render/)で学ぶ） |

### 動作確認：コンソールに出力される値を確認する

| 確認する行 | 確認したいこと |
|---|---|
| 条件分岐の出力 | `合格`と出力される（`score`を`60`・`30`に変えると`もう少し`・`不合格`になる） |
| `score === 80`の3行 | `true`・`false`・`false`の順に出力される |
| for文の出力 | `ループ 0 回目`〜`ループ 2 回目`の順に出力され、続けて合計の`6`が出力される |
| `categories.length`（`push`の前後） | `3`→`4`と出力される（`push()`で配列に要素が増えた） |
| `forEach`の出力 | `家事`・`仕事`・`趣味`の順に出力される |
| オブジェクトの配列の出力 | `1：買い物リスト`・`2：企画会議メモ`の順に出力される |

**正常な状態の見分け方**：コンソールに赤字のエラー（`Uncaught ReferenceError`など）が出ていなければ、上から順にすべての`console.log`が実行されています。途中で出力が止まっている場合は、それより前の行に文法ミスがないか確認してください。

### 小問3：条件分岐・繰り返し・配列

> 問題：[question/03_control_flow/index.html](question/03_control_flow/index.html)・[question/03_control_flow/script.js](question/03_control_flow/script.js) ｜ 解答：[question/answer/03_control_flow/index.html](question/answer/03_control_flow/index.html)・[question/answer/03_control_flow/script.js](question/answer/03_control_flow/script.js)

<details>
<summary>問題の内容を開く</summary>

`03_control_flow/script.js`の`TODO 1`〜`TODO 6`に、関数の中身を書きます。`03_control_flow/index.html`を開くと、ファイルの一番下のテストが実行され、Consoleに ✅（正しい）／❌（間違い）が表示されます。**1問ずつ**書いてリロードし、その問題のテストが ✅ になるのを確かめてから、次に進みます（まだ書いていない問題が ❌ になるのは正常です）。

| # | 関数 | やること | 例 |
|---|---|---|---|
| 1 | `signOf(n)` | `n`が0より大きければ`'正'`、0なら`'ゼロ'`、それ以外は`'負'`を返す | `signOf(5)` → `'正'`、`signOf(-2)` → `'負'` |
| 2 | `isSame(a, b)` | `a`と`b`が、型も含めて等しいかを`true` / `false`で返す | `isSame(1, '1')` → `false` |
| 3 | `repeatText(text, times)` | `text`を`times`回つなげた文字を返す（`for`文） | `repeatText('ab', 3)` → `'ababab'` |
| 4 | `sum(list)` | 配列の数値の合計を返す（`forEach`） | `sum([1, 2, 3])` → `6`、`sum([])` → `0` |
| 5 | `addItem(list, item)` | 配列の最後に`item`を追加して、追加後の件数を返す | `addItem(['a'], 'b')` → `2` |
| 6 | `getTitles(memos)` | メモの配列から、`title`だけを取り出した新しい配列を返す（`forEach`と`push`） | `getTitles([{ title: '会議' }])` → `['会議']` |

| # | ヒント |
|---|---|
| 1 | `if` / `else if` / `else`。0かどうかは`n === 0` |
| 2 | 比較は`===`。結果をそのまま`return`してよい |
| 3 | 文字を入れる変数を`let`で用意し、`+=`でつなげる |
| 4 | 合計を入れる変数を`let`で用意し、`forEach`の中で足す |
| 5 | `list.push(item)`のあと、`list.length`を返す |
| 6 | 空の配列を`const`で用意し、`forEach`の中で`push`する（`const`でも`push`はできる） |

</details>

### 練習問題1：基本文法で関数を書く

> 問題：[question/04_basic_functions/index.html](question/04_basic_functions/index.html)・[question/04_basic_functions/script.js](question/04_basic_functions/script.js) ｜ 解答：[question/answer/04_basic_functions/index.html](question/answer/04_basic_functions/index.html)・[question/answer/04_basic_functions/script.js](question/answer/04_basic_functions/script.js)

<details>
<summary>問題の内容を開く</summary>

`04_basic_functions/script.js`の`TODO 1`〜`TODO 6`の関数の中身を書きます。1〜3節の内容だけで解けます。`04_basic_functions/index.html`を開くと、ファイルの一番下のテストが実行され、Consoleに ✅（正しい）／❌（間違い）が表示されます。❌のときは、結果と期待する値も表示されます。すべて ✅ になれば完成です。

**1問ずつ進めましょう**。1問書くたびにリロードして、その問題のテストが ✅ になるのを確かめてから、次に進みます（まだ書いていない問題が ❌ になるのは正常です）。

変数の宣言には`let`か`const`を使い（`var`は使わない）、比較には`===` / `!==`を使います。

| # | 関数 | やること | 例 |
|---|---|---|---|
| 1 | `getGrade(score)` | 点数から評価を返す。80点以上→`'合格'`、50点以上→`'もう少し'`、それ以外→`'不合格'` | `getGrade(80)` → `'合格'` |
| 2 | `formatMemo(memo)` | メモのオブジェクトから「[カテゴリ] タイトル」という文字列を作る | `formatMemo({ title: '企画会議メモ', category: '仕事' })` → `'[仕事] 企画会議メモ'` |
| 3 | `sumTo(n)` | 1からnまでの合計を返す | `sumTo(3)` → `6`、`sumTo(10)` → `55` |
| 4 | `isFilled(text)` | 文字が「1文字以上」あるか（空文字でないか）を`true` / `false`で返す | `isFilled('メモ')` → `true`、`isFilled('')` → `false` |
| 5 | `countByCategory(memos, category)` | メモの配列のうち、指定したカテゴリのメモが何件あるかを返す | `countByCategory(memos, '仕事')` → `2` |
| 6 | `describeList(list)` | 配列の件数を文章で返す。0件なら`'メモはありません'`、それ以外なら`'3件のメモがあります'`のように返す | `describeList([])` → `'メモはありません'` |

| # | ヒント |
|---|---|
| 1 | `if` / `else if` / `else` |
| 2 | テンプレートリテラル（バッククォート`` ` ``と`${}`） |
| 3 | 合計を入れる変数は、あとで値を足していくので`let`で宣言する。`for`文で1からnまで繰り返す |
| 4 | `text !== ''`の結果をそのまま`return`してもよいし、`if`で`true` / `false`を返してもよい |
| 5 | 件数を入れる変数を`let`で用意し、`forEach`で1件ずつ見て、カテゴリが等しければ1増やす |
| 6 | 配列の件数は`list.length`。0件かどうかは`list.length === 0`で調べる |

</details>

---

## 4. 関数を渡す：コールバック関数

> [example/04_callbacks/index.html](example/04_callbacks/index.html) / [example/04_callbacks/script.js](example/04_callbacks/script.js)

### 関数は「値」として扱える

```javascript
const greet = (name) => `こんにちは、${name}さん`;

typeof greet;        // 'function'（() を付けない → 関数そのもの）
typeof greet('a');   // 'string'  （() を付ける → 呼び出した結果）
```

JavaScriptでは、関数を変数に入れたり、別の関数の引数に渡したりできます。`()`を付けるかどうかで「関数そのもの」か「呼び出した結果」かが変わる点に注意します。

### コールバック関数

引数として渡し、**相手の都合のよいタイミングで呼び出してもらう関数**を、コールバック関数と呼びます。

```javascript
const repeat = (times, callback) => {
    for (let i = 0; i < times; i++) {
        callback(i);            // 受け取った関数を、ここで呼び出す
    }
};

repeat(3, (i) => console.log(`${i + 1}回目`));
```

3節で使った`forEach`も、この後の`addEventListener`も、コールバック関数を受け取る関数です。

```javascript
memos.forEach((memo) => { ... });                   // 要素1つごとに呼び出してもらう
button.addEventListener('click', () => { ... });    // クリックされたときに呼び出してもらう
```

この「あとで呼び出してもらう関数を渡す」考え方は、`02_backend/03_function`でPythonのデコレータを学ぶときや、[12_js_data](../12_js_data/)の`fetch()`で通信の結果を受け取るときにも出てきます。

#### 🐍 Pythonとの違い

Pythonでも関数は値として渡せます（`sorted(items, key=len)`の`key`など）。書き方の違いは、無名関数の書き方です。

| | Python | JavaScript |
|---|---|---|
| 名前のある関数を渡す | `run(say_hi)` | `run(sayHi)`（どちらも`()`を付けない） |
| その場で作った関数を渡す | `run(lambda x: x * 2)`（式1つだけ） | `run((x) => x * 2)`（複数行の処理も書ける） |
| 呼び出した結果を渡す | `run(say_hi())` | `run(sayHi())`（意味も同じ。**間違いやすい**） |

### 動作確認：コンソールに出力される値を確認する

`example/04_callbacks/index.html`をブラウザで開き、Consoleを確認します。

| 確認する出力 | 確認したいこと |
|---|---|
| `function`と`string` | `greet`は関数そのもの、`greet('a')`は呼び出した結果（文字列）であることがわかる |
| `1回目の呼び出し`〜`3回目の呼び出し` | `repeat()`に渡した関数が3回呼び出されている |

### 練習問題2：コールバック関数を書く

> 問題：[question/05_callbacks/index.html](question/05_callbacks/index.html)・[question/05_callbacks/script.js](question/05_callbacks/script.js) ｜ 解答：[question/answer/05_callbacks/index.html](question/answer/05_callbacks/index.html)・[question/answer/05_callbacks/script.js](question/answer/05_callbacks/script.js)

<details>
<summary>問題の内容を開く</summary>

`05_callbacks/script.js`の`TODO 1`・`TODO 2`を書きます。練習問題1と同じく、`05_callbacks/index.html`を開くとConsoleにテスト結果が表示されます。

| # | やること | 期待する結果 |
|---|---|---|
| 1 | `countIf(list, test)`：配列の各要素を「判定する関数」`test`に渡し、`true`が返ってきた要素の件数を返す（上の`repeat()`と同じく、受け取った関数を中で`test(item)`のように呼び出す。`forEach`と`let`の変数を使う） | `countIf([3, 8, 1, 6], (n) => n > 4)` → `2`、`countIf(items, (item) => item.pinned)` → `2` |
| 2 | `todayText`と`runSayHi`の2か所は、どちらも「関数そのもの」か「呼び出した結果」かを間違えている。`()`を足すか消すかして直す | `todayText` → `'2026-10-03'`、`runSayHi()`で`sayHi`がちょうど2回呼ばれる |

</details>

---

## 5. 発展：nullと真偽の判定

> [example/05_null_and_truthy/index.html](example/05_null_and_truthy/index.html) / [example/05_null_and_truthy/script.js](example/05_null_and_truthy/script.js)

この節は**発展**です。1〜4節で[06_js_dom_basics](../06_js_dom_basics/)に進む準備は整っているので、[08_js_forms](../08_js_forms/)の3節（発展）や[10_js_render](../10_js_render/)で`null`や真偽の判定が出てきたときに、ここへ戻ってきても構いません。

### `null`と`undefined`

```javascript
let notAssigned;
console.log(notAssigned);          // undefined（宣言しただけで、まだ値が入っていない）

const selected = null;             // 「まだ選ばれていない」ことを、意図的に表す
console.log(selected);             // null
// console.log(selected.title);    // TypeError：null のプロパティは読めない
```

| 値 | 意味 | よく出会う場面 |
|---|---|---|
| `undefined` | まだ値が入っていない | 宣言しただけの変数、存在しないプロパティ（`obj.lenght`のような打ち間違い） |
| `null` | 「無い」ことを意図的に表す値 | 「まだ選ばれていない」などを表す変数。次の[06_js_dom_basics](../06_js_dom_basics/)で、`getElementById()`が要素を見つけられなかったときに返す値としても出てくる |

#### 🐍 Pythonとの違い

Pythonの「値が無い」は`None`の1つだけですが、JavaScriptには**`null`と`undefined`の2つ**があります。

```python
# Python
memo = {'title': 'メモ'}
memo['body']        # KeyError：存在しないキーはエラーで止まる
memo.get('body')    # None
```

```javascript
// JavaScript
const memo = { title: 'メモ' };
memo.body;          // undefined：存在しないプロパティはエラーにならない
```

JavaScriptは存在しないプロパティを読んでも**エラーにならない**ので、打ち間違い（`lenght`）に気づきにくくなります。

### 真偽の判定：truthy と falsy

`if`の条件には、`true`/`false`以外の値も書けます。次の6つは**偽（falsy）**として扱われ、それ以外はすべて**真（truthy）**になります。

| falsy な値 | |
|---|---|
| `false`・`0`・`''`（空文字）・`null`・`undefined`・`NaN` | これ以外（`'0'`・`[]`・`{}`も含む）はすべて truthy |

```javascript
const selected = null;
if (selected) {
    // 値があるとき（null でないとき）だけ実行される
}

const text = '';
if (text) {
    // 1文字以上あるときだけ実行される（空文字は falsy）
}
```

値が truthy か falsy かは、`Boolean(値)`で`true`/`false`に変換して確かめられます（`Boolean('')` → `false`、`Boolean('0')` → `true`、`Boolean([])` → `true`）。

ページの要素を取得するメソッドも、要素が見つからないと`null`を返します（[06_js_dom_basics](../06_js_dom_basics/)）。複数のページで同じ`script.js`を読み込む制作課題のHP（[10_js_render](../10_js_render/)）では、`if (要素)`と書いて、「そのページに要素があるときだけ処理する」ようにします。

> 注意：Pythonでは空のリスト`[]`は偽ですが、JavaScriptの空の配列`[]`は**真**です。配列が空かどうかは`list.length === 0`で判定します。

#### 🐍 Pythonとの違い

| 値 | Python | JavaScript |
|---|---|---|
| `0` | 偽 | 偽 |
| `''`（空文字） | 偽 | 偽 |
| `None` / `null` / `undefined` | 偽 | 偽 |
| `NaN` | （なし） | 偽 |
| **`[]`（空の配列・リスト）** | **偽** | **真** |
| **`{}`（空の辞書・オブジェクト）** | **偽** | **真** |
| `'0'`（文字列の0） | 真 | 真 |

「空のリストを`if not items:`で判定する」Pythonの書き方は、そのままではJavaScriptで動きません。`items.length === 0`と書きます。

### `==`を使わない理由

```javascript
1 == '1';     // true （== は型を変換してから比べる）
1 === '1';    // false（=== は型も含めて比べる）
1 !== '1';    // true （!== は「等しくない」）
```

`==`は型を自動で変換するため思わぬ結果になります。**比較は常に`===`と`!==`を使います**。また、古いコードでは変数の宣言に`var`が使われていることがありますが、予期しない動きをしやすいため、今は`let`と`const`だけを使います。

#### 🐍 Pythonとの違い

Pythonの`==`は「値が等しいか」を、型の違う値同士では`False`として比べます。JavaScriptの`==`だけが、型を勝手に変換します。

| 式 | Python | JavaScript |
|---|---|---|
| `1 == '1'` | `False` | `true`（**型を変換するので**） |
| `1 === '1'` | （書けない） | `false` |
| `1 !== '1'` | （`!=`を使う） | `true` |

### 動作確認：コンソールに出力される値を確認する

| 確認する行 | 確認したいこと |
|---|---|
| 「1. null と undefined」の出力 | `undefined`→`null`の順に出力される |
| 「2. truthy と falsy」の出力 | `false`・`0`・空文字・`null`・`undefined`が`falsy`、`'a'`・`1`・`[]`・`{}`が`truthy`と出力され、最後に`値が無い（null）ので何もしない`・`空欄`と出力される |
| 「3. == は使わない」の出力 | `==`の3行はすべて`true`、`===`の2行は`false` |

### 練習問題3：何が出力されるか予想する

> 問題：[question/06_output_quiz/index.html](question/06_output_quiz/index.html)・[question/06_output_quiz/script.js](question/06_output_quiz/script.js) ｜ 解答：[question/answer/06_output_quiz/index.html](question/answer/06_output_quiz/index.html)・[question/answer/06_output_quiz/script.js](question/answer/06_output_quiz/script.js)

<details>
<summary>問題の内容を開く</summary>

3〜5節のまとめの問題です。`06_output_quiz/script.js`の10個の`console.log`（真偽の判定・`==`と`===`・`null`・関数とコールバック）の出力を、ブラウザで**開く前に**予想し、各行の「`// Q◯ 予想：`」の後ろに書き込みます。

| 確認する操作 | 確認したいこと |
|---|---|
| 予想を書き終えてから`06_output_quiz/index.html`を開き、Consoleを見る | 予想と実際の出力を比べる |
| 外れたものについて、4節・5節を読み直す | なぜその出力になるのかを説明できる |

</details>

---

## まとめ：Pythonとの対応表

この章で出てきたPythonとの違いを、一覧にまとめます。三項演算子・`&&`・`||`・`trim`などのPythonとの比較は[08_js_forms](../08_js_forms/)に、`map`/`filter`などは[10_js_render](../10_js_render/)にあります。Pythonは`02_backend/03_function`以降で本格的に使います。

| Python | JavaScript |
|---|---|
| `x = 1`（宣言なしの変数） | `let x = 1;` または `const x = 1;`（宣言が必要） |
| `None` | `null`（または`undefined`） |
| `==`（値の比較） | `===`（`==`は使わない） |
| `and` / `or` / `not` | `&&` / `\|\|` / `!`（[08_js_forms](../08_js_forms/)で学ぶ） |
| `True` / `False` | `true` / `false` |
| `[1, 2, 3]`（list） | `[1, 2, 3]`（配列） |
| `{"a": 1}`（dict） | `{ a: 1 }`（オブジェクト） |
| `d['a']` | `d.a`（または`d['a']`） |
| `len(x)` | `x.length` |
| `list.append(v)` | `list.push(v)` |
| `f"{name}さん"` | `` `${name}さん` ``（テンプレートリテラル） |
| `def f(a, b): return a + b` | `const f = (a, b) => a + b;`（アロー関数） |
| インデントでブロック | `{ }`でブロック |
| `elif` | `else if` |
| `for i in range(3):` | `for (let i = 0; i < 3; i++) { ... }` |
| `for x in list:` | `list.forEach((x) => { ... });` |
| `print(x)` | `console.log(x)` |
| `# コメント` | `// コメント` |
| 空のリスト`[]`は偽 | 空の配列`[]`は**真** |

---

## 次のステップ

続きは [06_js_dom_basics](../06_js_dom_basics/) です。JavaScriptでページの文字を書き換えるところから始め、[07_js_events](../07_js_events/)でボタンのクリックや入力に反応して、ブラウザ上で動くものを作ります。三項演算子や配列メソッドなどの残りの文法は、必要になったところで学びます。
