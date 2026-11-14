# 08 フォーム：送信を止めて、入力をチェックする

> フロントエンド編 ／ 前の章：[07_js_events](../07_js_events/) ／ 次の章：[09_js_dom](../09_js_dom/)

[07_js_events](../07_js_events/)で学んだ「イベントに反応して書き換える」方法を、**フォーム**に使います。フォームの**送信（`submit`）**を止めて、入力が正しいかをJavaScriptでチェックし、問題があればエラーを表示します。

| 節 | 学ぶこと | 練習問題 |
|---|---|---|
| 1 | `submit`：フォームの送信を止める（`preventDefault()`） | 練習問題1・2 |
| 2 | 入力をチェックする（`trim()`・`if`・`return`） | 練習問題3〜6 |
| 3 | 発展：条件の組み合わせ・三項演算子・`confirm()`・`reset`・`mouseover` | 練習問題7・8 |

1〜2節で、基本の入力チェックまで作れます。**3節は発展**で、短く書く方法や、少し難しい話をまとめています。

## 前提

| チャプター | 使う知識 |
|---|---|
| 02_html_semantic_form | フォーム部品（`form`・`input`・`textarea`・`button`） |
| 03_css_basics | `class`、クラスセレクタ（エラーの枠線を付け外しする） |
| 05_js_basics | 変数・関数・`if`・`===`・コールバック関数 |
| 06_js_dom_basics | `getElementById`・`textContent` |
| 07_js_events | `addEventListener`・`.value`・`classList.toggle`・`event`（イベントオブジェクト） |

## 目次

