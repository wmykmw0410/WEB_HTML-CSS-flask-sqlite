# 07 イベント：クリック・入力に反応する

> フロントエンド編 ／ 前の章：[06_js_dom_basics](../06_js_dom_basics/) ／ 次の章：[08_js_forms](../08_js_forms/)

[06_js_dom_basics](../06_js_dom_basics/)では、`getElementById`で要素を取得し、`textContent`で書き換える「DOMの最小限」を学びました。ただし、その書き換えは、ページを開いたときに**1回だけ**実行されるものでした。

この章では、その書き換えを、ボタンの**クリック**や、入力欄への**入力**など、**ユーザーの操作に反応して**実行します。ユーザーの操作や、ページで起きたできごとを**イベント**と呼び、「イベントが起きたら、この関数を実行して」と登録することで、ページに動きを付けます。

| 節 | 学ぶこと | 練習問題 |
|---|---|---|
| 1 | `click`：クリックで文字を変える | 練習問題1〜3 |
| 2 | `input`：入力に反応する | 練習問題4〜6 |
| 3 | いろいろなイベント（イベントオブジェクト・ホバー・フォーカス） | 練習問題7・8 |

この章の練習問題は、**1問に1つのこと**だけを書く小さな問題に分けています。ページ下の「テストを実行」ボタンを押すと、イベントが自動で起こされて結果がConsoleに表示されるので、✅ を目安に進められます。

フォームの送信と入力チェックは、次の[08_js_forms](../08_js_forms/)で学びます。

## 前提

| チャプター | 使う知識 |
|---|---|
| 03_css_basics | `class`・`id`属性、クラスセレクタ（JavaScriptからクラスを付け外しして見た目を切り替える） |
| 05_js_basics | 変数・関数・`if`・コールバック関数・デバッグの方法 |
| 06_js_dom_basics | `getElementById`・`textContent` |

## 目次

