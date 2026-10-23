# 08 JavaScriptでデータを扱う

> フロントエンド編 ／ 前の章：[09_js_ui](../09_js_ui/) ／ 次の章：[11_homepage](../11_homepage/)

これまでは、表示する内容（制作実績の一覧など）をHTMLに直接書いていました。実際のアプリでは、**データ**（メモの一覧）と**画面**（HTML）を分けて扱います。データはJSONという形式でファイルやサーバーから受け取り、JavaScriptがそのデータから画面を作ります。

この章では、データを**読み込む**（`fetch()`）、データを**保存する**（`localStorage`）、データから**画面を作る**（描画）の3つを学びます。ここで学ぶことが、[02_backend/02_memo_app_frontend](../../02_backend/02_memo_app_frontend/)で作るメモアプリの土台になり、バックエンド編でサーバーとやり取りするときにもそのまま使います。

## 前提

| チャプター | 使う知識 |
|---|---|
| [00_docs/web_basic](../../00_docs/web_basic/) | リクエストとレスポンス、URL（ポート・`localhost`）、ステータスコード（200・404） |
| 05_js_basics〜08_js_render | コールバック関数・イベント・`trim()`・`createElement`・配列メソッド・`render()` |

## 目次

0. [この章はサーバー経由で開く](#0-この章はサーバー経由で開く)
1. [JSON](#1-json) — データの書き方・`JSON.stringify`・`JSON.parse`
2. [fetch()でデータを読み込む](#2-fetchでデータを読み込む) — `async`/`await`・`response.json()`・Ajax
3. [エラー処理](#3-エラー処理) — `response.ok`・`try`/`catch`・Networkタブ
4. [localStorage](#4-localstorage) — ブラウザにデータを保存する
5. [データから画面を作る](#5-データから画面を作る) — 「データを変える → 保存 → 描画」
6. [HTTPメソッドを体験する（JSONPlaceholder）（発展・任意）](#6-httpメソッドを体験するjsonplaceholder発展任意) — GET・POST・PUT・PATCH・DELETE
- [制作課題：オリジナルHP（ステップ4）](#制作課題オリジナルhpステップ4)

---

## フォルダ構成

```
01_frontend/10_js_data/
├── README.md
├── example/                      サンプル（1つのサンプル＝1つのフォルダ）
│   ├── 01_json/                  JSONの書き方・変換（サーバー不要）
│   │   ├── index.html
│   │   └── script.js
│   ├── 02_fetch/                 fetch()・エラー処理（サーバー必須）
│   │   ├── index.html
│   │   ├── script.js
│   │   └── data/memos.json
│   ├── 03_local_storage/         localStorage（サーバー不要）
│   │   ├── index.html
│   │   └── script.js
│   ├── 04_render/                データから画面を作る（やることリスト）
│   │   ├── index.html
│   │   └── script.js
│   └── 05_http_methods/          HTTPメソッドを体験する（発展・任意。JSONPlaceholder・インターネット接続が必要）
│       ├── index.html
│       └── script.js
├── question/                     練習問題（5問。問題文はREADMEの各節の最後）
│   ├── 01_json/                  練習問題1：JSONの読み書き
│   │   ├── index.html
│   │   └── script.js
│   ├── 02_book_table/            練習問題2：JSONファイルから本の一覧を読み込んで表にする
│   │   ├── index.html
│   │   ├── script.js
│   │   └── data/books.json
│   ├── 03_dark_mode/             練習問題3：ダークモードの設定を保存する
│   │   ├── index.html
│   │   └── script.js
│   ├── 04_reading_list/          練習問題4：読書記録アプリを作る
│   │   ├── index.html
│   │   └── script.js
│   ├── 05_post_board/            練習問題5：JSONPlaceholderで投稿ボードを作る（発展・任意）
│   │   ├── index.html
│   │   └── script.js
│   └── answer/                   解答（問題と同じ名前のフォルダ。中のファイル構成も問題と同じ）
│       ├── 01_json/
│       ├── 02_book_table/
│       ├── 03_dark_mode/
│       ├── 04_reading_list/
│       └── 05_post_board/
└── challenge/                         制作課題（オリジナルHP）ステップ4：data/works.json と js/script.js の読み込み部分を書く
    └── answer/                        完成例
```

---

## 0. この章はサーバー経由で開く

これまでのページは、ファイルをダブルクリックして開くだけで動きました。この章の`fetch()`を使うページは、**簡易サーバーを起動して、`http://`で開く**必要があります。

```bash
cd 01_frontend/10_js_data
python -m http.server 8000
# → http://localhost:8000/example/02_fetch/ などを開く（終了は Ctrl + C）
```

| 開き方 | アドレス | `fetch()` |
|---|---|---|
| ファイルを直接開く | `file:///Users/.../index.html` | **使えない**（Consoleに`Fetch API cannot load file:///...`などのエラーが出る） |
| サーバー経由で開く | `http://localhost:8000/...` | 使える |

ブラウザは安全のため、`file://`で開いたページがパソコン内のファイルを自由に読み込むことを禁止しています。`fetch()`は「サーバーにリクエストを送ってレスポンスを受け取る」仕組みなので、相手となるサーバーが必要です。`python -m http.server`は、フォルダの中のファイルをそのままレスポンスとして返すだけの、最も簡単なWebサーバーです。[00_docs/web_basic](../../00_docs/web_basic/)で見た「ブラウザがリクエストを送り、サーバーがレスポンスを返す」流れを、ここで初めて自分の手で動かします。

---

## 1. JSON

> [example/01_json/index.html](example/01_json/index.html) / [example/01_json/script.js](example/01_json/script.js)

**JSON**（JavaScript Object Notation）は、データをやり取りするための文字列の書き方です。JavaScriptのオブジェクトや配列とよく似た形で書けるので、人間にも読みやすく、ほとんどのプログラミング言語で扱えます。バックエンド編で作るFlaskのAPIも、JSONでデータを返します。

```json
[
    { "id": 1, "title": "買い物リスト", "tags": ["家事", "急ぎ"], "pinned": true },
    { "id": 2, "title": "企画会議メモ", "tags": [], "pinned": false }
]
```

### JSONの書き方のルール

JavaScriptのオブジェクトより**ルールが厳しい**ので注意します。

| ルール | 正しい | 間違い |
|---|---|---|
| キーは必ずダブルクォートで囲む | `{"title": "メモ"}` | `{title: "メモ"}` |
| 文字列はダブルクォート | `"メモ"` | `'メモ'` |
| 最後の要素の後ろにカンマを付けない | `[1, 2, 3]` | `[1, 2, 3,]` |
| 使える値 | 文字列・数値・`true`/`false`・`null`・配列・オブジェクト | 関数・`undefined`・コメント |

### JSONとJavaScriptの相互変換

```javascript
const memo = { id: 1, title: '買い物リスト', pinned: true };

const json = JSON.stringify(memo);   // オブジェクト → JSON文字列
// '{"id":1,"title":"買い物リスト","pinned":true}'

const back = JSON.parse(json);       // JSON文字列 → オブジェクト
back.title;                          // '買い物リスト'
```

| メソッド | 変換 | 使う場面 |
|---|---|---|
| `JSON.stringify(値)` | JavaScriptの値 → JSON文字列 | データを保存する・サーバーに送る |
| `JSON.parse(文字列)` | JSON文字列 → JavaScriptの値 | 保存したデータを読み出す・受け取ったデータを使う |

ルール違反のJSONを`JSON.parse()`するとエラーになります（`try`/`catch`については3節）。

#### 🐍 Pythonとの違い

```python
# Python：json モジュールを import して使う
import json

text = json.dumps({'title': '買い物'}, ensure_ascii=False)   # dict → JSON文字列
data = json.loads(text)                                      # JSON文字列 → dict
```

```javascript
// JavaScript：JSON は最初から使える（import 不要）
const text = JSON.stringify({ title: '買い物' });
const data = JSON.parse(text);
```

| | Python | JavaScript |
|---|---|---|
| 値 → JSON文字列 | `json.dumps(値)` | `JSON.stringify(値)` |
| JSON文字列 → 値 | `json.loads(文字列)` | `JSON.parse(文字列)` |
| 読み込み | `import json`が必要 | 不要（最初から使える） |
| 日本語の扱い | `ensure_ascii=False`を付けないと`\uXXXX`になる | そのまま日本語で出力される |
| `True` / `None` | JSONでは`true` / `null`に変換される | JSONの`true` / `null`と同じ |
| 整形して出力 | `json.dumps(値, indent=2)` | `JSON.stringify(値, null, 2)` |

バックエンド編のFlaskでは、PythonのdictをJSONにして返す側（`jsonify`）を作ります。このJavaScriptの`fetch()`が受け取る側です。

### 動作確認

| 確認する操作 | 確認したいこと |
|---|---|
| `example/01_json/index.html`をブラウザで開き、Consoleを見る | `JSON.stringify`の結果が`{"id":1,...}`という1行の文字列になり、`typeof`が`string`と表示される |
| 同じくConsoleを見る | `JSON.stringify(memo, null, 2)`の結果は改行とインデント付きで表示される |
| 同じくConsoleを見る | シングルクォートのJSONを`parse`しようとした行で「JSONとして読めない」とエラーの内容が表示される |


### 練習問題1：JSONの読み書き

> 問題：[question/01_json/index.html](question/01_json/index.html)・[question/01_json/script.js](question/01_json/script.js) ｜ 解答：[question/answer/01_json/index.html](question/answer/01_json/index.html)・[question/answer/01_json/script.js](question/answer/01_json/script.js)

<details>
<summary>問題の内容を開く</summary>

`01_json/script.js`の`TODO 1`〜`TODO 4`を書き、`01_json/index.html`を開いて、Consoleに「期待する出力」と同じものが出ることを確認します（サーバー不要）。

| # | やること | 期待する出力 |
|---|---|---|
| 1 | `user`をJSON文字列に変換して`console.log`する | `{"name":"山田","age":20,"hobbies":["読書","散歩"]}` |
| 2 | `text`を`JSON.parse`で配列に戻し、2件目の`title`を`console.log`する | `企画会議メモ` |
| 3 | TODO 2の配列から、`pinned`が`true`のものの件数を`console.log`する（`filter`を使う） | `1` |
| 4 | `broken`の文字列は「JSONとしては正しくない」。どこが間違っているか考え、正しいJSONに直した文字列を`fixed`に入れて、`JSON.parse`した結果の`city`を`console.log`する | `東京` |

</details>

---

## 2. fetch()でデータを読み込む

> [example/02_fetch/index.html](example/02_fetch/index.html) / [example/02_fetch/script.js](example/02_fetch/script.js) / [example/02_fetch/data/memos.json](example/02_fetch/data/memos.json)

`fetch(URL)`は、JavaScriptからサーバーにHTTPリクエストを送り、レスポンスを受け取る関数です。

```javascript
const loadMemos = async () => {
    const response = await fetch('data/memos.json');   // 1. リクエストを送り、レスポンスを待つ
    const memos = await response.json();               // 2. 本文をJSONとして読み、配列にする
    memos.forEach((memo) => list.append(createMemo(memo)));   // 3. データから画面を作る
};

loadMemos();
```

### 非同期処理と`async`/`await`

通信には時間がかかります（数ミリ秒〜数秒）。JavaScriptは、その間に画面が固まらないよう、**結果を待たずに次の処理へ進む**仕組みになっています。これを**非同期処理**と呼びます。`fetch()`は結果そのものではなく、「あとで結果が届く」ことを表す**Promise**というオブジェクトをすぐに返します。

| キーワード | 役割 |
|---|---|
| `async` | 関数の前に付けると、その中で`await`が使えるようになる |
| `await` | Promiseの結果が届くまで待ってから、次の行に進む |

`await`を付け忘れると、`response`にはまだ結果ではなくPromiseが入ったままになり、`response.json is not a function`のようなエラーになります。

#### 🐍 Pythonとの違い

Pythonでは、ふだんのコードで`async`/`await`はあまり使いません。`requests`ライブラリで通信すると、結果が届くまでその行で止まって待ちます。

```python
# Python（requests）：その行で結果が届くまで止まる。await は要らない
import requests

response = requests.get('https://example.com/data/memos.json')
memos = response.json()
```

```javascript
// JavaScript：待っている間もページが動き続けるので、「待つ」場所に await を書く
const response = await fetch('data/memos.json');
const memos = await response.json();
```

| | Python（`requests`） | JavaScript（`fetch`） |
|---|---|---|
| 通信中の動き | その行で**止まって待つ** | 画面を止めずに**別の処理を進める** |
| 結果を待つ書き方 | 普通に書くだけ | `await`を付ける（`async`関数の中だけ） |
| 本文をJSONにする | `response.json()` | `await response.json()`（こちらも`await`が必要） |
| 404のとき | `response.raise_for_status()`を呼べばエラー | 自分で`response.ok`を調べて`throw`する（3節） |

### `.then()`による書き方

同じ処理は`.then()`でも書けます。古いコードではこちらの書き方がよく使われています。

```javascript
fetch('data/memos.json')
    .then((response) => response.json())   // レスポンスが届いたら、JSONとして読む
    .then((memos) => {                     // 読み終わったら、データを使う
        memos.forEach((memo) => list.append(createMemo(memo)));
    });
```

`.then()`には「結果が届いたら呼び出してもらう関数」を渡します。05_js_basics の2節で学んだ**コールバック関数**です。`async`/`await`の方が上から順に読めるので、この章では主に`async`/`await`を使います。

### Ajax：ページを再読み込みせずに、画面の一部を書き換える

ここまでの「`fetch()`でデータを受け取り、その結果で画面の一部を作る」やり方には、**Ajax**（エイジャックス：Asynchronous JavaScript and XML）という呼び名があります。上で学んだ**非同期**（Asynchronous）の通信を**JavaScript**で行い、ページ全体を読み込み直さずに、必要な部分だけを書き換える手法です。

| | ページの移動（リンク・フォームの送信） | Ajax（`fetch()`） |
|---|---|---|
| サーバーに送るきっかけ | リンクのクリック・フォームの送信 | JavaScriptの`fetch()` |
| 返ってくるもの | ページ全体のHTML | 必要なデータだけ（今はJSONが主流） |
| 画面の変わり方 | ページ全体が白くなって読み込み直される。スクロール位置や入力中の内容はリセットされる | 一部だけが書き換わる。スクロール位置や入力中の内容はそのまま |
| 例 | 02_html_semantic_form のフォームの送信 | この章の2節・6節、SNSの「いいね」 |

名前に「XML」が入っているのは、Ajaxという言葉ができた頃（2005年ごろ）は、データをXMLという形式でやり取りすることが多かったからです。今はJSON（1節）が主流ですが、呼び名はそのまま使われています。

通信に使う道具も変わりました。昔は`XMLHttpRequest`（XHR）を使っていましたが、今は`fetch()`を使います。同じ「`data/memos.json`を読み込んでタイトルを表示する」処理を比べると、`fetch()`の方が短く、上から順に読めることがわかります。

```javascript
// 昔の書き方：XMLHttpRequest
const xhr = new XMLHttpRequest();
xhr.open('GET', 'data/memos.json');               // メソッドとURLを指定する
xhr.addEventListener('load', () => {              // 届いたら呼ばれる（コールバック）
    const memos = JSON.parse(xhr.responseText);   // 文字列で届くので、自分でJSONに戻す
    memos.forEach((memo) => console.log(memo.title));
});
xhr.send();                                       // 送信する

// 今の書き方：fetch()
const response = await fetch('data/memos.json');
const memos = await response.json();
memos.forEach((memo) => console.log(memo.title));
```

古い記事や求人では「Ajax」「非同期通信」という言葉がよく使われます。見かけたら、「`fetch()`で通信して、画面の一部を書き換えること」だと読み替えてください。このあとの6節（JSONPlaceholder・発展）も、Ajaxの例です。

### 動作確認：Ajaxで一部だけが書き換わることを確かめる

| 確認する操作 | 確認したいこと |
|---|---|
| `example/02_fetch/index.html`をサーバー経由で開き、Networkタブを開いてから「data/memos.json を読み込む」を押す | `memos.json`のリクエストが1件だけ増え、ページそのもののHTML（`index.html`）は読み直されていない。Typeの列は`fetch`（`XMLHttpRequest`なら`xhr`と表示される） |
| Networkタブの上にある「Fetch/XHR」フィルタを押す | Ajaxで送ったリクエスト（`fetch()`・`XMLHttpRequest`）だけに絞り込める |
| 6節の`example/05_http_methods/index.html`で、ボディ欄を書き換え、ページを少しスクロールしてから「送信」を何回か押す | 書き換えた内容もスクロール位置も、送信のたびに消えたりリセットされたりしない（ページ全体を読み込み直していない） |
| 同じページで、ブラウザの再読み込みボタンを押す | ページ全体が読み込み直され、書き換えた内容が元に戻る（Ajaxとの違い） |

### GET以外のメソッドで送る

`fetch(URL)`だけで呼ぶと、HTTPメソッドは**GET**（データの取得）になります（[00_docs/web_basic](../../00_docs/web_basic/#4-リクエストとレスポンス)の4節）。POST・PUT・DELETEで送るときは、2つ目の引数に設定のオブジェクトを渡します。

```javascript
// POST：新しいメモを送る（受け取って保存するのはサーバー側のプログラム）
const response = await fetch('/api/memos', {
    method: 'POST',                                   // メソッド
    headers: { 'Content-Type': 'application/json' },  // ボディの中身はJSONです、と伝える
    body: JSON.stringify({ title: '買い物', category: '家事', body: '牛乳' }),   // 送るデータ（1節の JSON.stringify）
});

// DELETE：3番のメモを削除する
await fetch('/api/memos/3', { method: 'DELETE' });
```

| 設定 | 説明 |
|---|---|
| `method` | `'GET'`（省略時）・`'POST'`・`'PUT'`・`'DELETE'`など |
| `headers` | リクエストのヘッダー。JSONを送るときは`Content-Type: application/json`を付ける |
| `body` | 送るデータ。オブジェクトはそのまま送れないので、`JSON.stringify()`で文字列にする |

実際に送って結果を見るのは、[6節](#6-httpメソッドを体験するjsonplaceholder発展任意)（発展・任意）で練習用のAPIを相手に行います。POST・PUT・DELETEを受け取って、データを本当に保存・変更・削除するのはサーバー側のプログラムの役割で、バックエンド編で作ります。`python -m http.server`はファイルを返すだけのサーバーなので、POSTを送ってもエラー（501）になります。

---

## 3. エラー処理

通信は失敗することがあります（ファイルが無い・サーバーが止まっている・ネットワークが切れているなど）。失敗したときに画面が「読み込み中…」のまま止まらないよう、エラー処理を書きます。

```javascript
const loadMemos = async (url) => {
    try {
        const response = await fetch(url);
        if (!response.ok) {                              // 200番台以外（404など）
            throw new Error(`HTTP ${response.status}`);  // 自分でエラーにする
        }
        const memos = await response.json();
        // ...画面を作る
        statusEl.textContent = `${memos.length}件読み込みました`;
    } catch (error) {
        // try の中でエラーが起きると、ここに飛んでくる
        statusEl.textContent = `読み込みに失敗しました（${error.message}）`;
        statusEl.classList.add('error');
    }
};
```

| 書き方 | 説明 |
|---|---|
| `try { ... } catch (error) { ... }` | `try`の中でエラーが起きたら、処理を中断して`catch`に移る |
| `throw new Error('メッセージ')` | 自分でエラーを発生させる |
| `response.ok` | ステータスコードが200番台なら`true` |
| `response.status` | ステータスコード（`200`・`404`など） |

**注意**：`fetch()`は、サーバーから**404や500が返ってきてもエラーにしません**（レスポンス自体は届いているため）。エラーになるのはネットワークが切れているときなどだけです。そのため`response.ok`を自分で確認し、`throw`でエラーにする必要があります。

#### 🐍 Pythonとの違い

```python
# Python
try:
    response = requests.get(url)
    if not response.ok:
        raise Exception(f'HTTP {response.status_code}')
    memos = response.json()
except Exception as error:
    print(f'読み込みに失敗しました（{error}）')
finally:
    print('終わり')
```

| | Python | JavaScript |
|---|---|---|
| 試す | `try:` | `try { ... }` |
| 失敗したときの処理 | `except Exception as error:` | `catch (error) { ... }` |
| 必ず行う処理 | `finally:` | `finally { ... }`（同じ） |
| エラーを自分で起こす | `raise Exception('メッセージ')` | `throw new Error('メッセージ')` |
| エラーのメッセージ | `str(error)` | `error.message` |
| ステータスコード | `response.status_code` | `response.status` |
| 成功か（200番台か） | `response.ok` | `response.ok`（同じ） |
| エラーの種類で分ける | `except ValueError:`のように型を書ける | `catch (error)`は1つだけ。種類は`error`の中身で調べる |

### 成功しても失敗しても行う処理：`finally`

`try`/`catch`の後ろに`finally`を付けると、**成功したときも失敗したときも、最後に必ず**実行されます。通信中はボタンを押せなくしておき、終わったら戻す、という処理によく使います。

```javascript
button.addEventListener('click', async () => {
    button.disabled = true;           // 通信中は押せなくする（連打を防ぐ）
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        // ...成功したときの処理
    } catch (error) {
        // ...失敗したときの処理
    } finally {
        button.disabled = false;      // 成功しても失敗しても、ボタンを戻す
    }
});
```

`finally`を使わずに`try`と`catch`の両方の最後に`button.disabled = false;`を書くこともできますが、書き忘れると、失敗したときにボタンが押せないままになってしまいます。6節のサンプル（`example/05_http_methods/`）の「送信」ボタンが、この書き方です。

### Networkタブで通信を見る

開発者ツールの**Network**タブを開いた状態でページを操作すると、`fetch()`が送ったリクエストが一覧に表示されます。

| 列・タブ | 見えるもの |
|---|---|
| Name | リクエストしたファイル名（`memos.json`） |
| Status | ステータスコード（成功なら`200`、ファイルが無ければ`404`） |
| Type | `fetch`と表示される |
| （行をクリック）Response / Preview | サーバーから返ってきた本文（JSONの中身） |

### 動作確認：読み込みの成功と失敗

`python -m http.server`を起動し、`http://localhost:8000/example/02_fetch/`を開いて確認します。

| 確認する操作 | 確認したいこと |
|---|---|
| Networkタブを開いて「data/memos.json を読み込む」を押す | 3件のメモが表示され、「3件読み込みました」と表示される。Networkタブに`memos.json`がStatus `200`で記録される |
| Networkタブで`memos.json`の行をクリックし、Previewを見る | JSONの中身が展開して表示される |
| 「存在しないファイルを読み込む」を押す | 赤字で「読み込みに失敗しました（HTTP 404）」と表示される。Networkタブには`not-found.json`がStatus `404`で記録される |
| `data/memos.json`の最後の`}`の後ろにカンマを足して保存し、読み込み直す（確認後は戻す） | 赤字のエラーが表示される（JSONの形式が正しくないので`response.json()`が失敗する） |
| `index.html`をファイルとして直接開いて（`file://`）ボタンを押す | 読み込みに失敗する。Consoleに`fetch`が使えない旨のエラーが出る |


### 練習問題2：JSONファイルから本の一覧を読み込んで表にする

> 問題：[question/02_book_table/index.html](question/02_book_table/index.html)・[question/02_book_table/script.js](question/02_book_table/script.js) ｜ 解答：[question/answer/02_book_table/index.html](question/answer/02_book_table/index.html)・[question/answer/02_book_table/script.js](question/answer/02_book_table/script.js)

<details>
<summary>問題の内容を開く</summary>

2節（`fetch()`）と3節（エラー処理）を組み合わせる問題です。[question/02_book_table/data/books.json](question/02_book_table/data/books.json)の4冊を読み込み、`02_book_table/index.html`の表の行として表示します。HTMLとCSSは完成しています。このページは、0節のとおりサーバー経由で開きます。

```bash
cd 01_frontend/10_js_data
python -m http.server 8000
# → http://localhost:8000/question/02_book_table/index.html
```

| # | やること | ヒント |
|---|---|---|
| 1 | `createRow(book)`：本1冊分の行を作って返す。構造は`<tr><td>タイトル</td><td>著者</td><td>発表年</td><td>✓ または 空</td></tr>`（`read`が`true`なら「✓」） | `td`を4つ作って`textContent`を入れ、`tr.append(td1, td2, td3, td4)`。配列と`forEach`を使うと短く書ける：`[book.title, book.author, book.year, book.read ? '✓' : ''].forEach((value) => { ... });` |
| 2 | `loadBooks()`：`data/books.json`を読み込んで表示する`async`関数 | 下の手順のとおり |

`loadBooks()`の手順：

1. `fetch('data/books.json')`で読み込む（`await`）
2. `response.ok`が`false`なら`throw new Error(...)`でエラーにする
3. `response.json()`で配列にする（`await`）
4. 各本の行を`rows`に追加する
5. `statusEl`の文字を消し、`summary`に「◯冊中◯冊読了」と表示する
6. 失敗したら（`catch`）、`statusEl`に「本の一覧を読み込めませんでした」と表示し、`error`クラスを付ける

| 確認する操作 | 確認したいこと |
|---|---|
| サーバー経由で開く | 4冊が表の行として表示され、表の下に「4冊中2冊読了」と表示される |
| `fetch()`のファイル名をわざと間違えてリロードする（確認後は戻す） | 赤字で「本の一覧を読み込めませんでした」と表示される。Networkタブで`404`になっている |

</details>

---

## 4. localStorage

> [example/03_local_storage/index.html](example/03_local_storage/index.html) / [example/03_local_storage/script.js](example/03_local_storage/script.js)

`fetch()`で読み込めるのは、サーバーに置いてあるファイルだけです。ユーザーが追加・変更したデータを残しておくには、どこかに**保存**する必要があります。**localStorage**は、ブラウザの中に「キーと値」の組を保存できる仕組みです。ページを閉じても、ブラウザを再起動しても消えません。

```javascript
localStorage.setItem('draft', '書きかけの文章');   // 保存する
localStorage.getItem('draft');                    // 読み出す（無ければ null）
localStorage.removeItem('draft');                 // 1件消す
```

### 保存できるのは文字列だけ

配列やオブジェクトは、`JSON.stringify()`で文字列にしてから保存し、読み出すときに`JSON.parse()`で戻します。

```javascript
const save = (memos) => {
    localStorage.setItem('memos', JSON.stringify(memos));
};

const load = () => {
    const json = localStorage.getItem('memos');
    return json ? JSON.parse(json) : [];   // 保存されていなければ（null なら）空の配列
};
```

オブジェクトをそのまま`setItem()`すると、`'[object Object]'`という意味のない文字列が保存されてしまいます。

### 開発者ツールで中身を見る

**Application**タブ（Safariは「ストレージ」タブ）→ 左側の **Local storage** → ページのアドレスを選ぶと、保存されているキーと値の一覧が表示されます。値を直接書き換えたり、削除したりもできます。

### localStorageの特徴と限界

| 特徴 | 説明 |
|---|---|
| ブラウザの中だけに保存される | 別のパソコン・スマホ・別のブラウザからは見えない |
| サイト（オリジン）ごとに分かれる | `http://localhost:8000`で保存したデータは、`http://localhost:5000`からは見えない |
| 容量は5MB程度 | 画像や大量のデータには向かない |
| ユーザーが消せる | ブラウザの閲覧データを削除すると消える |
| 誰でも中身を見られる | パスワードなどの秘密の情報は保存しない |

「別の端末から見られない」「他の人と共有できない」という限界を、バックエンド編でサーバーとデータベースを使って解決していきます。

### localStorageが使えないこともある

ブラウザの設定（プライベートブラウズ・サイトのデータの保存を禁止している、など）によっては、`localStorage`を使おうとした時点でエラーになることがあります。エラーになると、それより後の処理がすべて止まってしまいます（05_js_basics 0節）。「保存できたら便利」程度の機能なら、`try`/`catch`（3節）で囲み、保存できなくてもページは動くようにしておきます。

```javascript
try {
    localStorage.setItem('memo-filter', category);
} catch (error) {
    // 保存できなくても、絞り込み自体は動くので何もしない
}
```

### 応用：OSの設定と、ボタンでの切り替えを両立する

練習問題3では、ダークモードを`body`のクラスで切り替えました。実際のサイトでは、「最初はOSの設定（04_css_layout 5節の`prefers-color-scheme`）に従い、ボタンを押したらその選択を覚える」という作り方がよく使われます。完成例の[02_backend/100_memo_api](../../02_backend/100_memo_api/)の「◐」ボタンが、この書き方です。

**1. CSS：選んだ配色を`<html>`の`data-theme`属性で表す**

```css
:root { --color-bg: #f4f6f9; --color-text: #262b33; }       /* ライト（基本） */

@media (prefers-color-scheme: dark) {
    :root:not([data-theme="light"]) {                       /* OSがダークで、ライトを選んでいないとき */
        --color-bg: #16181d; --color-text: #e6e8ec;
    }
}

:root[data-theme="dark"] {                                  /* ボタンでダークを選んだとき */
    --color-bg: #16181d; --color-text: #e6e8ec;
}
```

**2. HTML：保存した配色を、`<head>`の中で先に反映する**

`</body>`の直前の`script.js`で反映すると、ページが一瞬ライトで表示されてからダークに変わる「チラつき」が起きます。そこで、この数行だけは`<head>`の中に直接書き、CSSが当たる前に`data-theme`を付けます。

```html
<head>
    ...
    <link rel="stylesheet" href="css/style.css">
    <script>
        try {
            const saved = localStorage.getItem('theme');   // 'light' / 'dark' / null
            if (saved) {
                document.documentElement.dataset.theme = saved;   // <html data-theme="dark">
            }
        } catch (error) {
            // 保存できない環境では、OSの設定に従う
        }
    </script>
</head>
```

**3. JavaScript：ボタンで切り替えて保存する**

```javascript
const root = document.documentElement;   // <html> 要素

// 今の配色：ボタンで選んだもの（data-theme）が無ければ、OSの設定を調べる
const currentTheme = () => {
    if (root.dataset.theme) {
        return root.dataset.theme;
    }
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
};

themeButton.addEventListener('click', () => {
    const next = currentTheme() === 'dark' ? 'light' : 'dark';
    root.dataset.theme = next;
    try {
        localStorage.setItem('theme', next);
    } catch (error) {
        // 保存できなくても、表示は切り替わっている
    }
});
```

| 書き方 | 説明 |
|---|---|
| `document.documentElement` | `<html>`要素。`dataset.theme`に入れると`data-theme`属性になる |
| `:root[data-theme="dark"]`（CSS） | `<html>`に`data-theme="dark"`が付いているとき（`:root`は`<html>`のこと） |
| `:not([data-theme="light"])`（CSS） | `data-theme="light"`が**付いていない**とき（`:not(...)`は「〜でない」を表す） |
| `window.matchMedia('(メディアクエリ)').matches` | CSSのメディアクエリが今の画面に当てはまるかを、JavaScriptで`true`/`false`で調べる |

### 動作確認

`example/03_local_storage/index.html`をブラウザで開いて確認します（サーバーは不要です）。

| 確認する操作 | 確認したいこと |
|---|---|
| 何度かリロードする | 訪問回数が1ずつ増える |
| 下書き欄に入力してからタブを閉じ、開き直す | 入力した内容が残っている |
| 「文字を大きくする」にチェックしてリロードする | 文字が大きいまま表示される |
| Applicationタブの Local storage を見る | `visitCount`・`draft`・`settings`の3つのキーが保存されている。`settings`の値は`{"large":true}`というJSON文字列 |
| 「保存したデータをすべて消す」を押す | 訪問回数が1に戻り、下書きと設定が消える |


### 練習問題3：ダークモードの設定を保存する

> 問題：[question/03_dark_mode/index.html](question/03_dark_mode/index.html)・[question/03_dark_mode/script.js](question/03_dark_mode/script.js) ｜ 解答：[question/answer/03_dark_mode/index.html](question/answer/03_dark_mode/index.html)・[question/answer/03_dark_mode/script.js](question/answer/03_dark_mode/script.js)

<details>
<summary>問題の内容を開く</summary>

`03_dark_mode/index.html`のHTMLとCSSは完成しています。`03_dark_mode/script.js`を書いて、ダークモードの設定を`localStorage`に保存します（サーバー不要）。

| # | 仕様 |
|---|---|
| 1 | 「ダークモード」ボタンを押すたびに、`<body>`の`dark`クラスを付け外しする（CSSで配色が変わる） |
| 2 | ボタンの文字を、ダークモード中は「ライトモードにする」、そうでなければ「ダークモードにする」にする |
| 3 | 選んだモードを`localStorage`に保存し、ページをリロードしても同じモードで表示されるようにする |
| 4 | 「最後に切り替えた日時」を、保存した日時から表示する（まだ一度も切り替えていなければ「まだありません」） |

保存の形は自由ですが、`{ "dark": true, "updatedAt": "2026/10/2 21:30:00" }`のように1つのオブジェクトにまとめてJSONで保存すると扱いやすくなります。

| # | やること | ヒント |
|---|---|---|
| 1 | `loadTheme()`：保存されている設定を読み出す。保存されていなければ`{ dark: false, updatedAt: null }`を返す | `localStorage.getItem()` / `JSON.parse()` |
| 2 | `saveTheme(theme)`：設定を保存する | `localStorage.setItem()` / `JSON.stringify()` |
| 3 | `applyTheme(theme)`：設定を画面に反映する。`body`の`dark`クラスの付け外し・ボタンの文字・日時の表示（`null`なら「まだありません」） | `classList.toggle`の第2引数 |
| 4 | ページを開いたときに保存されている設定を反映し、ボタンが押されたら「設定を反転→保存→反映」する | 今の日時の文字列は`new Date().toLocaleString()`で作れる |

| 確認する操作 | 確認したいこと |
|---|---|
| ボタンを押してからリロードする | 同じモードで表示され、切り替えた日時が残っている |
| Applicationタブの Local storage を見る | `theme`キーにJSON文字列が保存されている |

</details>

---

## 5. データから画面を作る

> [example/04_render/index.html](example/04_render/index.html) / [example/04_render/script.js](example/04_render/script.js)

データを追加・変更できるようになると、「データ（配列）」と「画面（HTML）」の両方を正しく保つ必要があります。ボタンが押されるたびに画面の一部を直接書き換えていると、データと画面がずれるバグが起きやすくなります。

そこで、**データを正しい状態として持ち、画面は毎回データから作り直す**という考え方をします。この考え方は[08_js_render](../08_js_render/#2-データから画面を作る)で学んだ`render()`と同じです。ここでは、そこに「**保存する**」ステップを加えます。

```
ボタンが押された
   ↓
1. データ（配列）を変更する   todos.push(...) / todos.filter(...)
   ↓
2. 保存する                   save()   → localStorage.setItem(...)
   ↓
3. 画面を作り直す             render() → 一覧を空にして、配列から全部作る
```

```javascript
let todos = load();               // 画面の元になるデータ（状態）

const render = () => {
    list.textContent = '';        // いったん全部消して
    todos.forEach((todo) => {     // データから作り直す
        list.append(createItem(todo));
    });
};

form.addEventListener('submit', (event) => {
    event.preventDefault();
    todos.push({ id: Date.now(), title: input.value, done: false });   // 1. データを変える
    save();                                                            // 2. 保存する
    render();                                                          // 3. 描画する
});
```

### 作り直す要素へのイベントは、親に登録する

`render()`のたびにボタンなどの要素は作り直されるので、要素1つずつに`addEventListener`しても、次の描画で消えてしまいます。そこで、作り直されない**親要素**（一覧の`ul`）に1回だけイベントを登録し、`event.target`で何が押されたかを判定します（06_js_events の3節で学んだ書き方です）。

```javascript
list.addEventListener('click', (event) => {
    const li = event.target.closest('li');
    const id = Number(li.dataset.id);          // dataset の値は文字列なので数値に戻す
    if (event.target.classList.contains('remove')) {
        todos = todos.filter((t) => t.id !== id);
        save();
        render();
    }
});
```

| 書き方 | 説明 |
|---|---|
| `Date.now()` | 現在時刻をミリ秒で表した数値。簡易的な一意のIDとして使える |
| `Number('3')` | 文字列を数値に変換する。`dataset`や`localStorage`から読んだ値は文字列なので、数値として比べる前に変換する |
| `new Date().toLocaleString()` | 今の日時を、使っている環境の形式の文字列にする（日本語環境では`2026/10/2 21:30:00`）。`new Date()`は今の日時を表すオブジェクト |
| `配列.push(値)` / `配列.unshift(値)` | 配列の最後 / 先頭に追加する（05_js_basics 1節・08_js_render 1節） |
| `文字列.startsWith('文字')` | その文字で始まるか（`true`/`false`）。「タイトルが`【済】`で始まるか」のような判定に使う |
| `要素.classList.contains('クラス名')` | その要素にクラスが付いているか。`event.target`が押されたボタンの種類を判定するときに使う（07_js_dom 1節） |
| `ボタン.disabled = true` / `false` | ボタンを押せなく / 押せるようにする |
| `配列.sort((a, b) => 比較)` | 並べ替える（元の配列が変わる）。文字列の新しい順は`b.date.localeCompare(a.date)`（制作課題の自由課題で使う） |

### 動作確認

`example/04_render/index.html`をブラウザで開いて確認します（サーバーは不要です）。

| 確認する操作 | 確認したいこと |
|---|---|
| やることを3件追加する | 一覧に追加され、「全3件（未完了 3件）」と表示される |
| 1件のチェックボックスを押す | その項目に取り消し線が付き、「未完了 2件」になる |
| 1件を削除する | 一覧から消え、件数も減る |
| リロードする | 追加・完了・削除した状態がそのまま残っている |
| Elementsパネルを見ながら操作する | 操作のたびに`ul`の中身がまとめて作り直されている |


### 練習問題4：読書記録アプリを作る

> 問題：[question/04_reading_list/index.html](question/04_reading_list/index.html)・[question/04_reading_list/script.js](question/04_reading_list/script.js) ｜ 解答：[question/answer/04_reading_list/index.html](question/answer/04_reading_list/index.html)・[question/answer/04_reading_list/script.js](question/answer/04_reading_list/script.js)

<details>
<summary>問題の内容を開く</summary>

「データを変える→保存→描画」の考え方で、読書記録アプリを作ります。HTMLとCSSは完成しています（サーバー不要）。データ（`books`配列）の1件は次の形です。

```javascript
{ id: 1759480000000, title: '銀河鉄道の夜', author: '宮沢賢治', read: false }
```

| # | 仕様 |
|---|---|
| 1 | フォームでタイトルと著者を入力して「追加」を押すと、一覧の最後に追加される（タイトルが空白だけなら追加しない。著者が空欄なら「著者不明」にする） |
| 2 | 各行の「読了にする」ボタンで`read`を切り替える。読了の行は`.read`クラスが付き（CSSで取り消し線）、ボタンの文字は「未読に戻す」になる |
| 3 | 各行の「削除」ボタンで、`confirm('『タイトル』を削除しますか？')`で確認してから削除する |
| 4 | 上の「すべて／未読／読了」ボタンで、表示する本を切り替える（押したボタンに`active`クラス）。表示の切り替えはデータを変えるのではなく、`render()`で「表示する分だけ」を選んで作る |
| 5 | `#summary`に「全3冊（読了 1冊）」のように、表示の切り替えに関係なく全体の件数を表示する |
| 6 | 追加・読了・削除の結果を`localStorage`（キー`'reading-list'`）に保存し、リロードしても残る |

`04_reading_list/script.js`には次の6つを書きます。

| # | やること | ヒント |
|---|---|---|
| 1 | `load()`：保存されていれば`JSON.parse()`して返し、無ければ空の配列を返す。`save()`：`books`を`JSON.stringify()`して保存する | 4節の`load` / `save`と同じ形 |
| 2 | `createItem(book)`：本1冊分の`li`を作って返す（構造は下のとおり。`read`なら`li`に`class="read"`、ボタンの文字は「未読に戻す」） | タイトル・著者は利用者が入力した文字なので`textContent`で入れる |
| 3 | `render()`：`list`を空にし、`filter`に合う本だけを`createItem()`して追加し、`summary`に件数を表示する | `'unread'`なら`read`が`false`、`'read'`なら`true`、`'all'`なら全部。件数は`books`全体で数える |
| 4 | 追加（フォームの`submit`） | 送信を止め、`{ id: Date.now(), title, author, read: false }`を`push`→`save()`→`render()`→入力欄を空にする |
| 5 | 読了の切り替えと削除 | ボタンは`render()`のたびに作り直されるので、変わらない親の`list`に1回だけ`'click'`を登録する。行の`id`は`Number(event.target.closest('li').dataset.id)`。データを変えたら`save()`→`render()` |
| 6 | 表示の切り替え（すべて／未読／読了） | 押したボタンだけ`active`クラスを付け、`filter`を`data-filter`の値にして`render()`する（データは変わらないので`save()`は不要） |

```html
<li data-id="1759480000000">                              <!-- read が true なら class="read" -->
    <div class="info">
        <span class="title">銀河鉄道の夜</span><br>
        <span class="author">宮沢賢治</span>
    </div>
    <button type="button" class="toggle">読了にする</button>  <!-- read なら「未読に戻す」 -->
    <button type="button" class="remove">削除</button>
</li>
```

| 確認する操作 | 確認したいこと |
|---|---|
| 3冊追加し、1冊を「読了にする」 | 取り消し線が付き、「全3冊（読了 1冊）」になる |
| 「未読」を押し、その状態で1冊追加する | 未読の本だけが表示され、追加した本（未読）も一覧に増える |
| 「削除」を押し、確認でキャンセルする／OKを押す | キャンセルなら消えない。OKなら消える |
| リロードする | 追加・読了・削除した状態が残っている（表示の切り替えは「すべて」に戻ってよい） |
| Applicationタブの Local storage を見る | `reading-list`の値がJSONの配列になっている |

</details>

---

## 6. HTTPメソッドを体験する（JSONPlaceholder）（発展・任意）

この節は**発展（任意）**です。読み飛ばしても、制作課題とバックエンド編は進められます。PUT・PATCH・DELETEでデータを変える流れは、バックエンド編でサーバーを自分で作るときに、あらためて扱います（[02_backend/08_request](../../02_backend/08_request/)）。余裕があるときや、外部のAPIを使ってみたくなったときに戻ってきてください。

> [example/05_http_methods/index.html](example/05_http_methods/index.html) / [example/05_http_methods/script.js](example/05_http_methods/script.js)

2節の「GET以外のメソッドで送る」を、実際に試してみます。相手は**JSONPlaceholder**（`https://jsonplaceholder.typicode.com`）という、練習用に公開されている無料のAPIです。投稿（`/posts`）などのデータがあり、メソッドごとに本物のAPIと同じような返事をしてくれます。

| リクエスト | 意味 | 返ってくるもの | ステータスコード |
|---|---|---|---|
| `GET /posts` | 投稿の一覧を取得する（`?_limit=3`で件数、`?userId=1`で絞り込み） | 投稿の配列 | 200 |
| `GET /posts/1` | 1番の投稿を取得する | 投稿1件 | 200（無ければ404） |
| `POST /posts` | 投稿を追加する | 送った内容に`id: 101`を付けたもの | 201（Created：作成した） |
| `PUT /posts/1` | 1番の投稿を**丸ごと置き換える** | 送った内容そのもの（送らなかった項目は無くなる） | 200 |
| `PATCH /posts/1` | 1番の投稿の**一部だけを変える** | 元の投稿に、送った項目だけを上書きしたもの | 200 |
| `DELETE /posts/1` | 1番の投稿を削除する | 空のオブジェクト`{}` | 200 |

**注意**：JSONPlaceholderは「本物そっくりの返事をするだけ」です。POST・PUT・PATCH・DELETEを送っても、**サーバーのデータは実際には変わりません**（削除したはずの投稿も、GETし直すと元のまま返ってきます）。また、POSTで返ってくる`id`は毎回`101`です。データを本当に保存・変更・削除するサーバーは、バックエンド編で自分で作ります。インターネットへの接続が必要です。

### PUTとPATCHの違い

どちらも「更新」ですが、送らなかった項目の扱いが違います。1番の投稿（`userId`・`id`・`title`・`body`の4項目）に、`{ "title": "新しいタイトル" }`だけを送った場合：

| メソッド | 結果 |
|---|---|
| PUT | 投稿が`{ "title": "新しいタイトル", "id": 1 }`に**置き換わる**（`id`はURLから付く。`userId`・`body`は無くなる）。そのため、PUTでは全部の項目を送る |
| PATCH | `title`だけが変わり、`body`などは**元のまま残る** |

このカリキュラムのバックエンド編では、更新にPUTを使います。

### 動作確認

`python -m http.server`で起動し、`example/05_http_methods/index.html`を開きます。開発者ツールの**Network**タブも開いておきます。

| 確認する操作 | 確認したいこと |
|---|---|
| 「GET 一覧（3件）」→「送信」 | `200 成功`と、3件の投稿の配列が表示される。Networkタブで Request Method が`GET` |
| 「GET 存在しない（404）」→「送信」 | `404 失敗`と表示される（`fetch()`はエラーにならず、`response.ok`が`false`になる：3節） |
| 「POST 追加」→「送信」 | `201 成功`と、送った内容に`"id": 101`が付いたものが返ってくる。Networkタブの Payload に送ったJSONが表示される |
| 「PUT 丸ごと置き換え」と「PATCH 一部だけ変更」をそれぞれ送る | PUTは送った項目だけが返り、PATCHは`body`など送っていない項目も元のまま返ってくる |
| 「DELETE 削除」→「送信」 | `200 成功`と`{}`が返る。そのあと「GET 1件」を送ると、1番の投稿は消えずに返ってくる（練習用APIなので実際には削除されない） |
| ボディを`{title:'x'}`のように書き換えて送信する | 送る前に「ボディが正しいJSONではありません」と表示される（1節：キーは`"`で囲む） |

### 練習問題5：JSONPlaceholderで投稿ボードを作る（発展・任意）

> 問題：[question/05_post_board/index.html](question/05_post_board/index.html)・[question/05_post_board/script.js](question/05_post_board/script.js) ｜ 解答：[question/answer/05_post_board/index.html](question/answer/05_post_board/index.html)・[question/answer/05_post_board/script.js](question/answer/05_post_board/script.js)

<details>
<summary>問題の内容を開く</summary>

JSONPlaceholderを相手に、GET・POST・PATCH・DELETEを使う投稿ボードを作ります。HTMLとCSSは完成しています。5節と同じく、データ（`posts`配列）を変えてから`render()`で画面を作り直します。

| # | 仕様 |
|---|---|
| 1 | 開いたら、`GET /posts?userId=1&_limit=5`で5件の投稿を読み込んで表示する |
| 2 | フォームでタイトルと本文を入力して「投稿する」を押すと、`POST /posts`で送り、返ってきた投稿を一覧の**先頭**に加える（タイトルが空白だけなら送らない） |
| 3 | 各投稿の「済にする」を押すと、`PATCH /posts/:id`でタイトルを「【済】元のタイトル」に変える。済になった投稿のボタンは押せなくする |
| 4 | 各投稿の「削除」を押すと、`DELETE /posts/:id`を送り、成功したら一覧から消す |
| 5 | 「存在しない投稿（id: 9999）を読み込む」を押すと、`GET /posts/9999`が404になり、「投稿が見つかりませんでした」と表示する |
| 6 | リクエストを送るたびに、`#log`に「`POST /posts → 201`」のように、メソッド・パス・ステータスコードを表示する。失敗したときは`error`クラスを付ける（赤くなる） |

`05_post_board/script.js`には次の7つを書きます。

| # | やること | ヒント |
|---|---|---|
| 1 | `request(method, path, data)`：リクエストを送り、`#log`に結果を表示し、成功ならレスポンスのJSONを返す。失敗（`response.ok`が`false`）なら`throw new Error(...)`する | `data`があるときだけ`headers`と`body`（`JSON.stringify(data)`）を付ける。メソッドが違っても、送り方はこの1つの関数にまとめる |
| 2 | `createItem(post)`：投稿1件分の`li`を作る（タイトルの`h2`・本文の`p`・「済にする」ボタン（`class="done"`）・「削除」ボタン（`class="remove"`）。`li`には`data-id`） | タイトルが`【済】`で始まるなら、「済にする」を`disabled`にする（`文字列.startsWith()`） |
| 3 | `render()`：`posts`から一覧を作り直す | 5節の`render()`と同じ |
| 4 | `loadPosts()`：仕様1 | 失敗したら`#log`にメッセージを出す |
| 5 | フォームの`submit`：仕様2 | JSONPlaceholderは毎回`id: 101`を返すので、一覧で区別できるよう、返ってきた投稿の`id`を`Date.now()`に付け直してから`posts.unshift()`する |
| 6 | 一覧のクリック：仕様3・4 | 作り直される`li`ではなく、親の`#post-list`に1回だけ登録する（5節）。PATCHは変える項目だけ（`{ title: 新しいタイトル }`）を送る。DELETEはボディを送らない。リクエストが失敗したときは、データを変えない |
| 7 | 「存在しない投稿」ボタン：仕様5 | `request()`が投げたエラーを`try`/`catch`で受け取る |

| 確認する操作 | 確認したいこと |
|---|---|
| `python -m http.server`で起動して開く | 5件の投稿が表示され、`#log`に`GET /posts?userId=1&_limit=5 → 200` |
| タイトルを入力して「投稿する」 | 一覧の先頭に追加され、`POST /posts → 201` |
| 追加した投稿と、元からある投稿の「済にする」を押す | どちらもタイトルが「【済】…」になり、ボタンが押せなくなる。`PATCH … → 200` |
| 「削除」を押す | 一覧から消え、`DELETE /posts/… → 200` |
| 「存在しない投稿」を押す | `#log`が赤くなり、`GET /posts/9999 → 404：投稿が見つかりませんでした` |
| リロードする | 最初の5件に戻る（練習用APIなので、サーバーのデータは変わっていない） |

</details>

---

## 制作課題：オリジナルHP（ステップ4）

> [challenge/](challenge/) — 雛形 ｜ [challenge/answer/](challenge/answer/) — 完成例 ｜ 自分のHP：[00_my_homepage/](../00_my_homepage/)

HPの制作実績（または好きなもの紹介）の一覧を、HTMLから`data/works.json`に分けて、`fetch()`で読み込んで表示します。

制作課題は、毎回次の2段階で進めます。

1. **`challenge/`で練習する**：架空の人物「山田 太郎」のサイトを題材に、ファイルの中のTODOコメントに沿って書きます。書けたら`challenge/answer/`の完成例と見比べます。
2. **自分のHPに反映する**：同じことを、[00_my_homepage/](../00_my_homepage/)の自分のサイトに行います。こちらは文章・配色・レイアウトを自分で考えて作ります。下の「必須要件」は、自分のHPで満たすべき要件です。

### challenge/ の内容

| ファイル | 内容 |
|---|---|
| `works.html` | 作品のカードを削除し、空の`<ul id="works-list">`と、読み込み状況を表示する`<p id="works-status">`を置いたもの（完成済み） |
| `data/works.json` | 作品が**2件だけ**書いてある。残りの3件は、[08_js_renderの完成例のworks.html](../08_js_render/challenge/answer/works.html)を見て、JSONに書き写す |
| `js/script.js` | ハンバーガーメニューとお問い合わせの入力チェックは完成済み。制作実績を読み込んで表示する部分（`createWorkCard`・`loadWorks`・絞り込み）がTODO |

`fetch()`を使うので、確認は`python -m http.server`で起動して行います（0節）。

### 必須要件

| 要件 | 使う節 |
|---|---|
| 一覧の項目を`data/works.json`に移す（1件ごとにタイトル・日付・説明・タグなど） | 1 |
| `works.html`の一覧部分は空の要素だけにして、`fetch()`で読み込んだデータからJavaScriptで作る。テキストは`textContent`で入れる | 2・5 |
| 読み込み中と、読み込みに失敗したときのメッセージを表示する | 3 |
| ステップ3で作った絞り込みが、JSONから作った項目でも動く | 5 |

### 自由課題（1つ以上）

| 例 | ヒント |
|---|---|
| 作品を新しい順に並べる | `works.sort((a, b) => b.date.localeCompare(a.date))` |
| 作品の件数をタグごとに表示する | `filter()`でタグごとに数える |
| ホームの「お知らせ」もJSONに分ける | `data/news.json`を作り、同じ方法で表示する |
| 選んだ絞り込みを`localStorage`に覚えておく | 次に開いたときも同じタグで絞り込まれた状態にする |

### 進め方のヒント

1. まず`works.html`に書いてある内容をそのまま`works.json`に写す（JSONのルールに注意）
2. [challenge/answer/js/script.js](challenge/answer/js/script.js)の`createWorkCard`・`loadWorks`を参考にする
3. 確認は必ず`python -m http.server`で起動して行う

### 動作確認：challenge/

| 確認する操作 | 確認したいこと |
|---|---|
| `python -m http.server`で起動し、`challenge/works.html`を開く | 5件の作品が、08_js_renderと同じ見た目で表示される |
| 「JavaScript」を押す | JavaScriptのタグを持つ3件だけが残る（JSONから作ったカードでも絞り込みが動く） |
| `fetch()`のファイル名をわざと間違えてリロードする（確認後は戻す） | 赤字で読み込み失敗のメッセージが表示される |

## 次のステップ

続きは [11_homepage](../11_homepage/) です。オリジナルHPを仕上げます。