1. [フォームの送信を止める](#1-フォームの送信を止める)
2. [入力をチェックする](#2-入力をチェックする)
3. [発展：条件の組み合わせ・confirm・mouseover](#3-発展条件の組み合わせconfirmmouseover)

---

## フォルダ構成

```
01_frontend/08_js_forms/
├── README.md
├── example/                      サンプル（1つのサンプル＝1つのフォルダ）
│   ├── 01_submit/                フォームの送信を止める（submit・preventDefault）
│   │   ├── index.html
│   │   └── script.js
│   ├── 02_validation/            入力をチェックする（trim・if・return）
│   │   ├── index.html
│   │   └── script.js
│   └── 03_advanced/              発展（&&・||・三項演算子・confirm・reset・mouseover）
│       ├── index.html
│       └── script.js
└── question/                     練習問題（8問。問題文はREADMEの各節の最後）
    ├── 01_submit_stop/           練習問題1：送信を止める
    ├── 02_submit_result/         練習問題2：送信を止めて、結果を表示する
    ├── 03_trim/                  練習問題3：trim()で空白を取り除く
    ├── 04_title_check/           練習問題4：タイトルの入力をチェックする
    ├── 05_show_error/            練習問題5：エラー表示を関数にまとめる
    ├── 06_form_validation/       練習問題6：タイトルと本文をチェックする
    ├── 07_conditions/            練習問題7（発展）：条件を組み合わせる・三項演算子
    ├── 08_confirm_reset/         練習問題8（発展）：クリアの前に確認する
    └── answer/                   解答（問題と同じ名前のフォルダ）
        ├── 01_submit_stop/
        ├── 02_submit_result/
        ├── 03_trim/
        ├── 04_title_check/
        ├── 05_show_error/
        ├── 06_form_validation/
        ├── 07_conditions/
        └── 08_confirm_reset/
```

各練習問題のフォルダには、`index.html`と`script.js`があります。

---

## 1. フォームの送信を止める

> [example/01_submit/index.html](example/01_submit/index.html) / [example/01_submit/script.js](example/01_submit/script.js)

入力チェックの前に、フォームの`submit`イベントと、`preventDefault()`だけを学びます。

### 何もしないと、ページが再読み込みされる

フォームは、送信ボタンを押す（または入力欄でEnterキーを押す）と、入力内容をサーバーに送ろうとして、ページを移動（再読み込み）します。JavaScriptで入力チェックや結果表示をしても、ページが再読み込みされると、画面がリセットされてしまいます。

### 既定の動作を止める：`preventDefault()`

ブラウザには、イベントごとに決まった「既定の動作」があります。

| 操作 | 既定の動作 |
|---|---|
| フォームの`submit` | 入力内容をサーバーに送信して、ページを移動する |
| リンクの`click` | `href`のページに移動する |
| フォームの`reset` | 入力内容を初期状態に戻す |

`event.preventDefault()`を呼ぶと、この既定の動作を止められます。

```javascript
form.addEventListener('submit', (event) => {
    event.preventDefault();   // ページの再読み込み（送信）を止める

    result.textContent = `受け取りました：${titleInput.value}`;
});
```

ボタンの`click`ではなくフォームの`submit`を監視すると、Enterキーでの送信も同じように扱えます。

`preventDefault()`を呼んでも、そのあとのコードは実行されます。処理を途中で終わらせたいときは、別に`return`を書きます（次の2節）。

### 動作確認

`example/01_submit/index.html`をブラウザで開いて確認します。

| 確認する操作 | 確認したいこと |
|---|---|
| 「1. JavaScriptなし」に文字を入力して「送信」を押す | ページが再読み込みされ、入力が消える。URLの末尾に`?title=入力した文字`が付く |
| 「2. preventDefault()」に文字を入力して「送信」を押す | ページは再読み込みされず、入力も残る。下に「受け取りました」と表示される |
| 「2.」の入力欄でEnterキーを押す | ボタンを押したときと同じ動きになる（`submit`を監視しているため） |
| `script.js`の`event.preventDefault();`をコメントアウトして、「2.」で送信する | 「1.」と同じく、ページが再読み込みされ、表示がすぐに消える（確認したら戻す） |

### 練習問題1：送信を止める

> 問題：[question/01_submit_stop/index.html](question/01_submit_stop/index.html)・[question/01_submit_stop/script.js](question/01_submit_stop/script.js) ｜ 解答：[question/answer/01_submit_stop/index.html](question/answer/01_submit_stop/index.html)・[question/answer/01_submit_stop/script.js](question/answer/01_submit_stop/script.js)

<details>
<summary>問題の内容を開く</summary>

この章の練習問題は、「フォームの送信前に入力をチェックする」仕組みを、**小さな問題**に分けて、少しずつ作ります。HTMLの`required`などは、「JavaScriptだけで」チェックする練習のため、あえて付けていません。

`01_submit_stop/script.js`の`TODO 1`に書きます。`01_submit_stop/index.html`をブラウザで開き、ページ下の「テストを実行」ボタンを押すと、イベントが自動で起こされ、Consoleに ✅（正しい）／❌（間違い）が表示されます。自分でも画面を操作して、動きを確かめます。**1問ずつ**書いて確かめ、その問題が ✅ になってから、次に進みます（まだ書いていない問題が ❌ になるのは正常です）。

| # | やること |
|---|---|
| 1 | フォームの`submit`イベントで、送信（ページの再読み込み）を止める |

| # | ヒント |
|---|---|
| 1 | `form.addEventListener('submit', (event) => { ... })`の中で、`event.preventDefault()`を呼ぶ |

</details>

### 練習問題2：送信を止めて、結果を表示する

> 問題：[question/02_submit_result/index.html](question/02_submit_result/index.html)・[question/02_submit_result/script.js](question/02_submit_result/script.js) ｜ 解答：[question/answer/02_submit_result/index.html](question/answer/02_submit_result/index.html)・[question/answer/02_submit_result/script.js](question/answer/02_submit_result/script.js)

<details>
<summary>問題の内容を開く</summary>

`02_submit_result/script.js`の`TODO 1`に書きます（`preventDefault()`は書いてあります）。`02_submit_result/index.html`をブラウザで開き、ページ下の「テストを実行」ボタンを押すと、イベントが自動で起こされ、Consoleに ✅（正しい）／❌（間違い）が表示されます。自分でも画面を操作して、動きを確かめます。**1問ずつ**書いて確かめ、その問題が ✅ になってから、次に進みます（まだ書いていない問題が ❌ になるのは正常です）。

| # | やること |
|---|---|
| 1 | `result`に「送信されました：（タイトル）」と表示する |

| # | ヒント |
|---|---|
| 1 | 入力欄の値は`titleInput.value`。表示は`result.textContent = ...`（テンプレートリテラルを使う） |

</details>

---

## 2. 入力をチェックする

> [example/02_validation/index.html](example/02_validation/index.html) / [example/02_validation/script.js](example/02_validation/script.js)

1節で身につけた`submit`と`preventDefault()`に、「入力が正しいかを`if`で調べる」処理を加えます。

### 文字列の前後の空白を除く：`trim()`

```javascript
'  メモ '.trim();   // 'メモ'（前後の空白・改行を取り除く）
'   '.trim();       // ''（空白だけの入力は、空文字になる）
```

HTMLの`required`は空欄を防げますが、空白だけの入力（`'   '`）は通ってしまいます。`trim()`してから空かどうかを調べれば、空白だけの入力も防げます。

#### 🐍 Pythonとの違い

| | Python | JavaScript |
|---|---|---|
| 前後の空白を除く | `s.strip()` | `s.trim()` |

### 問題があれば、エラーを表示して`return`で終わる

```javascript
form.addEventListener('submit', (event) => {
    event.preventDefault();

    const name = nameInput.value.trim();

    if (name === '') {
        nameError.textContent = 'ニックネームを入力してください';
        result.textContent = '';
        return;                       // ここで関数を終わる
    }

    if (name.length > 10) {
        nameError.textContent = 'ニックネームは10文字以内で入力してください';
        result.textContent = '';
        return;
    }

    // ここまで来たら、問題なし
    nameError.textContent = '';
    result.textContent = `登録しました：${name}`;
});
```

| 書き方 | 説明 |
|---|---|
| `name === ''` | 空文字かどうか（`trim()`の後なので、空白だけの入力も`true`になる） |
| `name.length > 10` | 文字数が10を超えているか |
| `return;` | その場で関数を終わる。`return`より下の「問題が無いときの処理」は実行されない |

チェックを「問題があるものから順に調べ、あれば`return`で抜ける」形にすると、最後に残るのは「問題が無い場合の処理」だけになり、読みやすくなります（早期リターン）。

> HTMLの`required`でも空欄は防げますが、空白だけの入力（`'   '`）は通ってしまいます。JavaScriptなら`trim()`を使った細かいチェックができます。ただし、ブラウザ側のチェックは開発者ツールなどで無効にできるので、`02_backend/09_forms`で**サーバー（Python）側でも必ずチェック**します。

### 動作確認

`example/02_validation/index.html`をブラウザで開いて確認します。

| 確認する操作 | 確認したいこと |
|---|---|
| 何も入力せずに「登録する」を押す | 「ニックネームを入力してください」と表示される |
| スペースだけを入力して「登録する」を押す | 同じエラーが表示される（`trim()`で空文字になるため） |
| 11文字以上入力して「登録する」を押す | 「10文字以内で入力してください」と表示される |
| 1〜10文字入力して「登録する」を押す | エラーが消え、「登録しました：（名前）」と表示される |
| Consoleを見る | `メモ`・`true`と出力されている（`trim()`の例） |

### 練習問題3：trim()で空白を取り除く

> 問題：[question/03_trim/index.html](question/03_trim/index.html)・[question/03_trim/script.js](question/03_trim/script.js) ｜ 解答：[question/answer/03_trim/index.html](question/answer/03_trim/index.html)・[question/answer/03_trim/script.js](question/answer/03_trim/script.js)

<details>
<summary>問題の内容を開く</summary>

`03_trim/script.js`の`TODO 1`〜`TODO 3`に、関数を書きます。`03_trim/index.html`をブラウザで開くと、ファイルの一番下のテストが実行され、Consoleに ✅（正しい）／❌（間違い）が表示されます。**1問ずつ**書いてリロードし、その問題が ✅ になってから、次に進みます（まだ書いていない問題が ❌ になるのは正常です）。

| # | 関数 | やること | 例 |
|---|---|---|---|
| 1 | `trimText(text)` | 前後の空白を取り除いた文字を返す | `trimText('  メモ ')` → `'メモ'` |
| 2 | `isBlank(text)` | 空、または空白だけなら`true`、そうでなければ`false`を返す | `isBlank('   ')` → `true` |
| 3 | `hasEnough(text, min)` | 前後の空白を取り除いたあとの文字数が、`min`以上なら`true`を返す | `hasEnough('  あい  ', 5)` → `false` |

| # | ヒント |
|---|---|
| 1 | `text.trim()` |
| 2 | `trim()`してから、`=== ''`で比べる |
| 3 | `trim()`してから、`.length`で文字数を調べ、`>=`で比べる |

</details>

### 練習問題4：タイトルの入力をチェックする

> 問題：[question/04_title_check/index.html](question/04_title_check/index.html)・[question/04_title_check/script.js](question/04_title_check/script.js) ｜ 解答：[question/answer/04_title_check/index.html](question/answer/04_title_check/index.html)・[question/answer/04_title_check/script.js](question/answer/04_title_check/script.js)

<details>
<summary>問題の内容を開く</summary>

`04_title_check/script.js`の`TODO 1`に、`submit`の処理を書きます（`preventDefault()`は書いてあります）。`04_title_check/index.html`をブラウザで開き、ページ下の「テストを実行」ボタンを押すと、イベントが自動で起こされ、Consoleに ✅（正しい）／❌（間違い）が表示されます。自分でも画面を操作して、動きを確かめます。**1問ずつ**書いて確かめ、その問題が ✅ になってから、次に進みます（まだ書いていない問題が ❌ になるのは正常です）。

| # | 仕様 |
|---|---|
| 1 | タイトル（前後の空白を除いたもの）が空なら、`titleError`に「タイトルを入力してください」と表示し、`result`を空にして、処理を終わる |
| 2 | 問題が無ければ、`titleError`を空にして、`result`に「保存しました：（タイトル）」と表示する |

| # | ヒント |
|---|---|
| 1 | `titleInput.value.trim()`を変数に入れ、`=== ''`で調べる。エラーのときは`return`で関数を終わる |
| 2 | `return`より下に書くので、`if`の`else`は要らない |

</details>

### 練習問題5：エラー表示を関数にまとめる

> 問題：[question/05_show_error/index.html](question/05_show_error/index.html)・[question/05_show_error/script.js](question/05_show_error/script.js) ｜ 解答：[question/answer/05_show_error/index.html](question/answer/05_show_error/index.html)・[question/answer/05_show_error/script.js](question/answer/05_show_error/script.js)

<details>
<summary>問題の内容を開く</summary>

同じようなエラー表示を何度も書くことになるので、`showError()`という関数にまとめます。`05_show_error/script.js`の`TODO 1`に書きます。`05_show_error/index.html`をブラウザで開き、ページ下の「テストを実行」ボタンを押すと、イベントが自動で起こされ、Consoleに ✅（正しい）／❌（間違い）が表示されます。自分でも画面を操作して、動きを確かめます。**1問ずつ**書いて確かめ、その問題が ✅ になってから、次に進みます（まだ書いていない問題が ❌ になるのは正常です）。

| # | やること |
|---|---|
| 1 | `showError(input, errorEl, message)`：`errorEl`の文字を`message`にする。`message`が空文字でなければ、`input`に`invalid`クラスを付ける（空文字なら外す。CSSで赤枠になる） |

| # | ヒント |
|---|---|
| 1 | `errorEl.textContent = message;` / `input.classList.toggle('invalid', message !== '')` |

</details>

### 練習問題6：タイトルと本文をチェックする

> 問題：[question/06_form_validation/index.html](question/06_form_validation/index.html)・[question/06_form_validation/script.js](question/06_form_validation/script.js) ｜ 解答：[question/answer/06_form_validation/index.html](question/answer/06_form_validation/index.html)・[question/answer/06_form_validation/script.js](question/answer/06_form_validation/script.js)

<details>
<summary>問題の内容を開く</summary>

`showError()`は書いてあります。`06_form_validation/script.js`の`TODO 1`に、タイトルと本文の両方をチェックする`submit`の処理を書きます。`06_form_validation/index.html`をブラウザで開き、ページ下の「テストを実行」ボタンを押すと、イベントが自動で起こされ、Consoleに ✅（正しい）／❌（間違い）が表示されます。自分でも画面を操作して、動きを確かめます。**1問ずつ**書いて確かめ、その問題が ✅ になってから、次に進みます（まだ書いていない問題が ❌ になるのは正常です）。

| # | 仕様 |
|---|---|
| 1 | 送信（ページの再読み込み）は、チェック結果にかかわらず止める（このページには送信先が無いため） |
| 2 | タイトルが空白だけ・空なら「タイトルを入力してください」、本文が前後の空白を除いて10文字未満なら「本文は10文字以上で入力してください」を、各欄の下に表示する。エラーのある欄には`invalid`クラスが付く。問題が無い欄は、エラーを消す |
| 3 | どちらかにエラーがあれば、`result`を空にして処理を終わる。無ければ`result`に「保存しました：（タイトル）」と表示する |

| # | ヒント |
|---|---|
| 2 | `let hasError = false;`で「エラーがあったか」を覚えておき、2つの欄を`if / else`でそれぞれ調べる。片方がエラーでも、もう片方の表示は更新する |
| 3 | 最後に`hasError`が`true`なら`return`する |

</details>

---

## 3. 発展：条件の組み合わせ・confirm・mouseover

> [example/03_advanced/index.html](example/03_advanced/index.html) / [example/03_advanced/script.js](example/03_advanced/script.js)

この節は**発展**です。2節までで基本の入力チェックは作れます。ここでは、同じ処理をもっと短く書く方法や、削除の確認などで使う`confirm()`、`mouseover`と`mouseenter`の違いをまとめます。以降の章でも出てくるので、必要になったときに読み返してください。

なお、1つのイベントを親要素でまとめて受け取る書き方（イベント委譲）は、要素の作成と一緒に使うことが多いので、[09_js_dom](../09_js_dom/)で学びます。

### 条件を組み合わせる：`&&`・`||`・`!`

| 書き方 | 意味 | 例 |
|---|---|---|
| `A && B`（かつ） | 両方が真のときだけ真 | `hasInput && !confirm('…')` |
| `A \|\| B`（または） | どちらかが真なら真 | `title === '' \|\| body === ''` |
| `!A`（でない） | 真と偽を入れ替える | `!isAdmin` |

`&&`と`||`は、左から順に評価して、結果が決まった時点で右側を評価しません。

### 値を条件で選ぶ：三項演算子 `条件 ? A : B`

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

const titleMessage = title === '' ? 'タイトルを入力してください' : '';   // 空ならエラー文、そうでなければ空文字
```

2節の練習問題6も、`if`/`else`の代わりに三項演算子を使うと、次のように短く書き換えられます。

```javascript
const titleMessage = title === '' ? 'タイトルを入力してください' : '';
const bodyMessage = body.length < 10 ? '本文は10文字以上で入力してください' : '';

showError(titleInput, titleError, titleMessage);
showError(bodyInput, bodyError, bodyMessage);

if (titleMessage !== '' || bodyMessage !== '') {   // どちらかにエラー文があれば終わる
    result.textContent = '';
    return;
}
```

#### 🐍 Pythonとの違い

```python
# Python
if has_input and not confirm('…'):                          # and / not
    ...
label = '完了' if is_done else '未完了'                        # 三項演算子は「値 if 条件 else 値」
```

| | Python | JavaScript |
|---|---|---|
| かつ／または／でない | `and` / `or` / `not` | `&&` / `\|\|` / `!`（**単語ではなく記号**） |
| 値を条件で選ぶ | `A if 条件 else B`（**値が先**） | `条件 ? A : B`（**条件が先**） |

### `confirm()`で確認する

```javascript
link.addEventListener('click', (event) => {
    if (!confirm('外部サイトに移動します。よろしいですか？')) {
        event.preventDefault();   // 「キャンセル」なら移動を止める
    }
});
```

`confirm('メッセージ')`は確認ダイアログを表示し、「OK」なら`true`、「キャンセル」なら`false`を返します。

Flaskのテンプレートでは、これをHTMLの属性（`onclick`）で短く書くこともあります。

```html
<button type="submit" onclick="return confirm('削除しますか？')">削除</button>
```

`onclick`属性の中で`false`を`return`すると、`preventDefault()`と同じく既定の動作（ここではフォームの送信）が止まります。つまり「キャンセル」を押すと`confirm()`が`false`を返し、削除のリクエストが送られません。

### `reset`の前に確認する

```javascript
form.addEventListener('reset', (event) => {
    const hasInput = titleInput.value !== '' || bodyInput.value !== '';

    if (hasInput && !confirm('入力内容を消しますか？')) {
        event.preventDefault();   // キャンセル → 入力を消さない
    }
});
```

`reset`は「入力内容を初期状態に戻す」という既定の動作を持つイベントなので、`preventDefault()`で止められます。

### `mouseenter`と`mouseover`の違い

| イベント | 違い |
|---|---|
| `mouseenter` / `mouseleave` | その要素に入ったとき・出たときに**1回だけ**発生する。普段はこちらを使う |
| `mouseover` / `mouseout` | 中の子要素に移るたびにも発生する（イベントは、子要素から親要素へ伝わるため） |
| `focus` / `blur` | その要素自身が選ばれた・外れたときだけ発生する |
| `focusin` / `focusout` | 中の子要素が選ばれた・外れたときにも発生する（11_js_ui 4節で使う） |

### 動作確認

`example/03_advanced/index.html`をブラウザで開いて確認します。

| 確認する操作 | 確認したいこと |
|---|---|
| Consoleを見る | `false`・`true`・`true`（`&&`・`\|\|`・`!`）、`完了`・`完了`（三項演算子と`if`/`else`）、`タイトルを入力してください`と出力されている |
| 「MDNへ移動する」をクリックして「キャンセル」を選ぶ | ページが移動しない |
| 「削除」ボタンを押して「キャンセル」を選ぶ | フォームが送信されない（URLの末尾に`#`が付かない） |
| 入力欄に文字を入力して「クリア」を押し、「キャンセル」を選ぶ | 入力が消えない（OKを選ぶと消える） |
| 何も入力せずに「クリア」を押す | 確認が出ず、そのまま動く |
| 点線の箱の中で、子要素の上を行き来する | `mouseover`の回数だけがどんどん増え、`mouseenter`は箱に入ったときだけ増える |

### 練習問題7：条件を組み合わせる・三項演算子（発展）

> 問題：[question/07_conditions/index.html](question/07_conditions/index.html)・[question/07_conditions/script.js](question/07_conditions/script.js) ｜ 解答：[question/answer/07_conditions/index.html](question/answer/07_conditions/index.html)・[question/answer/07_conditions/script.js](question/answer/07_conditions/script.js)

<details>
<summary>問題の内容を開く</summary>

`07_conditions/script.js`の`TODO 1`〜`TODO 5`に、関数を書きます。`07_conditions/index.html`をブラウザで開くと、ファイルの一番下のテストが実行され、Consoleに ✅（正しい）／❌（間違い）が表示されます。**1問ずつ**書いてリロードし、その問題が ✅ になってから、次に進みます（まだ書いていない問題が ❌ になるのは正常です）。

| # | 関数 | やること | 使う書き方 |
|---|---|---|---|
| 1 | `canEdit(isLoggedIn, isAdmin)` | ログイン中**かつ**管理者のときだけ`true` | `&&` |
| 2 | `hasInput(title, body)` | タイトル**または**本文のどちらかが、空文字でなければ`true` | `\|\|` |
| 3 | `isGuest(isLoggedIn)` | ログインしていないとき`true` | `!` |
| 4 | `statusLabel(isDone)` | `true`なら`'完了'`、`false`なら`'未完了'` | 三項演算子 |
| 5 | `titleMessage(title)` | `title`が空文字なら`'タイトルを入力してください'`、そうでなければ`''` | 三項演算子 |

| # | ヒント |
|---|---|
| 2 | `title !== '' \|\| body !== ''` |
| 4・5 | `条件 ? 真のとき : 偽のとき`（条件が先） |

</details>

### 練習問題8：クリアの前に確認する（発展）

> 問題：[question/08_confirm_reset/index.html](question/08_confirm_reset/index.html)・[question/08_confirm_reset/script.js](question/08_confirm_reset/script.js) ｜ 解答：[question/answer/08_confirm_reset/index.html](question/answer/08_confirm_reset/index.html)・[question/answer/08_confirm_reset/script.js](question/answer/08_confirm_reset/script.js)

<details>
<summary>問題の内容を開く</summary>

練習問題6までの完成コードに、**クリアボタンを押したときの確認**を加えます。`08_confirm_reset/script.js`の`TODO 1`・`TODO 2`を書きます。`08_confirm_reset/index.html`をブラウザで開き、ページ下の「テストを実行」ボタンを押すと、イベントが自動で起こされ、Consoleに ✅（正しい）／❌（間違い）が表示されます。自分でも画面を操作して、動きを確かめます。**1問ずつ**書いて確かめ、その問題が ✅ になってから、次に進みます（まだ書いていない問題が ❌ になるのは正常です）。

| # | 仕様 |
|---|---|
| 1 | 「クリア」ボタン（`type="reset"`）を押したとき（フォームの`reset`イベント）、何か入力されていれば`confirm('入力内容を消しますか？')`で確認し、キャンセルなら消さない。入力が何も無いときは、確認を出さない |
| 2 | 入力を消す場合は、エラー表示（`showError`で空文字を渡す）と`#result`も消す |

| # | ヒント |
|---|---|
| 1 | 入力があるかは`titleInput.value !== '' || bodyInput.value !== ''`。`reset`イベントでも`event.preventDefault()`で入力を消す動作を止められる |
| 2 | `showError(titleInput, titleError, '')`のように、空文字を渡すとエラーが消える |

</details>

---

## 次のステップ

続きは [09_js_dom](../09_js_dom/) です。ここまで使ってきた「要素の取得と書き換え」を、`querySelector`・属性・要素の作成・イベント委譲など、DOM操作として整理します。
