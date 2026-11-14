# JavaScript 文法・メソッド リファレンス

フロントエンド編（[05_js_basics](../../01_frontend/05_js_basics/)〜[12_js_data](../../01_frontend/12_js_data/)）で出てくる、JavaScriptの**文法・メソッド・プロパティ・イベント**を、種類別にまとめた一覧です。章のように順番に読む必要はなく、書き方を忘れたときに辞書的に引く使い方を想定しています。

## 使い方

- 表の「初出」は、その書き方を**最初に学ぶ章と節**です。例：`06-2`は、[06_js_dom_basics](../../01_frontend/06_js_dom_basics/)の2節。詳しい説明・例・練習問題は、その章を見ます。
- 各章は、**学んだ文法だけで問題が解ける順番**になっています。表の初出より前の章では、その書き方を使いません。
- Pythonとの違いは、末尾の[Pythonとの対応表](#9-pythonとの対応表)にまとめています。

## 章と学ぶ内容

| 章 | 内容 | 主な文法・API |
|---|---|---|
| [05_js_basics](../../01_frontend/05_js_basics/) | 基本文法 | 変数・型・関数・`if`・`for`・配列・コールバック・`null`と真偽の判定 |
| [06_js_dom_basics](../../01_frontend/06_js_dom_basics/) | DOMの最小限 | 要素の取得（`getElementById`・`querySelector`など）・`textContent` |
| [07_js_events](../../01_frontend/07_js_events/) | イベント | `addEventListener`・`click`・`input`・イベントオブジェクト・ホバー・フォーカス |
| [08_js_forms](../../01_frontend/08_js_forms/) | フォーム | `submit`・`preventDefault()`・`trim()`・入力チェック・`confirm()` |
| [09_js_dom](../../01_frontend/09_js_dom/) | DOMの応用 | 属性・要素の作成と削除・イベント委譲・`innerHTML`とXSS・道具箱 |
| [10_js_render](../../01_frontend/10_js_render/) | 配列メソッドと一覧の画面 | `map`・`filter`・`find`・`includes`・`render()` |
| [11_js_ui](../../01_frontend/11_js_ui/) | UI | タブ・`popover`・`<dialog>`・スライドショー・スクロール |
| [12_js_data](../../01_frontend/12_js_data/) | データ | JSON・`fetch()`・`async`/`await`・`try`/`catch`・`localStorage` |

## 目次

1. [基本文法](#1-基本文法)
2. [文字列・配列・数値のメソッド](#2-文字列配列数値のメソッド)
3. [要素の取得](#3-要素の取得)
4. [要素の書き換え](#4-要素の書き換え)
5. [イベント](#5-イベント)
6. [フォームと入力チェック](#6-フォームと入力チェック)
7. [時間・スクロール・UIのAPI](#7-時間スクロールuiのapi)
8. [データの扱い（JSON・通信・保存）](#8-データの扱いjson通信保存)
9. [Pythonとの対応表](#9-pythonとの対応表)
10. [デバッグ](#10-デバッグ)

---

## 1. 基本文法

### 変数・データ型

| 書き方 | 説明 | 初出 |
|---|---|---|
| `let x = 1;` | 再代入できる変数 | 05-1 |
| `const x = 1;` | 再代入できない変数（何が変わるか分からないときは、まず`const`） | 05-1 |
| `'文字'` / `"文字"` | 文字列 | 05-1 |
| `42` / `4.2` | 数値（整数と小数を区別しない） | 05-1 |
| `true` / `false` | 真偽値（すべて小文字） | 05-1 |
| `[1, 2, 3]` | 配列（Pythonのlist） | 05-1 |
| `{ title: 'メモ', pinned: false }` | オブジェクト（Pythonのdict） | 05-1 |
| `obj.title` / `obj['title']` | オブジェクトの値の取り出し | 05-1 |
| `obj.title = 'x';` | 値の書き換え（`const`でも中身の書き換えはできる） | 05-1 |
| `` `${name}さん` `` | テンプレートリテラル。`${ }`に変数や計算を埋め込む（Pythonのf文字列） | 05-1 |
| `null` | 「無い」ことを意図的に表す値 | 05-5 |
| `undefined` | まだ値が入っていない・存在しないプロパティを読んだ | 05-5 |

### 演算子・比較

| 書き方 | 説明 | 初出 |
|---|---|---|
| `a + b` `a - b` `a * b` `a / b` | 四則演算。`/`は小数になる。整数にするには`Math.floor()` | 05-1 |
| `a += b` `a -= b` | `a = a + b`の省略 | 05-3 |
| `a++` `a--` | 1増やす / 1減らす | 05-3 |
| `a === b` `a !== b` | 値と型が等しい / 等しくない。**比較は常にこちら** | 05-3 |
| `a > b` `a >= b` `a < b` `a <= b` | 大小の比較 | 05-3 |
| `a == b` | 型を変換して比べる。**使わない** | 05-5 |
| `A && B` | かつ | 08-3 |
| `A \|\| B` | または | 08-3 |
| `!A` | でない | 08-3 |
| `A ?? B` | `A`が`null`または`undefined`のときだけ`B`を使う | 12-4 |
| `条件 ? A : B` | 三項演算子。条件が真なら`A`、偽なら`B`（条件が先） | 08-3 |
| `a % b` | 割った余り | 11-4 |

### 関数

| 書き方 | 説明 | 初出 |
|---|---|---|
| `function add(a, b) { return a + b; }` | 関数宣言 | 05-2 |
| `const add = (a, b) => { return a + b; };` | アロー関数。**主にこの書き方を使う** | 05-2 |
| `const add = (a, b) => a + b;` | `{ }`と`return`を省略した1行の形 | 05-2 |
| `return 値;` | 値を返して、関数を終わる。`return;`だけでも終われる | 05-2 |
| `const f = greet;` / `typeof greet` | 関数は値。`()`を付けないと関数そのもの | 05-4 |
| `repeat(3, (i) => { ... })` | 関数を引数として渡す（コールバック関数） | 05-4 |

### 条件分岐・繰り返し

| 書き方 | 説明 | 初出 |
|---|---|---|
| `if (条件) { ... } else if (条件) { ... } else { ... }` | 条件分岐。条件は`( )`で囲み、ブロックは`{ }` | 05-3 |
| `for (let i = 0; i < n; i++) { ... }` | 回数を決めた繰り返し（Pythonの`range(n)`） | 05-3 |
| `配列.forEach((x) => { ... });` | 配列を1件ずつ処理する | 05-3 |
| `配列.forEach((x, index) => { ... });` | 2つ目の引数で、何番目か（0始まり） | 11-4 |

### 真偽の判定（truthy / falsy）

| 値 | 判定 |
|---|---|
| `false`・`0`・`''`・`null`・`undefined`・`NaN` | **偽（falsy）** |
| 上記以外（`'0'`・`[]`・`{}`を含む） | **真（truthy）** |

| 書き方 | 説明 | 初出 |
|---|---|---|
| `if (値) { ... }` | 値が truthy のときだけ実行する。`if (要素)`で「要素があるときだけ」 | 05-5 |
| `Boolean(値)` | `true` / `false`に変換して確かめる | 05-5 |
| `list.length === 0` | 空の配列の判定（空の配列`[]`は**真**なので、`if (list)`では判定できない） | 05-5 |

### 例外処理

| 書き方 | 説明 | 初出 |
|---|---|---|
| `try { ... } catch (error) { ... }` | `try`の中でエラーが起きたら、`catch`に移る | 12-3 |
| `finally { ... }` | 成功しても失敗しても、最後に行う処理 | 12-3 |
| `throw new Error('メッセージ')` | 自分でエラーを発生させる | 12-3 |

---

## 2. 文字列・配列・数値のメソッド

### 文字列

| 書き方 | 説明 | 初出 |
|---|---|---|
| `文字列.length` | 文字数（`()`を付けない） | 05-3 |
| `文字列.trim()` | 前後の空白・改行を取り除く（Pythonの`strip()`） | 08-2 |
| `文字列.slice(開始, 終了)` | 開始〜終了の手前までを取り出す | 10-1 |
| `文字列.startsWith('文字')` | その文字で始まるか | 10-1 |
| `文字列.split(区切り)` | 区切り文字で分けた配列にする（`'HTML CSS'.split(' ')`） | 10-3 |
| `a.localeCompare(b)` | 文字列の比較（並べ替えに使う） | 12-5 |
| `Number('3')` | 文字列を数値に変換する（Pythonの`int()`/`float()`） | 06-3 |

### 配列

| 書き方 | 説明 | 初出 |
|---|---|---|
| `配列.length` | 要素の数（`()`を付けない） | 05-1 |
| `配列[0]` / `配列[配列.length - 1]` | 最初 / 最後の要素（番号は0から） | 06-2 |
| `配列.push(値)` | 最後に追加する（元の配列が変わる） | 05-3 |
| `配列.unshift(値)` | 先頭に追加する（元の配列が変わる） | 10-1 |
| `配列.forEach(fn)` | 1件ずつ処理する（戻り値なし） | 05-3 |
| `配列.map(fn)` | 1件ずつ変換した**新しい配列** | 10-1 |
| `配列.filter(fn)` | 条件に合うものだけの**新しい配列** | 10-1 |
| `配列.find(fn)` | 条件に合う**最初の1件**（無ければ`undefined`） | 10-1 |
| `配列.includes(値)` | その値を含むか（`true` / `false`） | 10-1 |
| `配列.indexOf(値)` | 値が何番目か（0始まり。**無ければ`-1`**） | 10-1 |
| `配列.sort((a, b) => 比較)` | 並べ替える（元の配列が変わる） | 12-5 |
| `Array.from(NodeList)` | `querySelectorAll`の結果などを、配列に変換する | 10-1 |

### 数値・日時

| 書き方 | 説明 | 初出 |
|---|---|---|
| `Math.floor(数値)` | 小数点以下を切り捨てる | 10-1 |
| `Date.now()` | 現在時刻（ミリ秒の数値）。簡易的な一意のIDに使える | 12-5 |
| `new Date().toLocaleString()` | 今の日時を、使っている環境の形式の文字列にする | 12-4 |

---

## 3. 要素の取得

| 書き方 | 取得するもの | 戻り値 | 見つからないとき | 初出 |
|---|---|---|---|---|
| `document.getElementById('id')` | `id`が一致する要素**1つ**（`#`は付けない） | 要素 | `null` | 06-1 |
| `document.querySelector('セレクタ')` | セレクタに一致する**最初の**要素1つ | 要素 | `null` | 06-2 |
| `document.querySelectorAll('セレクタ')` | セレクタに一致する要素**すべて** | `NodeList`（`forEach`が使える） | 空（`length`が`0`） | 06-2 |
| `document.getElementsByClassName('クラス名')` | クラスが一致する要素**すべて**（`.`は付けない） | `HTMLCollection`（`forEach`は無い） | 空 | 06-2 |
| `document.getElementsByTagName('タグ名')` | タグ名が一致する要素**すべて** | `HTMLCollection` | 空 | 06-2 |
| `要素.closest('セレクタ')` | 自分または祖先から、最も近い一致する要素 | 要素 | `null` | 09-1 |
| `要素.matches('セレクタ')` | その要素が、セレクタに一致するか | `true` / `false` | — | 11-2 |
| `document.documentElement` | `<html>`要素 | 要素 | — | 12-4 |
| `document.activeElement` | 今フォーカスされている要素 | 要素 | — | 11-1 |

### `querySelector`のセレクタ

03_css_basicsで学んだCSSのセレクタが、そのまま使えます。

| セレクタ | 意味 | 例 |
|---|---|---|
| `#heading` | `id`が`heading`の要素 | `<h2 id="heading">` |
| `.note` | クラスが`note`の要素 | `<p class="note">` |
| `h1` | タグ名が`h1`の要素 | `<h1>` |
| `.item .name` | `.item`の**中にある**`.name` | `<li class="item"><span class="name">` |
| `ul > li` | `ul`の**直下の**`li` | `<ul><li>` |
| `a.doc-link` / `meta[name="csrf-token"]` | タグとクラス / 属性の値でも指定できる（CSSの書き方と同じ） | `<a class="doc-link">` |

### 取得した結果の使い方

| 書き方 | 説明 | 初出 |
|---|---|---|
| `結果.length` | 要素の数 | 06-2 |
| `結果[0]` / `結果[i]` | 最初 / `i`番目の要素（番号は0から） | 06-2 |
| `for (let i = 0; i < 結果.length; i++) { 結果[i] }` | 1つずつ処理する（`HTMLCollection`でも`NodeList`でも使える） | 06-2 |
| `NodeList.forEach((x) => { ... })` | 1つずつ処理する。**`querySelectorAll`の結果だけ**で使える | 06-2 |
| `Array.from(結果)` | 配列に変換する（`map`・`filter`・`indexOf`を使うため） | 10-1 |

---

## 4. 要素の書き換え

### 文字

| 書き方 | 説明 | 初出 |
|---|---|---|
| `要素.textContent` | 要素の中の文字を読む（**常に文字列**） | 06-1 |
| `要素.textContent = '文字';` | 書き換える。入れた文字は、ただの文字として扱われる（タグも文字になる）。子要素はすべて消える | 06-1 |
| `要素.textContent += '文字';` | 今の文字の後ろに追加する | 06-3 |
| `要素.textContent = '';` | 中身を消す | 06-3 |
| `要素.innerHTML = 'HTML';` | HTMLとして解釈して入れる。**ユーザーの入力には使わない**（XSS） | 09-1 |

### クラス・属性

| 書き方 | 説明 | 初出 |
|---|---|---|
| `要素.classList.toggle('クラス名')` | クラスが無ければ付け、あれば外す | 07-1 |
| `要素.classList.toggle('クラス名', 条件)` | 条件が`true`なら付け、`false`なら外す | 07-2 |
| `要素.classList.add('クラス名')` / `remove('クラス名')` | 付ける / 外す（条件に関係なく） | 09-1 |
| `要素.classList.contains('クラス名')` | そのクラスが付いているか（`true` / `false`） | 09-1 |
| `要素.className = 'クラス名'` | `class`属性をまとめて設定する | 09-1 |
| `要素.getAttribute('属性名')` | 属性の値を読む | 09-1 |
| `要素.setAttribute('属性名', '値')` | 属性を追加・変更する | 09-1 |
| `要素.dataset.名前` | `data-名前`属性の値（ハイフンはキャメルケースに。`data-theme-color` → `dataset.themeColor`）。**読んだ値は文字列** | 09-1 |

### プロパティ（状態）

| 書き方 | 説明 | 初出 |
|---|---|---|
| `入力欄.value` | 入力欄（`input`・`textarea`・`select`）に入力されている値を読み書きする | 07-2 |
| `要素.hidden = true / false` | 隠す / 表示する | 09-1 |
| `ボタン.disabled = true / false` | 押せなくする / 押せるようにする | 09-1 |
| `要素.focus()` | フォーカス（キーボード操作の対象）を移す | 09-1 |
| `要素.tabIndex` | Tabキーで止まるか（`0`＝止まる、`-1`＝飛ばす） | 11-1 |
| `要素.style.width = '50%'` | CSSを直接書き込む（ハイフンのあるプロパティはキャメルケース）。ふだんの見た目はクラスの付け外しで切り替える | 09-1 |

### 要素の作成・削除

| 書き方 | 説明 | 初出 |
|---|---|---|
| `document.createElement('li')` | 要素を作る（この時点では、まだ画面に無い） | 09-1 |
| `親.append(子1, 子2, '文字')` | 画面上の要素に追加する。追加して、初めて表示される | 09-1 |
| `要素.remove()` | 要素を消す | 09-1 |
| `要素.textContent = ''` | 子要素をすべて消す | 09-1 |

---

## 5. イベント

### イベントの登録

| 書き方 | 説明 | 初出 |
|---|---|---|
| `要素.addEventListener('イベント名', (event) => { ... });` | 「イベントが起きたら、この関数を呼んで」と登録する（コールバック関数） | 07-1 |
| `親.addEventListener('click', (event) => { ... });` | 親要素に1回だけ登録して、`event.target`でどの子要素かを判定する（イベント委譲）。作り直される要素に有効 | 09-1 |

### よく使うイベント

| イベント名 | 発生するタイミング | 主な対象 | 初出 |
|---|---|---|---|
| `click` | クリックされたとき | ボタン・リンク | 07-1 |
| `input` | 入力欄の値が変わるたび（1文字ごと） | `input`・`textarea` | 07-2 |
| `change` | 値が確定したとき（`select`の選択・チェックボックスの切り替えなど） | `select`・チェックボックス | 07-3 |
| `keydown` | キーが押されたとき | 入力欄・ページ全体 | 07-3 |
| `mouseenter` / `mouseleave` | マウスが要素に入った / 出た（1回だけ。普段はこちら） | どの要素でも | 07-3 |
| `mouseover` / `mouseout` | 子要素に移るたびにも発生する | どの要素でも | 08-3 |
| `focus` / `blur` | 要素が選ばれた / 外れた | ボタン・リンク・入力欄 | 07-3 |
| `focusin` / `focusout` | 中の子要素が選ばれた / 外れたときにも発生する | どの要素でも | 11-4 |
| `submit` | フォームが送信されようとしたとき（ボタンのクリック・Enterキー） | `form` | 08-1 |
| `reset` | フォームが初期状態に戻されようとしたとき | `form` | 08-3 |
| `toggle` | `popover`が開いた・閉じたとき（`event.newState`が`'open'`か`'closed'`） | `popover`を付けた要素 | 11-2 |
| `scroll` | スクロール中に何度も発生する（軽い処理だけにする） | `window` | 11-5 |

### イベントオブジェクト

| 書き方 | 説明 | 初出 |
|---|---|---|
| `event.type` | イベントの種類（`'click'`など） | 07-3 |
| `event.key` | 押されたキー（`'a'`・`'Enter'`など） | 07-3 |
| `event.target` | イベントが**実際に起きた要素**（子要素の場合もある） | 09-1 |
| `event.preventDefault()` | ブラウザの**既定の動作**（送信・リンク移動・入力の消去）を止める | 08-1 |

---

## 6. フォームと入力チェック

| 書き方 | 説明 | 初出 |
|---|---|---|
| `form.addEventListener('submit', (event) => { event.preventDefault(); ... });` | 送信（ページの再読み込み）を止めて、JavaScriptで処理する。Enterキーでの送信も拾える | 08-1 |
| `const title = input.value.trim();` | 前後の空白を除いた入力値。空白だけの入力も「空」として扱える | 08-2 |
| `if (title === '') { エラー表示; return; }` | 問題があれば、エラーを表示して**`return`で終わる**（早期リターン） | 08-2 |
| `let hasError = false;` | 複数の欄を調べるとき、エラーがあったかを覚えておく変数 | 08-2 |
| `errorEl.textContent = message;` / `input.classList.toggle('invalid', message !== '')` | エラー表示の切り替え（関数にまとめる） | 08-2 |
| `confirm('メッセージ')` | 確認ダイアログ。OKなら`true`、キャンセルなら`false` | 08-3 |
| `if (!confirm('...')) { event.preventDefault(); }` | キャンセルされたら、既定の動作を止める | 08-3 |
| `onclick="return confirm('削除しますか？')"` | HTML属性で書く短い形。`false`を`return`すると既定の動作が止まる | 08-3 |

> JavaScriptのチェックは、ブラウザ側だけのもので、無効にできます。サーバー側でも必ずチェックします（`02_backend/09_forms`）。

---

## 7. 時間・スクロール・UIのAPI

### 時間

| 書き方 | 説明 | 初出 |
|---|---|---|
| `setTimeout(関数, ミリ秒)` | 指定した時間のあとに**1回だけ**関数を呼ぶ。戻り値の番号を`clearTimeout(番号)`に渡すと取り消せる | 11-2 |
| `setInterval(関数, ミリ秒)` | 一定時間ごとに関数を呼び続ける。`clearInterval(番号)`で止める | 11-4 |

### ポップアップ・ダイアログ

| 書き方 | 説明 | 初出 |
|---|---|---|
| `<div popover>` / `<button popovertarget="id">` | JavaScriptなしで開閉するポップアップ（HTML） | 11-2 |
| `popover="manual"` | 外側のクリックやEscキーでは閉じない（開閉はJavaScript） | 11-2 |
| `要素.showPopover()` / `hidePopover()` | JavaScriptで開く / 閉じる。開いているものに`showPopover()`するとエラー | 11-2 |
| `要素.matches(':popover-open')` | 開いているかを調べる | 11-2 |
| `dialog.showModal()` | モーダルとして開く（後ろの画面は操作できない。Escキーで閉じる） | 11-3 |
| `dialog.close()` | 閉じる。フォーカスは開く前の要素に戻る | 11-3 |
| `dialog.open` | 今開いているか（`true` / `false`） | 11-3 |

### スクロール

| 書き方 | 説明 | 初出 |
|---|---|---|
| `window.scrollY` | ページの一番上から、何pxスクロールしたか | 11-5 |
| `document.documentElement.scrollHeight` / `window.innerHeight` | ページ全体の高さ / 画面に見えている部分の高さ | 11-5 |
| `window.scrollTo({ top, behavior: 'smooth' })` | 指定した位置までスクロールする | 11-5 |
| `要素.scrollIntoView({ behavior: 'smooth' })` | その要素が見える位置までスクロールする | 11-5 |
| `new IntersectionObserver((entries) => { ... })` | 要素が画面に入った・出たときだけ知らせる。`scroll`イベントより軽い | 11-5 |

### メディアクエリ

| 書き方 | 説明 | 初出 |
|---|---|---|
| `window.matchMedia('(prefers-color-scheme: dark)').matches` | CSSのメディアクエリが今の画面に当てはまるかを、`true` / `false`で調べる | 12-4 |

---

## 8. データの扱い（JSON・通信・保存）

### JSON

| 書き方 | 説明 | 初出 |
|---|---|---|
| `JSON.stringify(値)` | JavaScriptの値 → JSON文字列 | 12-1 |
| `JSON.parse(文字列)` | JSON文字列 → JavaScriptの値 | 12-1 |

JSONは、JavaScriptのオブジェクトよりルールが厳しく、**キーも文字列もダブルクォート**で囲み、**最後の要素の後ろにカンマを付けず**、コメントも書けません。使える値は、文字列・数値・`true`/`false`・`null`・配列・オブジェクトで、関数・`undefined`は使えません。

### fetch（通信）

| 書き方 | 説明 | 初出 |
|---|---|---|
| `const response = await fetch('url');` | データを取得する（GET）。サーバー経由（`http://`）で開いたページで使う | 12-2 |
| `await response.json()` | レスポンスのJSONを、JavaScriptの値にする | 12-2 |
| `async () => { ... }` / `await` | 関数の前に`async`を付けると、中で`await`（結果が届くまで待つ）が使える | 12-2 |
| `fetch(url, { method, headers, body })` | `method`：`'POST'`など。`headers`：JSONを送るときは`Content-Type: application/json`。`body`：`JSON.stringify()`した文字列 | 12-2 |
| `response.ok` / `response.status` | 成功（200番台）か / ステータスコード | 12-3 |

### localStorage（ブラウザへの保存）

| 書き方 | 説明 | 初出 |
|---|---|---|
| `localStorage.setItem('キー', '文字列')` | 保存する（**文字列だけ**） | 12-4 |
| `localStorage.getItem('キー')` | 読み出す（無ければ`null`） | 12-4 |
| `localStorage.removeItem('キー')` | 1件消す | 12-4 |
| `JSON.stringify(値)` で保存 / `JSON.parse(文字列)` で復元 | 配列やオブジェクトを保存する | 12-4 |
| `localStorage.getItem('draft') ?? ''` | 保存されていなければ、既定値を使う | 12-4 |

---

## 9. Pythonとの対応表

| Python | JavaScript |
|---|---|
| `x = 1`（宣言なし） | `let x = 1;` / `const x = 1;`（宣言が必要） |
| `None` | `null`（または`undefined`） |
| `True` / `False` | `true` / `false` |
| `==`（値の比較） | `===`（`==`は使わない） |
| `and` / `or` / `not` | `&&` / `\|\|` / `!` |
| `A if 条件 else B` | `条件 ? A : B`（条件が先） |
| `[1, 2, 3]`（list） | `[1, 2, 3]`（配列） |
| `{'a': 1}`（dict） | `{ a: 1 }`（オブジェクト） |
| `d['a']` | `d.a`（または`d['a']`） |
| `len(x)` | `x.length`（`()`を付けない） |
| `list.append(v)` | `list.push(v)` |
| `f'{name}さん'` | `` `${name}さん` `` |
| `def f(a, b): return a + b` | `const f = (a, b) => a + b;` |
| `lambda x: x * 2` | `(x) => x * 2` |
| インデントでブロック | `{ }`でブロック |
| `elif` | `else if` |
| `for i in range(3):` | `for (let i = 0; i < 3; i++) { ... }` |
| `for x in list:` | `list.forEach((x) => { ... });` |
| `print(x)` | `console.log(x)` |
| `s.strip()` | `s.trim()` |
| `int('3')` / `float('1.5')` | `Number('3')` / `Number('1.5')` |
| `'1000' + 500` → エラー | `'1000' + 500` → `'1000500'`（**連結される**） |
| `[x * 2 for x in list]` | `list.map((x) => x * 2)` |
| `[x for x in list if 条件]` | `list.filter((x) => 条件)` |
| 空のリスト`[]`は偽 | 空の配列`[]`は**真** |
| `memo['body']`（無いとKeyError） | `memo.body`（無いと`undefined`。エラーにならない） |
| `try: ... except Exception as e:` | `try { ... } catch (error) { ... }` |
| `json.dumps(x)` / `json.loads(s)` | `JSON.stringify(x)` / `JSON.parse(s)` |

---

## 10. デバッグ

| 画面・Consoleの様子 | 原因 |
|---|---|
| `Cannot read properties of null (reading '...')` / `Cannot set properties of null (setting '...')` | 要素を取得できず`null`になっている。`id`の綴り・`#`や`.`の付け忘れ・`<script>`を`<head>`で読み込んでいる、を疑う |
| `Cannot read properties of undefined` | 存在しない番号（`names[3]`など）を指定した |
| `xxx is not defined` | 定義されていない変数を使った（変数名の打ち間違い・宣言する前に使っている） |
| `Unexpected token` | 文法が間違っている（カッコ・引用符の閉じ忘れ） |
| `names.forEach is not a function` | `getElementsBy…`の結果（`HTMLCollection`）には`forEach`が無い。`for`文か`querySelectorAll`を使う |
| エラーは出ないのに画面が変わらない | `textcontent`のようにプロパティ名の**大文字小文字**が違う／取得した要素が別の要素になっている |
| 表示が`undefined`になる | `lenght`のようにプロパティ名を打ち間違えている |
| 合計が`NaN`・連結された文字になる | `textContent`・`value`・`dataset`で読んだ値は文字列。`Number()`で数値にしていない |
| `fetch`が失敗する（Consoleに`Fetch API cannot load file:///...`など） | HTMLを`file://`で直接開いている。簡易サーバー（`python -m http.server`）で開く（[12_js_dataの0節](../../01_frontend/12_js_data/)） |

調べる順番：①Consoleの赤字のエラーと、右端のファイル名・行番号を見る → ②エラーが出ないときは`console.log(変数)`かSourcesパネルのブレークポイントで、途中の値を確かめる（[05_js_basicsの0節](../../01_frontend/05_js_basics/#0-javascriptの読み込み方とデバッグ)）。
