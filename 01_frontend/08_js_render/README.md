# 08 配列メソッドと一覧の画面

> フロントエンド編 ／ 前の章：[07_js_dom](../07_js_dom/) ／ 次の章：[09_js_ui](../09_js_ui/)

実際のWebページの多くは、**配列のデータから一覧の画面を作ります**（メモ一覧・作品一覧など）。この章では、配列を扱う`map`・`filter`・`find`・`includes`と、「**データ（配列）を正しい状態として持ち、画面は毎回データから作り直す**」という考え方（`render()`）を学びます。最後に、一覧をボタンや検索欄で絞り込み、オリジナルHPに動き（ハンバーガーメニュー・一覧の絞り込み・お問い合わせの入力チェック）を付けます。

この考え方は、[10_js_data](../10_js_data/)の`localStorage`や`fetch()`、バックエンド編のメモ帳アプリ（`02_backend/02_memo_app_frontend`・`02_backend/100_memo_api`）でもそのまま使います。

## 前提

| チャプター | 使う知識 |
|---|---|
| 05_js_basics | 変数・関数・`forEach`・コールバック関数・`length`・`push` |
| 06_js_events | `getElementById`・`addEventListener`・`textContent`・`input`・`submit`・`trim()` |
| 07_js_dom | `createElement`・`append`・`dataset`・`hidden`・`querySelector` |

## 目次

