# 019 JavaScriptによる機能追加

`018_ownership_crud`まではPython（Flask）側でHTMLを組み立て、ページ全体を再読み込みする方式で操作を行ってきました。このチャプターでは初めて**JavaScript**を使い、ページを再読み込みせずに操作できる機能をメモ帳アプリに追加します。基本文法の確認から、DOM操作、サーバーとJSONをやり取りする`fetch()`まで、段階的に学びます。

## 前提

| チャプター | 使う知識 |
|---|---|
| 002_html_css | HTML/CSSの基礎（`id`・`class`セレクタ） |
| 018_ownership_crud | メモ帳アプリ本体（所有権・CRUD） |

## 目次

1. [JavaScript基本文法](#1-javascript基本文法) — 変数・データ型・関数・条件分岐・配列とオブジェクト
2. [DOM操作の基本](#2-dom操作の基本) — 要素の取得・書き換え・イベント
3. [クライアント側での絞り込み](#3-クライアント側での絞り込み) — ページ再読み込みなしの表示切り替え
4. [fetch()の基本](#4-fetchの基本) — サーバーとJSONをやり取りする
5. [練習問題](#5-練習問題メモ帳アプリにjavascriptで機能を追加しよう) — 000_my_appへの機能追加

---

## フォルダ構成

```
019_javascript/
├── README.md
├── example/
│   ├── 01_js_basics.html        JavaScript基本文法（Flask不使用）
│   ├── 01_js_basics.js
│   ├── 02_dom_basics.html       DOM操作の基本（文字数カウンター、Flask不使用）
│   ├── 02_dom_basics.js
│   ├── 03_client_filter.html    クライアント側での絞り込み（Flask不使用）
│   ├── 03_client_filter.js
│   └── 04_fetch_basics/         fetch()の基本（GET表示 + POSTでお気に入りトグル）
│       ├── app.py
│       ├── static/script.js
│       └── templates/index.html
└── challenge/                   018_ownership_crudの続き（000_my_appに組み込む機能の変更分）
    ├── app.py / models.py / ...    メモ帳アプリのアプリ本体（is_pinnedカラム・toggle-pinルートは実装済み）
    ├── static/
    │   ├── style.css
    │   └── script.js                TODOコメントの箇所にJavaScriptを書く
    └── answer/
        └── app.py / models.py / ...   example/app/ と同じ完成版
```

---

## 1. JavaScript基本文法

> [example/01_js_basics.html](example/01_js_basics.html) / [example/01_js_basics.js](example/01_js_basics.js)

Pythonとの対応を意識しながら、この先で使うJavaScriptの最低限の文法を確認します。ブラウザで開き、開発者ツールのコンソールで結果を確認してください。

### 変数：let と const

```javascript
let count = 1;
count = 2;   // let は再代入できる

const name = 'メモ帳';
// name = '別の名前';   // const は再代入できないのでエラーになる
```

Pythonでは`x = 1`だけで変数が使えますが、JavaScriptでは`let`か`const`が必要です。何が変わるか分からない場合はまず`const`を使い、再代入が必要になったら`let`に変えるのが一般的です。

### データ型とテンプレートリテラル

```javascript
const str = 'こんにちは';                    // 文字列
const num = 42;                              // 数値（整数もfloatも区別しない）
const isDone = true;                         // 真偽値（true / false）
const list = [1, 2, 3];                      // 配列（Pythonのlistに相当）
const obj = { title: 'メモ', category: '仕事' };   // オブジェクト（Pythonのdictに相当）

// テンプレートリテラル：バッククォート(`)で ${式} を埋め込める（Pythonのf文字列に相当）
const message = `${name}には${list.length}件のメモがあります`;
```

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

### Pythonとの対応

| Python | JavaScript |
|---|---|
| `x = 1`（変数） | `let x = 1;` または `const x = 1;` |
| `True` / `False` | `true` / `false` |
| `[1, 2, 3]`（list） | `[1, 2, 3]`（配列） |
| `{"a": 1}`（dict） | `{ a: 1 }`（オブジェクト） |
| `f"{name}さん"` | `` `${name}さん` ``（テンプレートリテラル） |
| `def f(a, b): return a + b` | `const f = (a, b) => a + b;`（アロー関数） |
| `for x in list:` | `list.forEach((x) => { ... });` |
| `[x for x in list if 条件]` | `list.filter((x) => 条件)` |

### 実行方法

`example/01_js_basics.html`をブラウザで直接開き、開発者ツール（`F12`または右クリック→検証）の「コンソール」タブで`console.log()`の出力を確認してください。

### 動作確認：コンソールに出力される値を確認する

| 確認する行 | 確認したいこと |
|---|---|
| `console.log(count, name);` | `2 メモ帳`と出力される（`let`で再代入した後の`count`の値が`2`になっている） |
| `console.log(message);` | `メモ帳には3件のメモがあります`と出力される（テンプレートリテラルで`${name}`・`${list.length}`が埋め込まれている） |
| `console.log(add(1, 2), addArrow(1, 2), addShort(1, 2));` | `3 3 3`と出力される（3つとも同じ結果を返す関数であることが分かる） |
| 条件分岐・for文・forEachの出力 | `合格` → `ループ 0 回目`〜`ループ 2 回目` → `家事`・`仕事`・`趣味`の順に出力される |
| `console.log(workMemos);` | `category`が`'仕事'`の要素だけが残った配列（`[{ id: 2, title: '企画会議メモ', category: '仕事' }]`）が出力される（`filter()`の効果） |

**正常な状態の見分け方**：コンソールに赤字のエラー（`Uncaught ReferenceError`など）が出ていなければ、上から順にすべての`console.log`が実行されています。途中で出力が止まっている場合は、それより前の行に文法ミスがないか確認してください。

---

## 2. DOM操作の基本

> [example/02_dom_basics.html](example/02_dom_basics.html) / [example/02_dom_basics.js](example/02_dom_basics.js)

JavaScriptからHTML要素を取得し、内容を書き換える基本を、文字数カウンターを題材に学びます。

```javascript
// 1. document.getElementById() で要素を取得する
const textarea = document.getElementById('body');
const counter = document.getElementById('count');

// 2. addEventListener() でイベント（入力のたびに発火する 'input'）を監視する
textarea.addEventListener('input', () => {
    const length = textarea.value.length;

    // 3. textContent を書き換えると画面表示が更新される
    counter.textContent = length;

    // 4. classList.toggle() で条件に応じてCSSクラスを付け外しする
    counter.classList.toggle('over', length > 450);
});
```

### ポイント

| 要素・メソッド | 説明 |
|---|---|
| `document.getElementById('id')` | `id`属性が一致する要素を1つ取得する |
| `要素.addEventListener('input', 関数)` | 入力のたびに関数を実行する（クリックなら`'click'`） |
| `要素.textContent` | 要素の中のテキストを取得・書き換える |
| `要素.classList.toggle('クラス名', 条件)` | 条件が`true`ならクラスを付け、`false`なら外す |

### 実行方法

`example/02_dom_basics.html`をブラウザで直接開いてください（Flask不使用）。入力するたびに文字数が更新され、450文字を超えると赤字になることを確認できます。

### 動作確認：入力に応じてカウンターが更新されるか

| 確認する操作 | 確認したいこと |
|---|---|
| テキストエリアに1文字入力する | `0 / 500文字`の`0`が`1`に変わる（`input`イベントのたびに`textContent`が書き換わる） |
| 文字を消していく（Backspace） | 文字数の表示もリアルタイムに減っていく |
| 450文字を超える文章を貼り付ける | 451文字目に達した瞬間、文字数の表示が赤字になる（`classList.toggle('over', length > 450)`） |
| 451文字以上の状態から文字を消して450文字以下に戻す | 赤字が元の色（グレー）に戻る（`toggle`は条件が`false`になるとクラスを自動で外す） |
| `textarea`の`maxlength="500"`を超えて入力しようとする | それ以上は入力できない（ブラウザの`maxlength`属性による制限で、JavaScriptのコードとは別の仕組み） |

**正常な状態の見分け方**：文字数の表示が「今テキストエリアに実際に入っている文字数」と常に一致していれば正常です。ズレている場合は`textarea.value.length`の取得タイミングやイベント名（`'input'`か`'change'`か）を疑ってください。

---

## 3. クライアント側での絞り込み

> [example/03_client_filter.html](example/03_client_filter.html) / [example/03_client_filter.js](example/03_client_filter.js)

`008_request`では`request.args`を使ってサーバー側でデータを絞り込みました。ここでは同じ「絞り込み」を、**サーバーに問い合わせずJavaScriptだけ**で行います。

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

### サーバー側の絞り込みとの違い

| | サーバー側（008_request） | クライアント側（本章） |
|---|---|---|
| 絞り込みの実行場所 | Flask（Python） | ブラウザ（JavaScript） |
| ページの再読み込み | 発生する（新しいHTMLを受け取る） | 発生しない（今のページのまま） |
| 向いている場面 | データ件数が多い・全件を一度に送りたくない | 表示中のデータの中で切り替えたいだけ |

### 実行方法

`example/03_client_filter.html`をブラウザで直接開いてください（Flask不使用）。カテゴリボタンをクリックすると、ページ全体が再読み込みされずにカードの表示・非表示だけが切り替わることを確認できます。

### 動作確認：クリックしたカテゴリだけ表示されるか

| 確認する操作 | 確認したいこと |
|---|---|
| 初期表示を確認する | 「すべて」ボタンが`active`（青背景）になっており、4件のカードがすべて表示されている |
| 「仕事」ボタンをクリックする | 「仕事」ボタンだけが`active`になり、`data-category="仕事"`の2枚（企画会議メモ・資料作成）だけが残り、他の2枚（買い物リスト・読書メモ）が非表示になる |
| 続けて「趣味」ボタンをクリックする | 表示が切り替わり、「読書メモ」1枚だけが表示される（前に選んだ「仕事」の`active`は自動的に外れる） |
| 「すべて」ボタンをクリックする | 4枚のカードがすべて再表示される |
| 操作中にページ全体が再読み込みされていないか確認する | 再読み込みは発生しない（ブラウザのタブのリロードアイコンが回らない、スクロール位置も保持される） |

**正常な状態の見分け方**：クリックのたびに「押したボタンだけが`active`」「そのカテゴリに一致するカードだけが表示」の2つが同時に成立していれば正常です。片方だけ変化する場合は、`buttons.forEach`または`cards.forEach`のどちらか一方しか正しく動いていない可能性があります。

---

## 4. fetch()の基本

> [example/04_fetch_basics/app.py](example/04_fetch_basics/app.py) / [example/04_fetch_basics/static/script.js](example/04_fetch_basics/static/script.js)

`fetch()`は、JavaScriptからHTTPリクエストを送るための組み込み関数です。Pythonの`requests`（`022_webapi`で後ほど学習します）とよく似た役割を、ブラウザの中で果たします。

```javascript
document.querySelectorAll('.like').forEach((button) => {
    button.addEventListener('click', async () => {
        const li = button.closest('li');
        const itemId = li.dataset.id;

        // fetch(URL, {method: ...}) でPOSTリクエストを送る
        const response = await fetch(`/api/items/${itemId}/toggle-like`, {
            method: 'POST',
        });

        // response.json() でレスポンス本文をJSONとして受け取る（Promiseなのでawaitする）
        const data = await response.json();

        // サーバーから返ってきた最新の状態でボタンの表示だけを書き換える
        button.textContent = data.liked ? '★' : '☆';
    });
});
```

### async / await とは

`fetch()`は結果がすぐには返ってこない（通信が終わるまで待つ必要がある）ため、`Promise`というオブジェクトを返します。関数に`async`を付けると、その中で`await`を使って「`Promise`の結果が返ってくるまで待つ」という書き方ができます。

| キーワード | 役割 |
|---|---|
| `async 関数`| 関数の中で`await`を使えるようにする |
| `await 式` | `Promise`の結果が返ってくるまで待ってから次の行に進む |

### requests（Python）とfetch()（JavaScript）の対応

| | Python（`requests`） | JavaScript（`fetch()`） |
|---|---|---|
| GETリクエスト | `requests.get(url)` | `await fetch(url)` |
| POSTリクエスト | `requests.post(url, json=data)` | `await fetch(url, {method: 'POST', body: JSON.stringify(data)})` |
| レスポンスをJSONとして取得 | `res.json()` | `await res.json()` |

### 実行方法

```bash
python 019_javascript/example/04_fetch_basics/app.py
```

ブラウザで`http://127.0.0.1:5073/`にアクセスし、☆をクリックすると★に変わり（もう一度クリックすると☆に戻る）、ページが再読み込みされないことを確認してください。

### 動作確認：ページを再読み込みせずに状態が変わるか

| 確認する操作 | 確認したいこと |
|---|---|
| `http://127.0.0.1:5073/`にアクセスする | 「紅茶」だけが★、他の2件（コーヒー・ジュース）が☆になっている（`items`の初期データ通り） |
| コーヒーの☆をクリックする | クリックした瞬間に★へ変わる。ページの再読み込みは発生しない（タブのリロードアイコンが回らない） |
| 開発者ツールの「Network」タブを開いた状態でもう一度クリックする | `toggle-like`への**POSTリクエストが1件だけ**記録される。ページ全体を取得し直す`GET /`のリクエストは発生しない |
| ★になったコーヒーをもう一度クリックする | ☆に戻る（サーバー側の`item['liked'] = not item['liked']`で反転している） |
| クリックした状態のまま、ブラウザをリロード（F5）する | クリック後の状態（★/☆）がそのまま表示される。`items`はサーバー側のプロセスに保持されているため、`GET /`をやり直しても最新の状態が返る |
| `app.py`を再起動してから同じページを開く | 状態が初期値（紅茶だけ★）に戻る。`items`はただのPythonのリストなのでサーバーの再起動でリセットされることが確認できる |

**正常な状態の見分け方**：クリック直後に星の表示だけが変わり、ページ全体はそのまま（スクロール位置などが保持される）であれば正常です。星が変わらない、または画面全体が一瞬白くなってから表示される場合は、`fetch()`ではなく通常の`<a>`や`<form>`の送信が起きてしまっている可能性があります。

---

## 5. 練習問題：メモ帳アプリにJavaScriptで機能を追加しよう

> [challenge/static/script.js](challenge/static/script.js) — 問題 ｜ [challenge/answer/static/script.js](challenge/answer/static/script.js) — 解答

### 問題：3つのJavaScript機能を実装しよう

`018_ownership_crud`で作ったメモ一覧・詳細・追加・編集・削除・認証の機能はそのままです（`challenge/`にすでに実装済み）。今回はPython側の変更はなく、`static/script.js`のTODOコメントの箇所にJavaScriptを書いて完成させます。

```bash
cd 019_javascript/challenge
flask db init
flask db migrate -m "create users and memos tables"
flask db upgrade
python app.py
```

#### 仕様

| 問題 | 内容 |
|---|---|
| 1 | メモ追加・編集ページの本文`textarea`（`#body`）に入力するたびに、`#body-count`の文字数表示を更新する。500文字を超えたら`over`クラスを付けて赤字にする |
| 2 | メモ一覧ページのカテゴリボタン（`.filters button`）をクリックしたら、選択中のボタンに`active`クラスを付け、一致しないカード（`.card`）に`hidden`クラスを付けて非表示にする |
| 3 | メモ一覧ページのピンボタン（`.pin-button`）をクリックしたら、`fetch()`で`/memos/<id>/toggle-pin`にPOSTし、返ってきたJSONの`is_pinned`に応じてボタンの表示（★/☆）を書き換える |

#### ヒント

- `is_pinned`カラムと`/memos/<id>/toggle-pin`ルート（JSONを返す）はすでに実装済み。今回はPython側を変更する必要はない（本章セクション4の`memos/views.py`を参照）
- このアプリは`CSRFProtect(app)`が有効なので、`fetch()`のPOSTには`X-CSRFToken`ヘッダーが必要（`018_ownership_crud`の「CSRFProtect(app)が必要な理由」を参照）。トークンは`<meta name="csrf-token">`にすでに埋め込んである
- `script.js`は全ページで読み込まれるため、対象の要素が無いページもある。`if (要素)`で存在確認してから使う
- 見た目やCSRF・所有権の仕組みは`018_ownership_crud`から変更不要

解答は`challenge/answer/`を参照してください。

### 動作確認：3つの機能がそれぞれ正しく動いているか

`challenge/static/script.js`はTODOのままだと何も起こらないので、下記の確認は完成版の`challenge/answer/`を実行して行ってください。

```bash
cd 019_javascript/challenge/answer
flask db init
flask db migrate -m "create users and memos tables"
flask db upgrade
python app.py
```

`http://127.0.0.1:5075/`にアクセスし、`/auth/register`で新規登録してからログインしておきます。

| 確認する操作 | 確認したいこと |
|---|---|
| メモ追加ページ（`/memos/new`）の本文欄に文字を入力する | 入力するたびに「◯ / 500文字」の数字がリアルタイムに増える。ページの再読み込みは発生しない |
| 本文欄に501文字以上入力する | 文字数の表示が赤字になる（`over`クラスが付く） |
| メモ一覧ページでカテゴリボタン（例：「仕事」）をクリックする | クリックしたボタンだけ色が変わり（`active`）、該当カテゴリ以外のカードが画面から消える（`hidden`）。ページの再読み込みは発生しない |
| 「すべて」ボタンをクリックする | 隠れていたカードがすべて再表示される |
| メモ一覧のピンボタン（☆）をクリックする | ページが再読み込みされずに☆が★に変わる。開発者ツールの「Network」タブで`/memos/<id>/toggle-pin`へのPOSTリクエストが1件発生していることが確認できる |
| ★になったボタンをもう一度クリックする | ★が☆に戻る |
| ピン留めした状態でページを再読み込みする | ★の状態を保ったまま、ピン留めしたメモが一覧の先頭に表示される（`memos/views.py`の`order_by(Memo.is_pinned.desc(), ...)`による。fetchでの更新がDBに反映されている証拠） |
| （比較用）`challenge/script.js`（TODOのまま）で同じ操作をする | 上記のいずれも起こらない（クリック・入力しても文字数・表示・★が変化しない）。これがこの練習問題で解消すべき「動いていない」状態 |

**正常な状態の見分け方**：3つの機能はいずれも「クリックや入力の直後に、ページ全体がリロードされずに一部の表示だけが変わる」という共通点があります。操作後にページ全体が再読み込みされている（タブのリロードアイコンが回る、スクロール位置がリセットされるなど）場合は、JavaScriptではなく通常のフォーム送信やリンク遷移が起きてしまっている可能性があります。

## 次のステップ

続きは [020_testing](../020_testing) で、このメモ帳アプリの自動テストを書きます。
