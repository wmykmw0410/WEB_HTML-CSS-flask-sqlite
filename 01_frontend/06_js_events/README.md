# 06 イベント：ブラウザで動かす

> フロントエンド編 ／ 前の章：[05_js_basics](../05_js_basics/) ／ 次の章：[07_js_dom](../07_js_dom/)

[05_js_basics](../05_js_basics/)で学んだ最小限の文法を使って、**ブラウザ上で動くもの**を作ります。ボタンを押すと文字が変わる、入力すると文字数が変わる、フォームを送る前に入力をチェックする、といった動きを、**イベント**（クリック・入力・送信など）への反応として作ります。

最初は「要素を取得する→イベントを登録する→文字を書き換える」の3ステップだけを使います。要素の取得や書き換えの詳しい方法（DOM操作）は、次の[07_js_dom](../07_js_dom/)で学びます。

## 前提

| チャプター | 使う知識 |
|---|---|
| 02_html_semantic_form | フォーム部品 |
| 03_css_basics | `class`・`id`属性、クラスセレクタ（JavaScriptからクラスを付け外しして見た目を切り替える） |
| 05_js_basics | 変数・関数・`if`・`null`と真偽の判定・コールバック関数・デバッグの方法 |

## 目次

1. [最初の動き：クリックで文字が変わる](#1-最初の動きクリックで文字が変わる)
2. [入力に反応する：文字数カウンター](#2-入力に反応する文字数カウンター)
3. [いろいろなイベントとフォーム](#3-いろいろなイベントとフォーム)

---

## フォルダ構成

```
01_frontend/06_js_events/
├── README.md
├── example/                      サンプル（1つのサンプル＝1つのフォルダ）
│   ├── 01_click/                 クリックで文字が変わる（getElementById・addEventListener・textContent）
│   │   ├── index.html
│   │   └── script.js
│   ├── 02_input/                 文字数カウンター（inputイベント・value・classList.toggle）
│   │   ├── index.html
│   │   └── script.js
│   └── 03_events/                イベント（イベントオブジェクト・ホバーとフォーカス・submit・preventDefault・confirm）
│       ├── index.html
│       └── script.js
└── question/                     練習問題（2問。問題文はREADMEの各節の最後）
    ├── 01_debug_counter/         練習問題1：動かない文字数カウンターを直す（デバッグ）
    │   ├── index.html
    │   └── script.js
    ├── 02_form_validation/       練習問題2：フォームの送信前に入力をチェックする
    │   ├── index.html
    │   └── script.js
    └── answer/                   解答（問題と同じ名前のフォルダ。中のファイル構成も問題と同じ）
        ├── 01_debug_counter/
        └── 02_form_validation/
```

---

## 1. 最初の動き：クリックで文字が変わる

> [example/01_click/index.html](example/01_click/index.html) / [example/01_click/script.js](example/01_click/script.js)

ボタンを押すと文字が変わる、というシンプルな動きを作ります。Webページの「動き」の多くは、次の3ステップの組み合わせでできています。

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
| `document.getElementById('id')` | HTMLの`id`が一致する要素を1つ取得する。ページの要素を、JavaScriptで操作できる形にしたものが**DOM**（Document Object Model）で、詳しくは[07_js_dom](../07_js_dom/)で学ぶ |
| `要素.addEventListener('click', 関数)` | クリックされたときに、関数を呼び出してもらう（[05_js_basicsのコールバック関数](../05_js_basics/#コールバック関数)） |
| `要素.textContent` | 要素の中の文字を取得・書き換える。書き換えると画面にすぐ反映される |
| `要素.classList.toggle('クラス名')` | クラスが無ければ付け、あれば外す。CSSのクラスと組み合わせて、見た目を切り替える |

### 動作確認

`example/01_click/index.html`をブラウザで開いて確認します。

| 確認する操作 | 確認したいこと |
|---|---|
| 「押してみてください」を押す | 下の文字が「1回押されました」に変わる。押すたびに回数が増える |
| 「色を切り替える」を押す | ボックスの背景色が変わる。もう一度押すと戻る（`classList.toggle`） |
| 開発者ツールのElementsで、ボックスを押しながら見る | `class="output highlight"`のように、`highlight`が付いたり外れたりしている |

**動かないときは**：Consoleに`Cannot read properties of null`と出たら、`getElementById`の`id`の綴りと、`<script>`を`</body>`の直前に置いているかを確かめます（[05_js_basicsの0節](../05_js_basics/#0-javascriptの読み込み方とデバッグ)）。

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

### 練習問題1：動かない文字数カウンターを直す（デバッグ）

> 問題：[question/01_debug_counter/index.html](question/01_debug_counter/index.html)・[question/01_debug_counter/script.js](question/01_debug_counter/script.js) ｜ 解答：[question/answer/01_debug_counter/index.html](question/answer/01_debug_counter/index.html)・[question/answer/01_debug_counter/script.js](question/answer/01_debug_counter/script.js)

<details>
<summary>問題の内容を開く</summary>

`01_debug_counter/index.html`は「入力した文字数を表示する」はずのページですが、動きません。バグは3つあります（HTMLに1つ、`01_debug_counter/script.js`に2つ）。[05_js_basicsの0節](../05_js_basics/#0-javascriptの読み込み方とデバッグ)で学んだ、ConsoleのエラーメッセージとSourcesパネルのブレークポイントを使って、原因を見つけて直します。

| # | 進め方 |
|---|---|
| 1 | まずConsoleを開いてリロードし、赤字のエラーを読む（何行目の、何が`null` / `undefined`か） |
| 2 | エラーを1つ直したらリロードし、次のエラーを見る |
| 3 | エラーは出ないのに表示がおかしいときは、Sourcesパネルで`01_debug_counter/script.js`を開き、行番号をクリックしてブレークポイントを置く。入力して止まったら、変数にマウスを乗せて値を確認する |

| 確認する操作 | 確認したいこと |
|---|---|
| 文字を入力・削除する | 入力するたびに「◯文字」が正しく増減する |
| 21文字以上入力する | 文字数が赤字になる |
| Consoleを見る | エラーが出ていない |

</details>



---

## 3. いろいろなイベントとフォーム

> [example/03_events/index.html](example/03_events/index.html) / [example/03_events/script.js](example/03_events/script.js)

1節の`click`、2節の`input`のほかにも、さまざまなイベントがあります。この節では、イベントの種類と、イベントが起きたときの情報（イベントオブジェクト）、ホバーとフォーカス、そしてフォームの送信を扱います。

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

### イベントオブジェクト

コールバック関数は、引数で**イベントオブジェクト**を受け取れます。何が起きたかの情報が入っています。

```javascript
document.getElementById('buttons').addEventListener('click', (event) => {
    const button = event.target.closest('button');   // 実際にクリックされた要素から、最も近い button を探す
    if (!button) {
        return;
    }
    console.log(button.dataset.color, event.type);
});

input.addEventListener('keydown', (event) => {
    console.log(event.key);   // 押されたキー（'a'、'Enter' など）
});
```

| プロパティ・メソッド | 説明 |
|---|---|
| `event.target` | イベントが実際に起きた要素 |
| `event.type` | イベントの種類（`'click'`など） |
| `event.key` | 押されたキー（キーボードのイベント） |
| `event.preventDefault()` | ブラウザの**既定の動作**を止める（下で説明） |
| `要素.closest('セレクタ')` | 自分または祖先から、セレクタに合う最も近い要素を探す |

上の例の`button.dataset.color`は`data-color`属性の値、`closest()`・`hidden`は、要素を調べたり表示を切り替えたりするための道具です。ここでは「こう書くと動く」と読み進めて構いません。くわしくは次の[07_js_dom](../07_js_dom/)で学びます。

上の例のように、ボタン1つずつではなく**親要素に1回だけ**イベントを登録し、`event.target`で「どのボタンが押されたか」を判定する書き方もよく使われます（イベントは子から親へ伝わるため）。

### ホバーとフォーカス

マウスを要素に乗せること（**ホバー**）に反応するには、`mouseenter`と`mouseleave`を使います。

```javascript
button.addEventListener('mouseenter', () => { tip.hidden = false; });   // 乗せたら表示
button.addEventListener('mouseleave', () => { tip.hidden = true; });    // 外したら隠す
button.addEventListener('focus', () => { tip.hidden = false; });        // キーボードで選ばれたときも表示
button.addEventListener('blur', () => { tip.hidden = true; });
```

| 使い分け | 例 |
|---|---|
| 見た目を変えるだけなら、CSSの`:hover`・`:focus-visible`（03_css_basics 3節・04_css_layout 6節） | ボタンの色を変える・影を付ける |
| 中身を書き換える・別の要素を出す・処理を止めるなら、JavaScriptの`mouseenter`/`mouseleave` | ツールチップを作って表示する・スライドショーの自動再生を止める（09_js_ui 4節） |

| イベント | 違い |
|---|---|
| `mouseenter` / `mouseleave` | その要素に入ったとき・出たときに**1回だけ**発生する。普段はこちらを使う |
| `mouseover` / `mouseout` | 中の子要素に移るたびにも発生する（イベントが子から親へ伝わるため） |
| `focus` / `blur` | その要素自身が選ばれた・外れたときだけ発生する |
| `focusin` / `focusout` | 中の子要素が選ばれた・外れたときにも発生する（09_js_ui 4節で使う） |

スマホにはマウスが無いので、ホバーは起こりません。ホバーでしか見られない情報を作らず、`focus`やクリックでも同じ情報が見られるようにしておくと、キーボードやタッチ操作の人にも届きます。

### 入力チェックで使う文法

次の`preventDefault()`の例から、入力チェックのために文字列の加工と、条件を組み合わせる書き方を使います。先に、この章で初めて出てくる書き方をまとめます。

#### 文字列の前後の空白を除く：`trim()`

```javascript
'  メモ '.trim();   // 'メモ'（前後の空白・改行を取り除く）
'   '.trim();       // ''（空白だけの入力は、空文字になる）
```

HTMLの`required`は空欄を防げますが、空白だけの入力（`'   '`）は通ってしまいます。`trim()`してから空かどうかを調べれば、空白だけの入力も防げます。

#### 条件を組み合わせる：`&&`・`||`・`!`

| 書き方 | 意味 | 例 |
|---|---|---|
| `A && B`（かつ） | 両方が真のときだけ真 | `hasInput && !confirm('…')` |
| `A \|\| B`（または） | どちらかが真なら真 | `selected === 'all' \|\| card.dataset.category === selected` |
| `!A`（でない） | 真と偽を入れ替える | `!categories.includes('仕事')` |

`&&`と`||`は、左から順に評価して、結果が決まった時点で右側を評価しません。

#### 値を条件で選ぶ：三項演算子 `条件 ? A : B`

条件が真なら`A`、偽なら`B`になる式です。`if`/`else`で値を選ぶ処理を1行で書けます。

```javascript
const label = isDone ? '完了' : '未完了';

// 上は次の if / else と同じ
let label;
if (isDone) {
    label = '完了';
} else {
    label = '未完了';
}

const titleMessage = title ? '' : 'タイトルを入力してください';   // 空でなければエラー文なし
```

#### 🐍 Pythonとの違い

```python
# Python
title = title.strip()                                       # trim に当たる
if has_input and not confirm('…'):                          # and / not
    ...
label = '完了' if is_done else '未完了'                        # 三項演算子は「値 if 条件 else 値」
```

| | Python | JavaScript |
|---|---|---|
| 前後の空白を除く | `s.strip()` | `s.trim()` |
| かつ／または／でない | `and` / `or` / `not` | `&&` / `\|\|` / `!`（**単語ではなく記号**） |
| 値を条件で選ぶ | `A if 条件 else B`（**値が先**） | `条件 ? A : B`（**条件が先**） |

### 既定の動作を止める：`preventDefault()`

ブラウザには、イベントごとに決まった「既定の動作」があります。

| 操作 | 既定の動作 |
|---|---|
| フォームの`submit` | 入力内容をサーバーに送信して、ページを移動する |
| リンクの`click` | `href`のページに移動する |
| フォームの`reset` | 入力内容を初期状態に戻す |

`event.preventDefault()`を呼ぶと、この既定の動作を止められます。送信前の入力チェックによく使います。

```javascript
form.addEventListener('submit', (event) => {
    if (!titleInput.value.trim()) {
        event.preventDefault();   // 送信を止める
        titleError.textContent = 'タイトルを入力してください';
    }
});
```

ボタンの`click`ではなくフォームの`submit`を監視すると、Enterキーでの送信も同じように扱えます。

> HTMLの`required`でも空欄は防げますが、空白だけの入力（`'   '`）は通ってしまいます。JavaScriptなら`trim()`を使った細かいチェックができます。ただし、ブラウザ側のチェックは開発者ツールなどで無効にできるので、`02_backend/09_forms`で**サーバー（Python）側でも必ずチェック**します。

### `confirm()`で確認する

```javascript
link.addEventListener('click', (event) => {
    if (!confirm('外部サイトに移動します。よろしいですか？')) {
        event.preventDefault();   // 「キャンセル」なら移動を止める
    }
});
```

`confirm('メッセージ')`は確認ダイアログを表示し、「OK」なら`true`、「キャンセル」なら`false`を返します。

Flaskのテンプレートでは、これをHTMLの属性（`onsubmit`）で短く書くこともあります。

```html
<button type="submit" onclick="return confirm('削除しますか？')">削除</button>
```

`onclick`属性の中で`false`を`return`すると、`preventDefault()`と同じく既定の動作（ここではフォームの送信）が止まります。つまり「キャンセル」を押すと`confirm()`が`false`を返し、削除のリクエストが送られません。

### 動作確認：イベントを受け取れているか

`example/03_events/index.html`をブラウザで開いて確認します。

| 確認する操作 | 確認したいこと |
|---|---|
| 「赤」「青」「緑」のボタンを押す | 押したボタンの色の名前と`event.type = click`が表示される（親要素の1つのリスナーで3つのボタンを処理している） |
| 下の入力欄でキーを押す | 押したキーの名前（`a`・`Enter`・`Shift`など）が表示される |
| タイトルを空、または空白だけにして「保存する」を押す | 送信されず、赤字のエラーメッセージが表示される |
| タイトルを入力して「保存する」、またはEnterキーを押す | 「◯◯を送信します」と表示される（`submit`を監視しているのでEnterキーでも同じ処理が動く） |
| 「MDNへ移動する」をクリックして「キャンセル」を選ぶ | ページが移動しない |
| 「削除」ボタンを押して「キャンセル」を選ぶ | フォームが送信されない（URLの末尾に`#`が付かない） |
| 「4. ホバーとフォーカス」のボタンにマウスを乗せる・Tabキーで移動する | どちらの方法でも、ボタンの上に説明（ツールチップ）が表示され、外れると消える |
| 点線の箱の中で、子要素の上を行き来する | `mouseover`の回数だけがどんどん増え、`mouseenter`は箱に入ったときだけ増える |

### 練習問題2：フォームの送信前に入力をチェックする

> 問題：[question/02_form_validation/index.html](question/02_form_validation/index.html)・[question/02_form_validation/script.js](question/02_form_validation/script.js) ｜ 解答：[question/answer/02_form_validation/index.html](question/answer/02_form_validation/index.html)・[question/answer/02_form_validation/script.js](question/answer/02_form_validation/script.js)

<details>
<summary>問題の内容を開く</summary>

`02_form_validation/index.html`のフォームに、`submit`・`preventDefault`・`confirm`を使った入力チェックを付けます。HTMLの`required`などは、「JavaScriptだけで」チェックする練習のため、あえて付けていません。

| # | 仕様 |
|---|---|
| 1 | 「保存する」を押したとき（フォームの`submit`）に次をチェックし、問題があれば送信を止めて、各入力欄の下の`.error`にメッセージを表示する。問題が無い欄のメッセージは消す。タイトルが空白だけ・空なら「タイトルを入力してください」、本文が前後の空白を除いて10文字未満なら「本文は10文字以上で入力してください」 |
| 2 | エラーのある入力欄には`invalid`クラスを付ける（CSSで赤枠になる）。直ったら外す |
| 3 | すべて問題なければ、送信は止めたうえで`#result`に「保存しました：（タイトル）」と表示する（このページには送信先が無いため。`02_backend/09_forms`以降は実際にFlaskへ送信する） |
| 4 | 「クリア」ボタン（`type="reset"`）を押したとき、何か入力されていれば`confirm('入力内容を消しますか？')`で確認し、キャンセルなら消さない |

`02_form_validation/script.js`には次の3つを書きます。

| # | やること | ヒント |
|---|---|---|
| 1 | `showError(input, errorEl, message)`：エラー表示を切り替える関数。`message`が空文字なら、メッセージを消して`invalid`クラスを外す。`message`があれば、表示して`invalid`クラスを付ける | `errorEl.textContent = message;` / `input.classList.toggle('invalid', 条件)` |
| 2 | フォームの`submit`イベントで入力をチェックする（仕様1〜3） | `event.preventDefault()`で送信を止める。エラー文は`条件 ? 'エラー文' : ''`の形（三項演算子）で書くと短くなる |
| 3 | フォームの`reset`イベントで確認する（仕様4）。消す場合は、エラー表示と`#result`も消す | `reset`イベントでも`preventDefault()`で既定の動作（入力を消す）を止められる |

| 確認する操作 | 確認したいこと |
|---|---|
| 何も入力せずに「保存する」を押す | 2つの欄の下にエラーが表示され、枠が赤くなる |
| 正しく入力して「保存する」を押す | エラーが消え、「保存しました：（タイトル）」と表示される |
| 入力した状態で「クリア」を押し、確認でキャンセルする | 入力内容が残っている |

</details>

---

## 次のステップ

続きは [07_js_dom](../07_js_dom/) です。ここまで使ってきた「要素の取得と書き換え」を、`querySelector`・属性・要素の作成など、DOM操作として整理します。