1. [配列メソッド](#1-配列メソッド)
2. [データから画面を作る](#2-データから画面を作る)
3. [クライアント側での絞り込み](#3-クライアント側での絞り込み)
- [制作課題：オリジナルHP（ステップ3）](#制作課題オリジナルhpステップ3)

---

## フォルダ構成

```
01_frontend/08_js_render/
├── README.md
├── example/                      サンプル（1つのサンプル＝1つのフォルダ）
│   ├── 01_array_methods/         配列メソッド（map/filter/find/includes）
│   │   ├── index.html
│   │   └── script.js
│   ├── 02_render/                データから画面を作る（render()）
│   │   ├── index.html
│   │   └── script.js
│   └── 03_client_filter/         クライアント側での絞り込み
│       ├── index.html
│       └── script.js
├── question/                     練習問題（3問。問題文はREADMEの各節の最後）
│   ├── 01_array_methods/         練習問題1：配列メソッド
│   │   ├── index.html
│   │   └── script.js
│   ├── 02_memo_cards/            練習問題2：配列のデータからメモカードを作る
│   │   ├── index.html
│   │   └── script.js
│   ├── 03_tag_filter/            練習問題3：タグとキーワードの両方で絞り込む
│   │   ├── index.html
│   │   └── script.js
│   └── answer/                   解答（問題と同じ名前のフォルダ。中のファイル構成も問題と同じ）
│       ├── 01_array_methods/
│       ├── 02_memo_cards/
│       └── 03_tag_filter/
└── challenge/                    制作課題（オリジナルHP）ステップ3：HTML・CSSは完成済み、js/script.js にTODOを書く
    └── answer/                   完成例
```

---

## 1. 配列メソッド

> [example/01_array_methods/index.html](example/01_array_methods/index.html) / [example/01_array_methods/script.js](example/01_array_methods/script.js)

メモの一覧のような**オブジェクトの配列**を、「一部だけ取り出す」「別の形に変える」「1件探す」ために使うメソッドを学びます。いずれも、**関数（コールバック）を渡して**使います（[05_js_basicsの2節](../05_js_basics/#2-関数とコールバック)）。

| メソッド | 戻り値 | 用途 |
|---|---|---|
| `forEach(fn)` | なし | 1件ずつ「何かをする」（画面を書き換える・ログを出す） |
| `map(fn)` | 新しい配列 | 1件ずつ**変換**する（メモの配列 → タイトルの配列） |
| `filter(fn)` | 新しい配列 | 条件に合うものだけを**残す** |
| `find(fn)` | 1件（無ければ`undefined`） | 条件に合う**最初の1件**を探す |
| `includes(値)` | `true`/`false` | その値が含まれているか。文字列にも使える（部分一致の検索） |

```javascript
const titles = memos.map((memo) => memo.title);
const pinned = memos.filter((memo) => memo.pinned);
const memo3 = memos.find((memo) => memo.id === 3);
categories.includes('仕事');      // true
'企画会議メモ'.includes('会議');   // true

// つなげて書ける：「仕事」のメモのタイトルだけ
const workTitles = memos
    .filter((memo) => memo.category === '仕事')
    .map((memo) => memo.title);
```

`map`・`filter`は元の配列を変更せず、新しい配列を返します。

#### 🐍 Pythonとの違い

```python
# Python：内包表記や組み込み関数で書く
titles   = [m['title'] for m in memos]                       # map
pinned   = [m for m in memos if m['pinned']]                 # filter
memo3    = next((m for m in memos if m['id'] == 3), None)    # find
```

```javascript
// JavaScript：配列のメソッドをつなげて書く
const titles = memos.map((memo) => memo.title);
const pinned = memos.filter((memo) => memo.pinned);
const memo3 = memos.find((memo) => memo.id === 3);
```

| やりたいこと | Python | JavaScript |
|---|---|---|
| 1件ずつ変換 | `[f(x) for x in list]` | `list.map((x) => f(x))` |
| 条件で絞る | `[x for x in list if 条件]` | `list.filter((x) => 条件)` |
| 最初の1件を探す | `next((x for x in list if 条件), None)` | `list.find((x) => 条件)`（無ければ`undefined`） |
| 1件ずつ処理 | `for x in list:` | `list.forEach((x) => { ... })` |
| つなげる | 内包表記は入れ子にする | `.filter(...).map(...)`と**左から右へつなげる** |

Pythonは「内包表記」という専用の構文で書きますが、JavaScriptでは**関数（コールバック）を渡すメソッド**で書きます。


### 文字列・配列でよく使う操作（追加）

画面に表示するデータを扱うとき、次の操作もよく使います。

| 書き方 | 説明 | 例 |
|---|---|---|
| `配列.unshift(値)` | 配列の**先頭**に追加する（元の配列が変わる。最後に追加する`push`は05章） | `list.unshift('家事')` |
| `配列.indexOf(値)` | 値が何番目にあるか（0始まり）。**無ければ`-1`** | `['a', 'b'].indexOf('b')` → `1` |
| `文字列.slice(開始, 終了)` | 開始〜終了の手前までを取り出す | `'銀河鉄道'.slice(0, 2)` → `'銀河'` |
| `文字列.startsWith(文字)` | その文字で始まるか（`true`/`false`） | `'【済】買い物'.startsWith('【済】')` → `true` |
| `Math.floor(数値)` | 小数点以下を切り捨てる | `Math.floor(3.9)` → `3` |
| `Array.from(NodeList)` | `querySelectorAll`の結果（`NodeList`）を配列に変換する。`NodeList`には`indexOf`・`map`・`filter`が無い | `Array.from(document.querySelectorAll('.card'))` |

#### 🐍 Pythonとの違い

| やりたいこと | Python | JavaScript |
|---|---|---|
| 先頭に追加 | `list.insert(0, v)` | `list.unshift(v)` |
| 何番目か | `list.index(v)`（**無いとエラー**） | `list.indexOf(v)`（**無いと`-1`**。エラーにならない） |
| 一部を取り出す | `s[0:2]` | `s.slice(0, 2)` |
| 〜で始まるか | `s.startswith('a')` | `s.startsWith('a')`（`s`が大文字） |
| 切り捨て | `int(3.9)` / `math.floor(3.9)` | `Math.floor(3.9)` |
| 含まれるか | `'a' in s` / `x in list` | `s.includes('a')` / `list.includes(x)` |

JavaScriptのメソッド名は`camelCase`（`startsWith`のように2語目の頭が大文字）です。Pythonの`startswith`のように全部小文字で書くと、`is not a function`のエラーになります。

### 動作確認：コンソールに出力される値を確認する

`example/01_array_methods/index.html`をブラウザで開き、Consoleを確認します。

| 確認する出力 | 確認したいこと |
|---|---|
| `map`・`filter`・`find`の出力 | タイトルの配列、ピン留めの件数`2`、`読書メモ：銀河鉄道の夜`、見つからないときの`undefined` |
| `includes`の出力 | `true`・`false`（カテゴリの有無） |
| `workTitles` | `['企画会議メモ', '資料作成']`（`filter`と`map`をつなげた結果） |


### 練習問題1：配列メソッド

> 問題：[question/01_array_methods/index.html](question/01_array_methods/index.html)・[question/01_array_methods/script.js](question/01_array_methods/script.js) ｜ 解答：[question/answer/01_array_methods/index.html](question/answer/01_array_methods/index.html)・[question/answer/01_array_methods/script.js](question/answer/01_array_methods/script.js)

<details>
<summary>問題の内容を開く</summary>

`01_array_methods/script.js`の`TODO 1`〜`TODO 5`を書きます。05章の練習問題と同じく、`01_array_methods/index.html`を開くとConsoleにテスト結果が表示されます。

TODO 1〜4は`for`文を使わず、`map` / `filter` / `find` / `includes`で書きます。元の`memos`配列は変更しません。

| # | やること | 期待する結果 |
|---|---|---|
| 1 | `ids`：すべてのメモの`id`だけを並べた配列 | `[1, 2, 3, 4, 5]` |
| 2 | `pinnedCount`：ピン留め（`pinned`が`true`）のメモの件数 | `2` |
| 3 | `findMemo(id)`：`id`を受け取り、そのメモ（オブジェクト）を返す。無ければ`undefined` | `findMemo(3).title` → `'読書メモ：銀河鉄道の夜'` |
| 4 | `searchTitles(keyword)`：タイトルにキーワードを含むメモの「タイトルの配列」を返す（`filter`と`map`をつなげる。文字列にも`includes()`が使える） | `searchTitles('会議')` → `['企画会議メモ', '会議の議事録']` |
| 5 | `categories`：カテゴリの一覧（重複なし・登場順）。空の配列に、`forEach`で1件ずつ見て、まだ`includes()`されていないカテゴリだけ`push()`する | `['家事', '仕事', '趣味', 'プライベート']` |

</details>

---

## 2. データから画面を作る

> [example/02_render/index.html](example/02_render/index.html) / [example/02_render/script.js](example/02_render/script.js)

ボタンが押されるたびに画面の一部を直接書き換えていると、データと画面がずれるバグが起きやすくなります。そこで、**データ（配列）を正しい状態として持ち、画面は毎回データから作り直す**という考え方をします。

```
データ（配列）を用意する／変更する
   ↓
render() が呼ばれる → 一覧を空にして、配列から全部作り直す
   ↓
画面に表示される
```

```javascript
const memos = [ /* 画面の元になるデータ */ ];

const createCard = (memo) => {       // 1件分の要素を作って返す
    const li = document.createElement('li');
    li.className = 'card';
    li.textContent = memo.title;     // データは textContent で入れる（06章のXSS）
    return li;
};

const render = (items) => {          // 渡された配列から、一覧を作り直す
    list.textContent = '';           // いったん全部消して
    items.forEach((memo) => {        // データから作り直す
        list.append(createCard(memo));
    });
};

searchInput.addEventListener('input', () => {
    const matched = memos.filter((memo) => memo.title.includes(searchInput.value));
    render(matched);                 // 絞り込んだ配列を渡すだけ。画面の直し方は render() が知っている
});

render(memos);                       // 最初に全件を表示する
```

### ポイント

| 考え方 | 説明 |
|---|---|
| 「データ」と「画面」を分ける | 画面を直接直さず、データ（配列）を直して、`render()`を呼ぶ。データと画面がずれない |
| `createCard(memo)`は1件分だけ作る | 1件の作り方を1か所にまとめる。一覧は`forEach`で`createCard`を繰り返すだけ |
| `render(items)`は配列を引数にする | 全件でも絞り込んだ配列でも、同じ`render()`で表示できる |
| 作り直す前に`list.textContent = ''` | 空にしてから作り直さないと、前の表示に追加されて重複する |
| ユーザーが入力した文字は`textContent`で入れる | `innerHTML`にするとXSSの原因になる（[07_js_dom](../07_js_dom/#1-dom操作)） |

この考え方は、[10_js_data](../10_js_data/)で`localStorage`にデータを保存するときも、`fetch()`でデータを受け取るときも同じです（「データを変える→保存する→`render()`する」）。

### 動作確認

`example/02_render/index.html`をブラウザで開いて確認します。

| 確認する操作 | 確認したいこと |
|---|---|
| ページを開く | 4件のカードが表示され、「4件表示中」と出る |
| 検索欄に「メモ」と入力する | タイトルに「メモ」を含む2件になり、「2件表示中」になる |
| 検索欄を空にする | 4件すべてに戻る |
| Elementsパネルを見ながら入力する | 入力のたびに`ul`の中身がまとめて作り直されている |

### 練習問題2：配列のデータからメモカードを作る

> 問題：[question/02_memo_cards/index.html](question/02_memo_cards/index.html)・[question/02_memo_cards/script.js](question/02_memo_cards/script.js) ｜ 解答：[question/answer/02_memo_cards/index.html](question/answer/02_memo_cards/index.html)・[question/answer/02_memo_cards/script.js](question/answer/02_memo_cards/script.js)

<details>
<summary>問題の内容を開く</summary>

`02_memo_cards/script.js`の`memos`配列の5件を、カードとして表示します。`TODO 1`〜`TODO 4`を書きます。

| # | やること | ヒント |
|---|---|---|
| 1 | `createCard(memo)`：メモ1件分のカード要素を作って返す。構造は下のとおり（📌は`pinned`が`true`のときだけ） | `document.createElement()` / `要素.className` / `要素.textContent` / `要素.append()`。タイトルは`textContent`で入れる（`innerHTML`は使わない） |
| 2 | `render(items)`：渡された配列のメモをすべて表示する。`list`の中身を空にし、各メモを`createCard()`して`list`に追加し、`shownCount`に「◯件表示中」と表示する | `list.textContent = '';`で子要素をすべて消せる |
| 3 | ピン留めの件数を`pinnedCount`に「ピン留め：◯件」と表示する | `filter()`で`pinned`が`true`のものだけにして、`length`を数える |
| 4 | 検索欄に入力するたびに、タイトルに入力文字を含むメモだけを`render()`する | `'input'`イベント / `searchInput.value` / `文字列.includes()`。空欄のときは`includes('')`が常に`true`になるので、特別扱いしなくても全件表示になる |

```html
<li class="card">
    <span class="tag">家事</span>
    <span class="pin">📌</span>      <!-- pinned が true のときだけ -->
    <h2>買い物リスト</h2>
</li>
```

| 確認する操作 | 確認したいこと |
|---|---|
| ページを開く | 5件のカードが表示され、「ピン留め：2件 ／ 5件表示中」と表示される |
| 検索欄に「リスト」と入力する | 「買い物リスト」「旅行の持ち物リスト」の2件だけになり、「2件表示中」になる |
| 検索欄を空にする | 5件すべてに戻る |

</details>

---

## 3. クライアント側での絞り込み

> [example/03_client_filter/index.html](example/03_client_filter/index.html) / [example/03_client_filter/script.js](example/03_client_filter/script.js)

この先の`02_backend/08_request`では、`request.args`を使ってサーバー（Flask）側でデータを絞り込む方法を学びます。ここでは同じ「絞り込み」を、**サーバーに問い合わせずJavaScriptだけ**で行います。

```javascript
const buttons = document.querySelectorAll('.filters button');
const cards = document.querySelectorAll('.card');

buttons.forEach((button) => {
    button.addEventListener('click', () => {
        buttons.forEach((b) => b.classList.remove('active'));
        button.classList.add('active');

        const selected = button.dataset.category;   // data-category="..." の値を取得

        cards.forEach((card) => {
            const match = selected === 'all' || card.dataset.category === selected;
            card.classList.toggle('hidden', !match);
        });
    });
});
```

### ポイント

| 要素・メソッド | 説明 |
|---|---|
| `document.querySelectorAll('.card')` | 条件に一致する要素を**すべて**取得する（`NodeList`が返る） |
| `NodeList.forEach(関数)` | 取得した要素それぞれに対して処理を行う |
| `要素.dataset.category` | `data-category="..."`のようなカスタム属性の値を取得する |

### 複数の値を持つ属性：`split()`

1つの要素が複数のタグを持つときは、`data-tags="HTML CSS"`のように空白で区切って書き、JavaScriptで配列に分けて調べます。

```javascript
const tags = card.dataset.tags.split(' ');   // 'HTML CSS' → ['HTML', 'CSS']
tags.includes('CSS');                        // true
```

| 書き方 | 説明 |
|---|---|
| `文字列.split(区切り)` | 区切り文字で分けた配列にする（`'HTML CSS'.split(' ')` → `['HTML', 'CSS']`） |
| `配列.includes(値)` | その値を含むか（1節） |
| `要素.hidden = true / false` | 表示・非表示の切り替え（[07_js_domの道具箱](../07_js_dom/#道具箱必要になったときに見る)） |

Pythonの`'HTML CSS'.split(' ')`と同じ書き方です。

### サーバー側の絞り込みとの違い

| | サーバー側（`02_backend/08_request`で学ぶ） | クライアント側（本章） |
|---|---|---|
| 絞り込みの実行場所 | Flask（Python） | ブラウザ（JavaScript） |
| ページの再読み込み | 発生する（新しいHTMLを受け取る） | 発生しない（今のページのまま） |
| 向いている場面 | データ件数が多い・全件を一度に送りたくない | 表示中のデータの中で切り替えたいだけ |

### 実行方法

`example/03_client_filter/index.html`をブラウザで直接開いてください（Flask不使用）。カテゴリボタンをクリックすると、ページ全体が再読み込みされずにカードの表示・非表示だけが切り替わることを確認できます。

### 動作確認：クリックしたカテゴリだけ表示されるか

| 確認する操作 | 確認したいこと |
|---|---|
| 初期表示を確認する | 「すべて」ボタンが`active`（青背景）になっており、4件のカードがすべて表示されている |
| 「仕事」ボタンをクリックする | 「仕事」ボタンだけが`active`になり、`data-category="仕事"`の2枚（企画会議メモ・資料作成）だけが残り、他の2枚（買い物リスト・読書メモ）が非表示になる |
| 続けて「趣味」ボタンをクリックする | 表示が切り替わり、「読書メモ」1枚だけが表示される（前に選んだ「仕事」の`active`は自動的に外れる） |
| 「すべて」ボタンをクリックする | 4枚のカードがすべて再表示される |
| 操作中にページ全体が再読み込みされていないか確認する | 再読み込みは発生しない（ブラウザのタブのリロードアイコンが回らない、スクロール位置も保持される） |

**正常な状態の見分け方**：クリックのたびに「押したボタンだけが`active`」「そのカテゴリに一致するカードだけが表示」の2つが同時に成立していれば正常です。片方だけ変化する場合は、`buttons.forEach`または`cards.forEach`のどちらか一方しか正しく動いていない可能性があります。


### 練習問題3：タグとキーワードの両方で絞り込む

> 問題：[question/03_tag_filter/index.html](question/03_tag_filter/index.html)・[question/03_tag_filter/script.js](question/03_tag_filter/script.js) ｜ 解答：[question/answer/03_tag_filter/index.html](question/answer/03_tag_filter/index.html)・[question/answer/03_tag_filter/script.js](question/answer/03_tag_filter/script.js)

<details>
<summary>問題の内容を開く</summary>

作品一覧を、タグのボタンとキーワードの検索欄の**両方**で絞り込みます。[example/03_client_filter](example/03_client_filter/index.html)との違いは、1つの作品が複数のタグを持つこと（`data-tags="HTML CSS"`のように空白区切り）と、2つの条件を両方満たす作品だけを表示することです。

| # | 仕様 |
|---|---|
| 1 | タグのボタンを押すと、押したボタンだけ`active`クラスを付け、他のボタンからは外す（CSSで`.filters button.active`が青くなる） |
| 2 | 選ばれているタグを持つ作品だけを表示する。「すべて」（`data-tag="all"`）なら全件 |
| 3 | 検索欄に入力するたびに、タイトル（`h3`の文字）にキーワードを含む作品だけを表示する |
| 4 | 2と3は組み合わせて働く（例：「JavaScript」を選んで「アプリ」と入力→「メモ帳アプリ」「タイピングアプリ」だけ） |
| 5 | `#count`に「◯件表示中」と表示する。0件のときは`#empty`（「該当する作品はありません」）を表示する |

`03_tag_filter/script.js`には次の3つを書きます。

| # | やること | ヒント |
|---|---|---|
| 1 | `applyFilter()`：今の条件（`selectedTag`と検索欄の文字）で、作品の表示・非表示を切り替え、件数と0件のメッセージを更新する関数 | `'HTML CSS'.split(' ')`→`['HTML', 'CSS']`。`要素.dataset.tags`・`要素.querySelector('h3')`。表示・非表示は`要素.hidden = true / false` |
| 2 | タグのボタンが押されたら、`active`クラスを付け替え、`selectedTag`を押したボタンの`data-tag`の値にして`applyFilter()`を呼ぶ | |
| 3 | 検索欄に入力するたびに`applyFilter()`を呼ぶ | |

| 確認する操作 | 確認したいこと |
|---|---|
| 「Python」を押す | 「メモ帳アプリ」「蔵書管理ツール」の2件 |
| そのまま検索欄に「蔵書」と入力する | 「蔵書管理ツール」の1件 |
| 検索欄に「ゲーム」と入力する | 0件になり、「該当する作品はありません」が表示される |
| 「すべて」を押して検索欄を空にする | 6件すべて |

</details>

---

## 制作課題：オリジナルHP（ステップ3）

> [challenge/](challenge/) — 雛形 ｜ [challenge/answer/](challenge/answer/) — 完成例 ｜ 自分のHP：[00_my_homepage/](../00_my_homepage/)

ステップ2までで作ったHPに、`js/script.js`を作って動きを付けます。全ページで同じ`script.js`を読み込み、`if (要素)`で「そのページにある要素だけ」を操作します（05_js_basics 1節の「真偽の判定」）。

制作課題は、毎回次の2段階で進めます。

1. **`challenge/`で練習する**：架空の人物「山田 太郎」のサイトを題材に、ファイルの中のTODOコメントに沿って書きます。書けたら`challenge/answer/`の完成例と見比べます。
2. **自分のHPに反映する**：同じことを、[00_my_homepage/](../00_my_homepage/)の自分のサイトに行います。こちらは文章・配色・レイアウトを自分で考えて作ります。下の「必須要件」は、自分のHPで満たすべき要件です。

### challenge/ の内容

| ファイル | 内容 |
|---|---|
| `*.html` | 04_css_layoutの完成例に、☰ボタン（`#nav-toggle`）・絞り込みボタン（`#filters`）・各入力欄のエラー表示（`<p class="error" id="name-error">`など）・送信後のメッセージ（`#contact-result`）・`<script src="js/script.js">`を足したもの（完成済み） |
| `css/style.css` | 上の要素のスタイル（`.nav-links.open`・`.filters button.active`・`.work-card.hidden`・`.invalid`など）を追加済み |
| `js/script.js` | TODO 1〜3（ハンバーガーメニュー・制作実績の絞り込み・お問い合わせの入力チェック）を書く |

### 必須要件

| 要件 | 使う節 |
|---|---|
| 全ページで`js/script.js`を`</body>`の直前で読み込む | 05_js_basics 0 |
| **ハンバーガーメニュー**：狭い画面ではナビゲーションを折りたたみ、☰ボタンで開閉する | 06_js_events 1、07_js_dom 1 |
| **一覧の絞り込み**：制作実績（または好きなもの紹介）をカテゴリやタグで絞り込むボタンを付ける。タグが複数ある項目は`data-tags="HTML/CSS JavaScript"`のように空白区切りで持たせ、`split(' ')`と`includes()`で判定する | 1（`includes`）・3（`split`・`hidden`） |
| **お問い合わせの入力チェック**：`submit`で入力をチェックし、問題があれば各欄の下にエラーを表示する。問題が無ければ「送信しました」などのメッセージを表示する（静的なサイトなので、送信自体は`preventDefault()`で止める） | 06_js_events 3 |
| すべてのページを操作しても、Consoleに赤字のエラーが出ない | 05_js_basics 0 |

### 自由課題（1つ以上）

必須要件に加えて、自分のサイトに合う動きを1つ以上考えて付けてみましょう。

| 例 | ヒント |
|---|---|
| ページ上部へ戻るボタン | 300pxスクロールしたら表示し、`window.scrollTo({ top: 0, behavior: 'smooth' })`で戻る（09_js_ui 5節） |
| ダークモードの切り替えボタン | `document.body.classList.toggle('dark')`と、`.dark`のときだけCSS変数を差し替えるCSS |
| よくある質問の開閉 | 質問をクリックしたら、答えの要素に`open`クラスを付け外しする |
| 今日の日付やあいさつの表示 | `new Date().getHours()`で時間帯によってメッセージを変える |
| プロフィールをタブで切り替える | 「基本情報」「スキル」「経歴」をタブにする（09_js_ui 1節） |
| 作品の詳細をモーダルウィンドウで表示する | 作品カードをクリックすると`<dialog>`で詳しい説明を出す（09_js_ui 3節） |
| ホームで作品をスライドショーにする | 前へ・次へと自動再生。ホバー中は止める（09_js_ui 4節） |
| スクロールで要素をふわっと表示する | `IntersectionObserver`で画面に入ったらクラスを付ける（09_js_ui 5節） |
| お問い合わせの送信後に通知を出す | `popover="manual"`と`setTimeout`で、数秒で消える通知（09_js_ui 2節） |
| ナビやボタンにツールチップを付ける | `mouseenter`・`focus`で説明を表示する（06_js_events 3節） |

### 進め方のヒント

1. まずハンバーガーメニューを作る。全ページに効くので、動けばすぐ実感できる
2. 絞り込みは、HTMLの各項目に`data-tags`を付けるところから始める
3. 入力チェックは、[06_js_eventsの練習問題2](../06_js_events/#練習問題2フォームの送信前に入力をチェックする)がそのまま使える
4. [challenge/answer/js/script.js](challenge/answer/js/script.js)と比べる

### 動作確認：challenge/

| 確認する操作 | 確認したいこと |
|---|---|
| 幅375pxで☰を押す | メニューが開閉する |
| `works.html`で「Python」を押す | 「メモ帳アプリ」「蔵書管理ツール」の2件だけが残る |
| `contact.html`で何も入力せずに送信する | 3つの欄の下にエラーが表示され、枠が赤くなる。正しく入力すると、お礼のメッセージが表示される |
| すべてのページでConsoleを見る | 赤字のエラーが出ていない |

## 次のステップ

続きは [09_js_ui](../09_js_ui/) です。タブ・ポップアップ・モーダルウィンドウ・スライドショー・スクロール動作など、よく使うUIを作ります。