1. [最初の動き：クリックで文字が変わる](#1-最初の動きクリックで文字が変わる)
2. [入力に反応する：文字数カウンター](#2-入力に反応する文字数カウンター)
3. [いろいろなイベント](#3-いろいろなイベント)

---

## フォルダ構成

```
01_frontend/07_js_events/
├── README.md
├── example/                      サンプル（1つのサンプル＝1つのフォルダ）
│   ├── 01_click/                 クリックで文字が変わる（addEventListener・textContent）
│   │   ├── index.html
│   │   └── script.js
│   ├── 02_input/                 文字数カウンター（inputイベント・value・classList.toggle）
│   │   ├── index.html
│   │   └── script.js
│   └── 03_events/                いろいろなイベント（イベントオブジェクト・ホバーとフォーカス）
│       ├── index.html
│       └── script.js
└── question/                     練習問題（8問。問題文はREADMEの各節の最後）
    ├── 01_click_text/            練習問題1：クリックで文字を変える
    ├── 02_click_count/           練習問題2：クリックの回数を数える
    ├── 03_click_toggle/          練習問題3：クリックでクラスを付け外しする
    ├── 04_input_text/            練習問題4：入力した文字をそのまま表示する
    ├── 05_input_counter/         練習問題5：文字数カウンターを作る
    ├── 06_debug_counter/         練習問題6：動かない文字数カウンターを直す（デバッグ）
    ├── 07_event_object/          練習問題7：イベントオブジェクトを使う
    ├── 08_hover_focus/           練習問題8：ホバーとフォーカスで説明を出す
    └── answer/                   解答（問題と同じ名前のフォルダ）
        ├── 01_click_text/
        ├── 02_click_count/
        ├── 03_click_toggle/
        ├── 04_input_text/
        ├── 05_input_counter/
        ├── 06_debug_counter/
        ├── 07_event_object/
        └── 08_hover_focus/
```

---

## 1. 最初の動き：クリックで文字が変わる

> [example/01_click/index.html](example/01_click/index.html) / [example/01_click/script.js](example/01_click/script.js)

ボタンを押すと文字が変わる、というシンプルな動きを作ります。Webページの「動き」の多くは、次の3ステップの組み合わせでできています。①と③は[06_js_dom_basics](../06_js_dom_basics/)で試したとおりで、**この節で新しく学ぶのは②（イベントの登録）だけ**です。

```
① 取得    動かしたい要素を見つける          document.getElementById('message')
② 登録    「〜されたら、この関数を呼んで」と登録   button.addEventListener('click', 関数)
③ 書き換え  関数の中で、画面を書き換える          message.textContent = '押されました'
```

```javascript
const helloButton = document.getElementById('hello-button');   // ① 取得
const message = document.getElementById('message');

let count = 0;

helloButton.addEventListener('click', () => {                  // ② 登録（コールバック関数）
    count++;
    message.textContent = `${count}回押されました`;               // ③ 書き換え
});
```

### ポイント

| 書き方 | 説明 |
|---|---|
| `document.getElementById('id')` | HTMLの`id`が一致する要素を1つ取得する（[06_js_dom_basics](../06_js_dom_basics/)）。DOMの詳しい操作は[09_js_dom](../09_js_dom/)で学ぶ |
| `要素.addEventListener('click', 関数)` | クリックされたときに、関数を呼び出してもらう（[05_js_basicsのコールバック関数](../05_js_basics/#コールバック関数)） |
| `要素.textContent` | 要素の中の文字を取得・書き換える。書き換えると画面にすぐ反映される（[06_js_dom_basics](../06_js_dom_basics/)） |
| `要素.classList.toggle('クラス名')` | クラスが無ければ付け、あれば外す。CSSのクラスと組み合わせて、見た目を切り替える |

### 動作確認

`example/01_click/index.html`をブラウザで開いて確認します。

| 確認する操作 | 確認したいこと |
|---|---|
| 「押してみてください」を押す | 下の文字が「1回押されました」に変わる。押すたびに回数が増える |
| 「色を切り替える」を押す | ボックスの背景色が変わる。もう一度押すと戻る（`classList.toggle`） |
| 開発者ツールのElementsで、ボックスを押しながら見る | `class="output highlight"`のように、`highlight`が付いたり外れたりしている |

**動かないときは**：Consoleに`Cannot read properties of null`と出たら、`getElementById`の`id`の綴りと、`<script>`を`</body>`の直前に置いているかを確かめます（[05_js_basicsの0節](../05_js_basics/#0-javascriptの読み込み方とデバッグ)）。

### 練習問題1：クリックで文字を変える

> 問題：[question/01_click_text/index.html](question/01_click_text/index.html)・[question/01_click_text/script.js](question/01_click_text/script.js) ｜ 解答：[question/answer/01_click_text/index.html](question/answer/01_click_text/index.html)・[question/answer/01_click_text/script.js](question/answer/01_click_text/script.js)

<details>
<summary>問題の内容を開く</summary>

`01_click_text/script.js`の`TODO 1`に、クリックされたときの処理を書きます。`01_click_text/index.html`をブラウザで開き、ページ下の「テストを実行」ボタンを押すと、イベントが自動で起こされ、Consoleに ✅（正しい）／❌（間違い）が表示されます。自分でも画面を操作して、動きを確かめます。**1問ずつ**書いて確かめ、その問題が ✅ になってから、次に進みます（まだ書いていない問題が ❌ になるのは正常です）。

| # | やること |
|---|---|
| 1 | `helloButton`がクリックされたら、`message`の文字を「押されました」に書き換える |

| # | ヒント |
|---|---|
| 1 | `要素.addEventListener('click', () => { ... })`の関数の中で、`textContent`を書き換える（①取得は書いてあるので、②登録と③書き換えを書く） |

</details>

### 練習問題2：クリックの回数を数える

> 問題：[question/02_click_count/index.html](question/02_click_count/index.html)・[question/02_click_count/script.js](question/02_click_count/script.js) ｜ 解答：[question/answer/02_click_count/index.html](question/answer/02_click_count/index.html)・[question/answer/02_click_count/script.js](question/answer/02_click_count/script.js)

<details>
<summary>問題の内容を開く</summary>

`02_click_count/script.js`の`TODO 1`・`TODO 2`に、回数を覚えて表示する処理を書きます。`02_click_count/index.html`をブラウザで開き、ページ下の「テストを実行」ボタンを押すと、イベントが自動で起こされ、Consoleに ✅（正しい）／❌（間違い）が表示されます。自分でも画面を操作して、動きを確かめます。**1問ずつ**書いて確かめ、その問題が ✅ になってから、次に進みます（まだ書いていない問題が ❌ になるのは正常です）。

| # | やること |
|---|---|
| 1 | 回数を入れる変数`count`を、0から始めて用意する |
| 2 | `countButton`がクリックされるたびに`count`を1増やし、「1回押されました」「2回押されました」…と表示する |

| # | ヒント |
|---|---|
| 1 | あとで値を増やすので`let`。**関数の外**に置く（関数の中に置くと、押すたびに0に戻ってしまう） |
| 2 | `count++;`で1増やしてから、テンプレートリテラルで表示する |

</details>

### 練習問題3：クリックでクラスを付け外しする

> 問題：[question/03_click_toggle/index.html](question/03_click_toggle/index.html)・[question/03_click_toggle/script.js](question/03_click_toggle/script.js) ｜ 解答：[question/answer/03_click_toggle/index.html](question/answer/03_click_toggle/index.html)・[question/answer/03_click_toggle/script.js](question/answer/03_click_toggle/script.js)

<details>
<summary>問題の内容を開く</summary>

`03_click_toggle/script.js`の`TODO 1`に書きます。`03_click_toggle/index.html`をブラウザで開き、ページ下の「テストを実行」ボタンを押すと、イベントが自動で起こされ、Consoleに ✅（正しい）／❌（間違い）が表示されます。自分でも画面を操作して、動きを確かめます。**1問ずつ**書いて確かめ、その問題が ✅ になってから、次に進みます（まだ書いていない問題が ❌ になるのは正常です）。

| # | やること |
|---|---|
| 1 | `toggleButton`がクリックされるたびに、`box`に`highlight`クラスを付けたり外したりする（CSSの`.highlight`で背景が黄色になる） |

| # | ヒント |
|---|---|
| 1 | `要素.classList.toggle('クラス名')`は、クラスが無ければ付け、あれば外す |

</details>

---

## 2. 入力に反応する：文字数カウンター

> [example/02_input/index.html](example/02_input/index.html) / [example/02_input/script.js](example/02_input/script.js)

入力欄に文字を打つたびに、文字数を表示します。クリックではなく**`input`イベント**を使い、入力欄の中身（`.value`）を読み取ります。

```javascript
const textarea = document.getElementById('body');
const counter = document.getElementById('count');

textarea.addEventListener('input', () => {        // 入力のたびに（1文字ごとに）呼ばれる
    const length = textarea.value.length;          // 入力欄の中身は .value

    counter.textContent = length;                  // 文字数を表示する

    counter.classList.toggle('over', length > 450);  // 450文字を超えたら 'over' クラスを付ける
});
```

### ポイント

| 書き方 | 説明 |
|---|---|
| `'input'`イベント | 入力欄の値が変わるたびに発生する（クリックなら`'click'`） |
| `要素.value` | 入力欄（`input`・`textarea`・`select`）に入力されている値 |
| `classList.toggle('クラス名', 条件)` | 第2引数の条件が`true`ならクラスを付け、`false`なら外す |

### よくあるエラー

| 画面・Consoleの様子 | 原因 |
|---|---|
| `Cannot read properties of null (reading 'addEventListener')` | `getElementById`の`id`の綴りが違う／HTMLに`id`が無い／`<script>`が`</body>`より前にある（[05_js_basicsの0節](../05_js_basics/#0-javascriptの読み込み方とデバッグ)） |
| 表示が`undefined`になる | `lenght`のようにプロパティ名を打ち間違えている |
| 文字を変えたのに画面が変わらない | 取得した要素が別の要素になっている（`id`の重複・取得した変数を間違えている） |

### 動作確認

| 確認する操作 | 確認したいこと |
|---|---|
| テキストエリアに1文字入力する | `0 / 500文字`の`0`が`1`に変わる（`input`イベントのたびに`textContent`が書き換わる） |
| 文字を消していく（Backspace） | 文字数の表示もリアルタイムに減っていく |
| 450文字を超える文章を貼り付ける | 451文字目に達した瞬間、文字数の表示が赤字になる（`classList.toggle('over', length > 450)`） |
| 451文字以上の状態から文字を消して450文字以下に戻す | 赤字が元の色（グレー）に戻る（`toggle`は条件が`false`になるとクラスを自動で外す） |
| `textarea`の`maxlength="500"`を超えて入力しようとする | それ以上は入力できない（ブラウザの`maxlength`属性による制限で、JavaScriptのコードとは別の仕組み） |

### 練習問題4：入力した文字をそのまま表示する

> 問題：[question/04_input_text/index.html](question/04_input_text/index.html)・[question/04_input_text/script.js](question/04_input_text/script.js) ｜ 解答：[question/answer/04_input_text/index.html](question/answer/04_input_text/index.html)・[question/answer/04_input_text/script.js](question/answer/04_input_text/script.js)

<details>
<summary>問題の内容を開く</summary>

`04_input_text/script.js`の`TODO 1`に書きます。`04_input_text/index.html`をブラウザで開き、ページ下の「テストを実行」ボタンを押すと、イベントが自動で起こされ、Consoleに ✅（正しい）／❌（間違い）が表示されます。自分でも画面を操作して、動きを確かめます。**1問ずつ**書いて確かめ、その問題が ✅ になってから、次に進みます（まだ書いていない問題が ❌ になるのは正常です）。

| # | やること |
|---|---|
| 1 | `nameInput`に文字が入力されるたび（`input`イベント）に、入力された文字（`value`）を`nameOutput`に表示する |

| # | ヒント |
|---|---|
| 1 | イベント名は`'input'`。入力欄の中身は`nameInput.value` |

</details>

### 練習問題5：文字数カウンターを作る

> 問題：[question/05_input_counter/index.html](question/05_input_counter/index.html)・[question/05_input_counter/script.js](question/05_input_counter/script.js) ｜ 解答：[question/answer/05_input_counter/index.html](question/answer/05_input_counter/index.html)・[question/answer/05_input_counter/script.js](question/answer/05_input_counter/script.js)

<details>
<summary>問題の内容を開く</summary>

`05_input_counter/script.js`の`TODO 1`・`TODO 2`に書きます。`05_input_counter/index.html`をブラウザで開き、ページ下の「テストを実行」ボタンを押すと、イベントが自動で起こされ、Consoleに ✅（正しい）／❌（間違い）が表示されます。自分でも画面を操作して、動きを確かめます。**1問ずつ**書いて確かめ、その問題が ✅ になってから、次に進みます（まだ書いていない問題が ❌ になるのは正常です）。

| # | やること |
|---|---|
| 1 | `textarea`に入力されるたびに、入力された文字数を`counter`に表示する |
| 2 | 文字数が10を超えたら、`counter`に`over`クラスを付ける（10以下に戻ったら外す。CSSの`.over`で赤字になる） |

| # | ヒント |
|---|---|
| 1 | 文字数は`textarea.value.length` |
| 2 | `classList.toggle('over', 条件)`は、第2引数の条件が`true`ならクラスを付け、`false`なら外す |

</details>

### 練習問題6：動かない文字数カウンターを直す（デバッグ）

> 問題：[question/06_debug_counter/index.html](question/06_debug_counter/index.html)・[question/06_debug_counter/script.js](question/06_debug_counter/script.js) ｜ 解答：[question/answer/06_debug_counter/index.html](question/answer/06_debug_counter/index.html)・[question/answer/06_debug_counter/script.js](question/answer/06_debug_counter/script.js)

<details>
<summary>問題の内容を開く</summary>

`06_debug_counter/index.html`は「入力した文字数を表示する」はずのページですが、動きません。バグは3つあります（HTMLに1つ、`06_debug_counter/script.js`に2つ）。[05_js_basicsの0節](../05_js_basics/#0-javascriptの読み込み方とデバッグ)で学んだ、ConsoleのエラーメッセージとSourcesパネルのブレークポイントを使って、原因を見つけて直します。

| # | 進め方 |
|---|---|
| 1 | まずConsoleを開いてリロードし、赤字のエラーを読む（何行目の、何が`null` / `undefined`か） |
| 2 | エラーを1つ直したらリロードし、次のエラーを見る |
| 3 | エラーは出ないのに表示がおかしいときは、Sourcesパネルで`06_debug_counter/script.js`を開き、行番号をクリックしてブレークポイントを置く。入力して止まったら、変数にマウスを乗せて値を確認する |

| 確認する操作 | 確認したいこと |
|---|---|
| 文字を入力・削除する | 入力するたびに「◯文字」が正しく増減する |
| 21文字以上入力する | 文字数が赤字になる |
| Consoleを見る | エラーが出ていない |

</details>

---

## 3. いろいろなイベント

> [example/03_events/index.html](example/03_events/index.html) / [example/03_events/script.js](example/03_events/script.js)

1節の`click`、2節の`input`のほかにも、さまざまなイベントがあります。この節では、イベントの種類と、イベントが起きたときの情報（イベントオブジェクト）、ホバーとフォーカスを扱います。

### よく使うイベント

| イベント名 | 発生するタイミング | 主な対象 |
|---|---|---|
| `click` | クリックされたとき | ボタン・リンク |
| `input` | 入力欄の値が変わるたび（1文字ごと） | `input`・`textarea` |
| `change` | 値が確定したとき（チェックボックスの切り替え・`select`の選択など） | `select`・チェックボックス |
| `keydown` | キーが押されたとき | 入力欄・ページ全体 |
| `mouseenter` / `mouseleave` | マウスが要素に入ったとき / 出たとき（ホバー） | どの要素でも |
| `focus` / `blur` | 要素が選ばれた（フォーカスされた）とき / 外れたとき | ボタン・リンク・入力欄 |
| `submit` | フォームが送信されようとしたとき（ボタンのクリック・Enterキー） | `form` |
| `reset` | フォームが初期状態に戻されようとしたとき（`type="reset"`のボタン） | `form` |

`submit`と`reset`は、次の[08_js_forms](../08_js_forms/)で使います。

### イベントオブジェクト

コールバック関数は、引数で**イベントオブジェクト**を受け取れます。何が起きたかの情報が入っています。

```javascript
button.addEventListener('click', (event) => {
    console.log(event.type);   // 'click'（イベントの種類）
});

input.addEventListener('keydown', (event) => {
    console.log(event.key);    // 押されたキー（'a'、'Enter' など）
});
```

| プロパティ | 説明 |
|---|---|
| `event.type` | イベントの種類（`'click'`など） |
| `event.key` | 押されたキー（キーボードのイベント） |
| `event.preventDefault()` | ブラウザの**既定の動作**を止める（[08_js_forms](../08_js_forms/)で説明） |

### ホバーとフォーカス

マウスを要素に乗せること（**ホバー**）に反応するには、`mouseenter`と`mouseleave`を使います。ここでは、ボタンに乗せたときに、説明（ツールチップ）の文字を出します。説明の出し入れは、0節の`textContent`だけで行います（文字を入れると表示され、空にすると隠れます）。

```html
<button type="button" id="tip-button">新規作成</button>
<p id="tip"></p>    <!-- 最初は空。CSSの :empty で、空のときは見えないようにしてある -->
```

```javascript
button.addEventListener('mouseenter', () => { tip.textContent = 'メモを新しく作ります'; });   // 乗せたら表示
button.addEventListener('mouseleave', () => { tip.textContent = ''; });                      // 外したら隠す
button.addEventListener('focus', () => { tip.textContent = 'メモを新しく作ります'; });        // キーボードで選ばれたときも表示
button.addEventListener('blur', () => { tip.textContent = ''; });
```

| 使い分け | 例 |
|---|---|
| 見た目を変えるだけなら、CSSの`:hover`・`:focus-visible`（03_css_basics 3節・04_css_layout 6節） | ボタンの色を変える・影を付ける |
| 別の要素を出す・中身を書き換える・処理を止めるなら、JavaScriptの`mouseenter`/`mouseleave` | ツールチップを表示する・スライドショーの自動再生を止める（11_js_ui 4節） |

スマホにはマウスが無いので、ホバーは起こりません。ホバーでしか見られない情報を作らず、`focus`やクリックでも同じ情報が見られるようにしておくと、キーボードやタッチ操作の人にも届きます。

### 動作確認

`example/03_events/index.html`をブラウザで開いて確認します。

| 確認する操作 | 確認したいこと |
|---|---|
| 「クリックしてみる」を押す | `click イベントが起きました`と表示される（`event.type`） |
| 下の入力欄でキーを押す | 押したキーの名前（`a`・`Enter`・`Shift`など）が表示される（`event.key`） |
| 「新規作成」ボタンにマウスを乗せる・外す | 説明が表示され、外すと消える |
| Tabキーで「新規作成」ボタンを選ぶ・外す | マウスを使わなくても、同じように説明が表示され、消える |

### 練習問題7：イベントオブジェクトを使う

> 問題：[question/07_event_object/index.html](question/07_event_object/index.html)・[question/07_event_object/script.js](question/07_event_object/script.js) ｜ 解答：[question/answer/07_event_object/index.html](question/answer/07_event_object/index.html)・[question/answer/07_event_object/script.js](question/answer/07_event_object/script.js)

<details>
<summary>問題の内容を開く</summary>

`07_event_object/script.js`の`TODO 1`・`TODO 2`に書きます。`07_event_object/index.html`をブラウザで開き、ページ下の「テストを実行」ボタンを押すと、イベントが自動で起こされ、Consoleに ✅（正しい）／❌（間違い）が表示されます。自分でも画面を操作して、動きを確かめます。**1問ずつ**書いて確かめ、その問題が ✅ になってから、次に進みます（まだ書いていない問題が ❌ になるのは正常です）。

| # | やること |
|---|---|
| 1 | `eventButton`がクリックされたら、イベントの種類（`event.type`）を`typeOutput`に表示する（`click`と表示される） |
| 2 | `keyInput`でキーが押されたら（`keydown`）、「押されたキー：a」のように、押されたキー（`event.key`）を`keyOutput`に表示する |

| # | ヒント |
|---|---|
| 1・2 | コールバック関数の引数（`(event) => { ... }`）が、イベントオブジェクト |

</details>

### 練習問題8：ホバーとフォーカスで説明を出す

> 問題：[question/08_hover_focus/index.html](question/08_hover_focus/index.html)・[question/08_hover_focus/script.js](question/08_hover_focus/script.js) ｜ 解答：[question/answer/08_hover_focus/index.html](question/answer/08_hover_focus/index.html)・[question/answer/08_hover_focus/script.js](question/answer/08_hover_focus/script.js)

<details>
<summary>問題の内容を開く</summary>

`08_hover_focus/script.js`の`TODO 1`・`TODO 2`に書きます。説明（`tip`）は、最初は空で、空のときはCSSの`:empty`で隠れています。`08_hover_focus/index.html`をブラウザで開き、ページ下の「テストを実行」ボタンを押すと、イベントが自動で起こされ、Consoleに ✅（正しい）／❌（間違い）が表示されます。自分でも画面を操作して、動きを確かめます。**1問ずつ**書いて確かめ、その問題が ✅ になってから、次に進みます（まだ書いていない問題が ❌ になるのは正常です）。

| # | やること |
|---|---|
| 1 | マウスが`tipButton`に乗ったとき（`mouseenter`）は、`tip`の文字を「メモを新しく作ります」にし、外れたとき（`mouseleave`）は空にする |
| 2 | キーボードで`tipButton`が選ばれたとき（`focus`）も同じ説明を出し、外れたとき（`blur`）は空にする |

| # | ヒント |
|---|---|
| 1・2 | 4つのイベントを、それぞれ`addEventListener`で登録する。文字を入れると表示され、`''`（空文字）で隠れる |
| 2 | ホバーだけだと、キーボードを使う人には説明が届かない。`focus`とセットで書く |

</details>

---

## 次のステップ

続きは [08_js_forms](../08_js_forms/) です。フォームの送信を止めて、入力をチェックします。
