# 05 JavaScriptの基本文法

> フロントエンド編 ／ 前の章：[04_css_layout](../04_css_layout/) ／ 次の章：[06_js_events](../06_js_events/)

HTMLが「構造」、CSSが「見た目」を担当するのに対し、**JavaScript**はWebページの「動き」を担当する、ブラウザの中で動くプログラミング言語です。この章では、JavaScriptの読み込み方とデバッグの方法、変数・条件分岐・関数などの**最小限の基本文法**と、コールバック関数を学びます。

文法は、ここで一度に覚えようとしません。次の[06_js_events](../06_js_events/)でボタンのクリックなど**ブラウザ上で動くもの**を作り始め、三項演算子・`trim()`・配列メソッドなどの**残りの文法は、それが初めて必要になる章**（[06_js_events](../06_js_events/)・[08_js_render](../08_js_render/)）で学びます。

## 目次

0. [JavaScriptの読み込み方とデバッグ](#0-javascriptの読み込み方とデバッグ)
1. [JavaScript基本文法](#1-javascript基本文法)
2. [関数とコールバック](#2-関数とコールバック)

---

## フォルダ構成

```
01_frontend/05_js_basics/
├── README.md
├── example/                      サンプル（1つのサンプル＝1つのフォルダ）
│   ├── 00_first_click/           まず動かしてみる（ボタンを押すと文字が変わる）
│   │   └── index.html
│   ├── 01_js_basics/             JavaScript基本文法・null・真偽の判定・===
│   │   ├── index.html
│   │   └── script.js
│   └── 02_callbacks/             関数は値・コールバック関数
│       ├── index.html
│       └── script.js
└── question/                     練習問題（3問。問題文はREADMEの各節の最後）
    ├── 01_basic_functions/       練習問題1：基本文法で関数を書く
    │   ├── index.html
    │   └── script.js
    ├── 02_callbacks/             練習問題2：コールバック関数を書く
    │   ├── index.html
    │   └── script.js
    ├── 03_output_quiz/           練習問題3：何が出力されるか予想する
    │   ├── index.html
    │   └── script.js
    └── answer/                   解答（問題と同じ名前のフォルダ。中のファイル構成も問題と同じ）
        ├── 01_basic_functions/
        ├── 02_callbacks/
        └── 03_output_quiz/
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

ボタンを押すと、下に「JavaScriptが動きました！」と表示されます。これは、「ボタンが押されたら、段落の文字を書き換える」という、たった3行のプログラムです。**しくみは[06_js_events](../06_js_events/)で学びます**。まずはこの章で、このプログラムを書くための最小限の文法（変数・関数・`if`など）を身につけます。

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

存在しないプロパティを読んだとき（`value.lenght`のような打ち間違い）は、エラーにならず`undefined`になります。表示に`undefined`と出たら、プロパティ名を疑いましょう。06_js_events の練習問題1で、実際に探してみます。

---

## 1. JavaScript基本文法

> [example/01_js_basics/index.html](example/01_js_basics/index.html) / [example/01_js_basics/script.js](example/01_js_basics/script.js)

この先で使うJavaScriptの最低限の文法を確認します。ブラウザで開き、開発者ツールのコンソールで結果を確認してください。

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

### データ型とテンプレートリテラル

```javascript
const str = 'こんにちは';                    // 文字列
const num = 42;                              // 数値（整数と小数を区別しない）
const isDone = true;                         // 真偽値（true / false）
const list = [1, 2, 3];                      // 配列（Pythonのlistに相当）
const obj = { title: 'メモ', category: '仕事' };   // オブジェクト（Pythonのdictに相当）

// テンプレートリテラル：バッククォート(`)で ${式} を埋め込める（Pythonのf文字列に相当）
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

```javascript
// JavaScript
const memo = { title: 'メモ', category: '仕事' };   // オブジェクト
memo.title;                                          // 値の取り出しは . （memo['title'] も可）
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

### 関数（アロー関数）

```javascript
// function 宣言
function add(a, b) {
    return a + b;
}

// アロー関数（本章で多用する書き方）
const addArrow = (a, b) => {
    return a + b;
};

// 処理が1行だけなら {} と return を省略できる
const addShort = (a, b) => a + b;
```

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

### 条件分岐・繰り返し

```javascript
if (score >= 80) {
    console.log('合格');
} else if (score >= 50) {
    console.log('もう少し');
} else {
    console.log('不合格');
}

for (let i = 0; i < 3; i++) {
    console.log(`ループ ${i} 回目`);
}

// 配列を1件ずつ処理する（Pythonの for x in list: に相当）
categories.forEach((category) => {
    console.log(category);
});
```

#### 🐍 Pythonとの違い

```python
# Python
if score >= 80:
    print('合格')
elif score >= 50:
    print('もう少し')
else:
    print('不合格')

for i in range(3):
    print(f'ループ {i} 回目')

for category in categories:
    print(category)
```

| | Python | JavaScript |
|---|---|---|
| 条件の書き方 | `if score >= 80:`（`:`とインデント） | `if (score >= 80) { ... }`（**条件を`( )`で囲み、`{ }`でブロック**） |
| 「そうでなければ、もし」 | `elif` | `else if`（2語） |
| 回数を決めた繰り返し | `for i in range(3):` | `for (let i = 0; i < 3; i++) { ... }`（初期値；続ける条件；毎回の更新） |
| 配列を1件ずつ | `for x in list:` | `list.forEach((x) => { ... });` |
| 画面に出力 | `print(...)` | `console.log(...)`（ブラウザのConsoleに出る） |

`for (let i = 0; i < 3; i++)`は、「`i`を0から始め、`i < 3`の間、1回終わるごとに`i`を1増やす」という意味で、Pythonの`range(3)`に当たります。

### 演算子：`+=`・`++`

| 書き方 | 意味 | 例 |
|---|---|---|
| `a += b` | `a = a + b`の省略。`-=`・`*=`も同様 | `total += i;` |
| `a++` / `a--` | `a`を1増やす / 1減らす | `count++;` |

`&&`（かつ）・`||`（または）・`!`（でない）と、`条件 ? A : B`で値を選ぶ書き方は、フォームの入力チェックで初めて必要になる[06_js_events](../06_js_events/)で学びます。

#### 🐍 Pythonとの違い

| | Python | JavaScript |
|---|---|---|
| 1増やす | `count += 1`（`count++`は**書けない**） | `count += 1;` も `count++;` も書ける |
| 割り算 | `7 / 2` → `3.5`、`7 // 2` → `3` | `7 / 2` → `3.5`。整数にするには`Math.floor(7 / 2)`（`Math.floor`は[08_js_render](../08_js_render/)で学ぶ） |
| べき乗 | `2 ** 3` | `2 ** 3`（同じ） |

### 配列の長さと追加

| 書き方 | 説明 | 例 |
|---|---|---|
| `配列.length` / `文字列.length` | 要素の数 / 文字数 | `[1, 2, 3].length` → `3` |
| `配列.push(値)` | 配列の**最後**に追加する（元の配列が変わる） | `list.push('仕事')` |

配列を加工する`map`・`filter`・`find`・`includes`などは[08_js_render](../08_js_render/)で、文字列を加工する`trim`は[06_js_events](../06_js_events/)、`split`は[08_js_render](../08_js_render/)で学びます。

#### 🐍 Pythonとの違い

| やりたいこと | Python | JavaScript |
|---|---|---|
| 要素の数・文字数 | `len(x)` | `x.length`（**関数ではなくプロパティ**なので`()`を付けない） |
| 最後に追加 | `list.append(v)` | `list.push(v)` |

### `null`と`undefined`

```javascript
let notAssigned;
console.log(notAssigned);          // undefined（宣言しただけで、まだ値が入っていない）

const missing = document.getElementById('body');
console.log(missing);              // null（id="body" の要素が無い）
// console.log(missing.value);     // TypeError：null のプロパティは読めない
```

| 値 | 意味 | よく出会う場面 |
|---|---|---|
| `undefined` | まだ値が入っていない | 宣言しただけの変数、存在しないプロパティ（`obj.lenght`のような打ち間違い）、`find()`で見つからなかったとき |
| `null` | 「無い」ことを意図的に表す値 | `getElementById()`・`querySelector()`で要素が見つからなかったとき |

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
const bodyTextarea = document.getElementById('body');
if (bodyTextarea) {
    // 要素があるとき（null でないとき）だけ実行される
}

if (input.value) {
    // 1文字以上入力されているときだけ実行される（空文字は falsy）
}
```

値が truthy か falsy かは、`Boolean(値)`で`true`/`false`に変換して確かめられます（`Boolean('')` → `false`、`Boolean('0')` → `true`、`Boolean([])` → `true`）。

複数のページで同じ`script.js`を読み込むと（制作課題のHPのように）、ページによっては要素が無く`null`になります。`if (要素)`はこの性質を使った「要素があるときだけ処理する」書き方です。

> 注意：Pythonでは空のリスト`[]`は偽ですが、JavaScriptの空の配列`[]`は**真**です。配列が空かどうかは`list.length > 0`で判定します。

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

### 比較は`===`を使う

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

JavaScriptでは`==`を使わず、**`===`と`!==`だけ**を使います。

### まとめ：Pythonとの対応表

この節で出てきたPythonとの違いを、一覧にまとめます。三項演算子・`map`/`filter`・`trim`などのPythonとの比較は、それぞれを学ぶ[06_js_events](../06_js_events/)・[08_js_render](../08_js_render/)にあります。Pythonは`02_backend/03_function`以降で本格的に使います。

| Python | JavaScript |
|---|---|
| `x = 1`（宣言なしの変数） | `let x = 1;` または `const x = 1;`（宣言が必要） |
| `None` | `null`（または`undefined`） |
| `==`（値の比較） | `===`（`==`は使わない） |
| `and` / `or` / `not` | `&&` / `\|\|` / `!`（[06_js_events](../06_js_events/)で学ぶ） |
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

### 実行方法

`example/01_js_basics/index.html`をブラウザで直接開き、開発者ツール（`F12`または右クリック→検証）の「コンソール」タブで`console.log()`の出力を確認してください。

### 動作確認：コンソールに出力される値を確認する

| 確認する行 | 確認したいこと |
|---|---|
| `console.log(count, name);` | `2 メモ帳`と出力される（`let`で再代入した後の`count`の値が`2`になっている） |
| `console.log(message);` | `メモ帳には3件のメモがあります`と出力される（テンプレートリテラルで`${name}`・`${list.length}`が埋め込まれている） |
| `console.log(add(1, 2), addArrow(1, 2), addShort(1, 2));` | `3 3 3`と出力される（3つとも同じ結果を返す関数であることが分かる） |
| 条件分岐・for文・forEachの出力 | `合格` → `ループ 0 回目`〜`ループ 2 回目` → `家事`・`仕事`・`趣味`の順に出力される |
| `memos.length`（`push`の前後） | `2`→`3`と出力される（`push()`で配列に要素が増えた） |
| 「6. null と undefined」の出力 | `undefined`→`null`の順に出力される |
| 「7. 真偽の判定」の出力 | `false`・`0`・空文字・`null`・`undefined`が`falsy`、`'a'`・`1`・`[]`・`{}`が`truthy`と出力され、最後に`要素が無いので何もしない`・`空欄`と出力される（`truthy`/`falsy`は`if`/`else`で出力している） |
| 「8. 比較は === を使う」の出力 | `==`の3行はすべて`true`、`===`の2行は`false`、`!==`の行は`true` |

**正常な状態の見分け方**：コンソールに赤字のエラー（`Uncaught ReferenceError`など）が出ていなければ、上から順にすべての`console.log`が実行されています。途中で出力が止まっている場合は、それより前の行に文法ミスがないか確認してください。


### 練習問題1：基本文法で関数を書く

> 問題：[question/01_basic_functions/index.html](question/01_basic_functions/index.html)・[question/01_basic_functions/script.js](question/01_basic_functions/script.js) ｜ 解答：[question/answer/01_basic_functions/index.html](question/answer/01_basic_functions/index.html)・[question/answer/01_basic_functions/script.js](question/answer/01_basic_functions/script.js)

<details>
<summary>問題の内容を開く</summary>

`01_basic_functions/script.js`の`TODO 1`〜`TODO 6`の関数の中身を書きます。`01_basic_functions/index.html`を開くと、ファイルの一番下のテストが実行され、Consoleに ✅（正しい）／❌（間違い）が表示されます。❌のときは、結果と期待する値も表示されます。すべて ✅ になれば完成です。

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
| 4 | 空文字`''`は falsy。`text !== ''`の結果をそのまま`return`してもよいし、`if (text) { return true; }`と書いてもよい |
| 5 | 件数を入れる変数を`let`で用意し、`forEach`で1件ずつ見て、カテゴリが等しければ1増やす |
| 6 | 空の配列`[]`は truthy なので、`if (list)`では空かどうか判定できない |

</details>

---

## 2. 関数とコールバック

> [example/02_callbacks/index.html](example/02_callbacks/index.html) / [example/02_callbacks/script.js](example/02_callbacks/script.js)

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

これまでに出てきた`forEach`も、この後の`addEventListener`も、コールバック関数を受け取る関数です。

```javascript
memos.forEach((memo) => { ... });                   // 要素1つごとに呼び出してもらう
button.addEventListener('click', () => { ... });    // クリックされたときに呼び出してもらう
```

この「あとで呼び出してもらう関数を渡す」考え方は、`02_backend/03_function`でPythonのデコレータを学ぶときや、[10_js_data](../10_js_data/)の`fetch()`で通信の結果を受け取るときにも出てきます。

#### 🐍 Pythonとの違い

Pythonでも関数は値として渡せます（`sorted(items, key=len)`の`key`など）。書き方の違いは、無名関数の書き方です。

| | Python | JavaScript |
|---|---|---|
| 名前のある関数を渡す | `run(say_hi)` | `run(sayHi)`（どちらも`()`を付けない） |
| その場で作った関数を渡す | `run(lambda x: x * 2)`（式1つだけ） | `run((x) => x * 2)`（複数行の処理も書ける） |
| 呼び出した結果を渡す | `run(say_hi())` | `run(sayHi())`（意味も同じ。**間違いやすい**） |

### 動作確認：コンソールに出力される値を確認する

`example/02_callbacks/index.html`をブラウザで開き、Consoleを確認します。

| 確認する出力 | 確認したいこと |
|---|---|
| `function`と`string` | `greet`は関数そのもの、`greet('a')`は呼び出した結果（文字列）であることがわかる |
| `1回目の呼び出し`〜`3回目の呼び出し` | `repeat()`に渡した関数が3回呼び出されている |


### 練習問題2：コールバック関数を書く

> 問題：[question/02_callbacks/index.html](question/02_callbacks/index.html)・[question/02_callbacks/script.js](question/02_callbacks/script.js) ｜ 解答：[question/answer/02_callbacks/index.html](question/answer/02_callbacks/index.html)・[question/answer/02_callbacks/script.js](question/answer/02_callbacks/script.js)

<details>
<summary>問題の内容を開く</summary>

`02_callbacks/script.js`の`TODO 1`・`TODO 2`を書きます。練習問題1と同じく、`02_callbacks/index.html`を開くとConsoleにテスト結果が表示されます。

| # | やること | 期待する結果 |
|---|---|---|
| 1 | `countIf(list, test)`：配列の各要素を「判定する関数」`test`に渡し、`true`が返ってきた要素の件数を返す（上の`repeat()`と同じく、受け取った関数を中で`test(item)`のように呼び出す。`forEach`と`let`の変数を使う） | `countIf([3, 8, 1, 6], (n) => n > 4)` → `2`、`countIf(items, (item) => item.pinned)` → `2` |
| 2 | `todayText`と`runSayHi`の2か所は、どちらも「関数そのもの」か「呼び出した結果」かを間違えている。`()`を足すか消すかして直す | `todayText` → `'2026-10-03'`、`runSayHi()`で`sayHi`がちょうど2回呼ばれる |

</details>

### 練習問題3：何が出力されるか予想する

> 問題：[question/03_output_quiz/index.html](question/03_output_quiz/index.html)・[question/03_output_quiz/script.js](question/03_output_quiz/script.js) ｜ 解答：[question/answer/03_output_quiz/index.html](question/answer/03_output_quiz/index.html)・[question/answer/03_output_quiz/script.js](question/answer/03_output_quiz/script.js)

<details>
<summary>問題の内容を開く</summary>

1節・2節のまとめの問題です。`03_output_quiz/script.js`の10個の`console.log`（真偽の判定・`==`と`===`・要素が見つからないとき・関数とコールバック）の出力を、ブラウザで**開く前に**予想し、各行の「`// Q◯ 予想：`」の後ろに書き込みます。

| 確認する操作 | 確認したいこと |
|---|---|
| 予想を書き終えてから`03_output_quiz/index.html`を開き、Consoleを見る | 予想と実際の出力を比べる |
| 外れたものについて、1節・2節を読み直す | なぜその出力になるのかを説明できる |

</details>

---

## 次のステップ

続きは [06_js_events](../06_js_events/) です。ボタンのクリックや入力に反応して、ブラウザ上で動くものを作ります。三項演算子や配列メソッドなどの残りの文法は、必要になったところで学びます。
