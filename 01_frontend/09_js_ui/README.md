# 07 JavaScriptでよく使うUIを作る

> フロントエンド編 ／ 前の章：[08_js_render](../08_js_render/) ／ 次の章：[10_js_data](../10_js_data/)

[06_js_events](../06_js_events/)・[07_js_dom](../07_js_dom/)で学んだイベントとDOM操作を組み合わせて、Webサイトでよく見かけるUI（タブ切り替え・ポップアップ・モーダルウィンドウ・スライドショー・スクロールに合わせた動き）を作ります。どれも「状態を変数やクラスで持ち、変わったら表示を切り替える」という同じ考え方でできています。

ここで作るUIは、オリジナルHPの自由課題（[08_js_renderの制作課題](../08_js_render/#制作課題オリジナルhpステップ3)）や、フロントエンド編の機能をすべて盛り込んだ作例（[11_homepage/sample](../11_homepage/sample/)）で使っています。

## 目次

1. [タブ切り替え](#1-タブ切り替え)
2. [ポップアップ](#2-ポップアップ)
3. [モーダルウィンドウ](#3-モーダルウィンドウ)
4. [スライドショー](#4-スライドショー)
5. [スクロール動作](#5-スクロール動作)

---

## フォルダ構成

```
01_frontend/09_js_ui/
├── README.md
├── example/                      サンプル（1つのサンプル＝1つのフォルダ）
│   ├── 01_tabs/                  タブ切り替え
│   │   ├── index.html
│   │   └── script.js
│   ├── 02_popup/                 ポップアップ（popover）
│   │   ├── index.html
│   │   └── script.js
│   ├── 03_modal/                 モーダルウィンドウ（dialog）
│   │   ├── index.html
│   │   └── script.js
│   ├── 04_slideshow/             スライドショー
│   │   ├── index.html
│   │   └── script.js
│   └── 05_scroll/                スクロール動作
│       ├── index.html
│       └── script.js
└── question/                     練習問題（4問。問題文はREADMEの各節の最後）
    ├── 01_two_tabs/              練習問題1：1ページにある2つのタブを、同じ関数で動かす
    │   ├── index.html
    │   └── script.js
    ├── 02_menu_toast/            練習問題2：「⋯」メニューと、自動で消える通知を作る
    │   ├── index.html
    │   └── script.js
    ├── 03_gallery/               練習問題3：モーダルウィンドウで作品ギャラリーを作る
    │   ├── index.html
    │   └── script.js
    ├── 04_scroll_article/        練習問題4：目次付きの長い記事を、スクロールで読みやすくする
    │   ├── index.html
    │   └── script.js
    └── answer/                   解答（問題と同じ名前のフォルダ。中のファイル構成も問題と同じ）
        ├── 01_two_tabs/
        ├── 02_menu_toast/
        ├── 03_gallery/
        └── 04_scroll_article/
```

---

## 1. タブ切り替え

> [example/01_tabs/index.html](example/01_tabs/index.html) / [example/01_tabs/script.js](example/01_tabs/script.js)

タブは、限られた場所に複数の内容を入れて、ボタンで切り替えるUIです。プロフィールの「スキル」「経歴」「趣味」のように、同じ種類の情報を分けて見せたいときに使います。

```html
<div class="tab-list" role="tablist">
    <button type="button" role="tab" aria-controls="panel-skills" aria-selected="true">スキル</button>
    <button type="button" role="tab" aria-controls="panel-history" aria-selected="false">経歴</button>
</div>
<div role="tabpanel" id="panel-skills">…</div>
<div role="tabpanel" id="panel-history" hidden>…</div>
```

```javascript
const selectTab = (selected) => {
    tabs.forEach((tab) => {
        const isSelected = tab === selected;
        tab.setAttribute('aria-selected', isSelected);
        const panel = document.getElementById(tab.getAttribute('aria-controls'));
        panel.hidden = !isSelected;
    });
};
```

### ポイント

| 書き方 | 説明 |
|---|---|
| `hidden`属性 / `要素.hidden = true` | 要素を隠す（`display: none`と同じ）。HTMLの属性としても、JavaScriptのプロパティとしても使える |
| `aria-selected="true"` | 選ばれているタブであることを、読み上げソフトに伝える。CSSでは`[aria-selected="true"]`で見た目を変える |
| `aria-controls="パネルのid"` | そのタブが、どのパネルを切り替えるか。JavaScriptではこれをたどってパネルを探す |
| `role="tablist"` / `"tab"` / `"tabpanel"` | 「これはタブだ」という役割を伝える（HTMLにタブ専用のタグが無いため） |
| ← → キーでの移動 | タブの一般的な操作方法。`keydown`で`event.key`が`'ArrowRight'`・`'ArrowLeft'`のときに隣のタブを選ぶ。最初・最後へは`'Home'`・`'End'`。そのほかのキー名は`'ArrowUp'`・`'ArrowDown'`・`'Escape'`・`' '`（スペース）など |
| `tabIndex`（`tabindex`属性） | Tabキーで移動できるかを決める数値。`0`＝Tabキーで止まる、`-1`＝Tabキーでは飛ばす（JavaScriptの`focus()`では選べる）。タブでは、選ばれているタブだけ`0`、ほかを`-1`にして、Tabキーで次の部品へ進み、タブの間は矢印キーで動くようにする |
| `document.activeElement` | 今フォーカスされている要素。`tabs.indexOf(document.activeElement)`で「何番目のタブにフォーカスがあるか」がわかる |
| `配列.indexOf(要素)` と `Array.from()` | 何番目か（0始まり）を調べる。`querySelectorAll`が返す`NodeList`には`indexOf`が無いので、`Array.from(...)`で配列に変えてから使う（08_js_render 1節） |
| `要素.focus()` | フォーカスを移す。矢印キーで選んだタブに、見た目だけでなくキーボードの操作対象も移すために呼ぶ |

08_js_render 3節の絞り込みと同じく、「選ばれたものに印を付け、それ以外から外す」という考え方です。クラスの代わりに`aria-selected`と`hidden`を使うと、見た目とアクセシビリティを同時に扱えます。

### 動作確認

`example/01_tabs/index.html`をブラウザで開いて確認します。

| 確認する操作 | 確認したいこと |
|---|---|
| 「経歴」タブを押す | 「経歴」に下線が付き、経歴の内容だけが表示される |
| Elementsパネルで操作を見る | 押したタブの`aria-selected`が`"true"`に、他のパネルに`hidden`属性が付く |
| 「スキル」タブをクリックしてから → キーを押す | 隣の「経歴」タブに切り替わる。「趣味」で → を押すと「スキル」に戻る |


### 練習問題1：1ページにある2つのタブを、同じ関数で動かす

> 問題：[question/01_two_tabs/index.html](question/01_two_tabs/index.html)・[question/01_two_tabs/script.js](question/01_two_tabs/script.js) ｜ 解答：[question/answer/01_two_tabs/index.html](question/answer/01_two_tabs/index.html)・[question/answer/01_two_tabs/script.js](question/answer/01_two_tabs/script.js)

<details>
<summary>問題の内容を開く</summary>

`01_two_tabs/index.html`には`.tabs`が**2つ**あります。[example/01_tabs/script.js](example/01_tabs/script.js)のように`id`で1つだけ取り出して書くと、同じコードを2回書くことになります。そこで、「`.tabs`の要素を1つ受け取って動くようにする関数」`setupTabs(container)`を作り、2つの`.tabs`それぞれに対して呼び出します。HTMLとCSSは完成しています。

| # | 仕様 |
|---|---|
| 1 | タブを押すと、そのタブの`aria-selected`を`"true"`・`tabIndex`を`0`にし、他のタブは`aria-selected="false"`・`tabIndex`を`-1`にする。対応するパネル（`aria-controls`の`id`）だけを表示し、他のパネルは`hidden`にする |
| 2 | タブにフォーカスがあるとき、→で次・←で前のタブを選んでフォーカスを移す（最後の次は最初、最初の前は最後）。Homeで最初、Endで最後のタブ |
| 3 | 上のタブを操作しても、下のタブには影響しない（逆も同じ） |

`01_two_tabs/script.js`には次の4つを書きます。`setupTabs`の中では`document`ではなく`container`から探すと、「この`.tabs`の中のタブ」だけが取り出せます。

| # | やること | ヒント |
|---|---|---|
| 1 | `selectTab(selected)`：渡されたタブを選び、他のタブの選択を外す（仕様1） | パネルは`document.getElementById(tab.getAttribute('aria-controls'))` |
| 2 | クリックで切り替える | `tabList`に1回だけ`addEventListener`し、`event.target.closest('[role="tab"]')`で押されたタブを探す |
| 3 | キーボードで切り替える（`tabList`の`'keydown'`イベント、仕様2） | 今のタブの番号は`tabs.indexOf(document.activeElement)`。端で反対側に回るのは`%`で割った余り。それ以外のキーでは何もしない。選んだら`selectTab()`して`focus()`する。Home / Endはページのスクロールにも使われるので、`event.preventDefault()`で止める |
| 4 | ページ内のすべての`.tabs`に対して`setupTabs()`を呼ぶ | `document.querySelectorAll('.tabs')` |

| 確認する操作 | 確認したいこと |
|---|---|
| 「プロフィール」で「経歴」を押す | 経歴だけが表示される。「メモ」のタブは変わらない |
| 「メモ」の「仕事」をクリックしてからEndキーを押す | 「趣味」が選ばれる。続けて→キーを押すと「すべて」に戻る |
| Elementsパネルを見ながら操作する | 操作したタブの`aria-selected`と、パネルの`hidden`が切り替わる |

</details>

---

## 2. ポップアップ

> [example/02_popup/index.html](example/02_popup/index.html) / [example/02_popup/script.js](example/02_popup/script.js)

**ポップアップ**は、ボタンを押したときに小さな窓を手前に出すUIです。メニュー・ヘルプ・通知などに使います。後ろの画面はそのまま操作でき、外側をクリックすると閉じます。HTMLの`popover`属性を使うと、JavaScriptを書かなくても作れます。

```html
<button type="button" popovertarget="menu">メニュー ▾</button>
<div id="menu" popover>
    <ul>…</ul>
</div>
```

`popovertarget="ポップアップのid"`を付けたボタンを押すと、そのポップアップが開閉します。外側のクリックやEscキーで閉じる動作も、ブラウザが自動で付けてくれます。

JavaScriptで開閉することもできます。自動で消える通知（トースト）は、`popover="manual"`（外側をクリックしても閉じない）にして、`setTimeout`で閉じます。

```javascript
toast.showPopover();                 // 開く
clearTimeout(hideTimer);             // 連続で押されたときは、前のタイマーを取り消す
hideTimer = setTimeout(() => {
    toast.hidePopover();             // 3秒後に閉じる
}, 3000);
```

### ポイント

| 書き方 | 説明 |
|---|---|
| `popover`属性 | その要素をポップアップにする。最初は表示されず、開くと他の要素より手前に表示される |
| `popovertarget="id"` | ボタンに付けると、押したときにそのidのポップアップを開閉する |
| `popover="manual"` | 外側のクリックやEscキーでは閉じない。開閉はJavaScriptで行う |
| `要素.showPopover()` / `hidePopover()` | JavaScriptで開く / 閉じる |
| `toggle`イベント | 開いた・閉じたときに発生する。`event.newState`が`'open'`か`'closed'` |
| `setTimeout(関数, ミリ秒)` / `clearTimeout(番号)` | 指定した時間のあとに**1回だけ**関数を呼ぶ / その予約を取り消す |
| `role="status"` | 通知に付けると、中身が変わったときに読み上げソフトが読み上げる（画面を見ていなくても「保存しました」が伝わる） |

ポップアップは、何も位置を指定しないと画面の中央に表示されます。ボタンのすぐ下に出したい場合は、CSSで位置を指定します。

### ポップアップとモーダルウィンドウの違い

| | ポップアップ（2節） | モーダルウィンドウ（3節） |
|---|---|---|
| 後ろの画面 | そのまま操作できる | 閉じるまで操作できない（暗くなる） |
| 閉じ方 | 外側のクリック・Escキー | 閉じるボタン・Escキー（背景クリックは自分で書く） |
| HTML | `popover`属性 | `<dialog>`要素＋`showModal()` |
| 向いている用途 | メニュー・ヘルプ・通知など、ちょっとした補足 | 確認・詳細表示・入力など、そこに集中してほしい内容 |

### 動作確認

`example/02_popup/index.html`をブラウザで開いて確認します。

| 確認する操作 | 確認したいこと |
|---|---|
| 「メニュー ▾」を押す | メニューが手前に表示される。もう一度押すと閉じる |
| メニューを開いたまま、外側をクリックする・Escキーを押す | どちらでも閉じる |
| 「メニュー」を開いたまま「？ ヘルプ」を押す | メニューが閉じて、ヘルプが開く（`popover`は1つずつ開く） |
| 「保存する」を押す | 右下に「保存しました」が出て、3秒後に消える。出ている間もページは操作できる |


### 練習問題2：「⋯」メニューと、自動で消える通知を作る

> 問題：[question/02_menu_toast/index.html](question/02_menu_toast/index.html)・[question/02_menu_toast/script.js](question/02_menu_toast/script.js) ｜ 解答：[question/answer/02_menu_toast/index.html](question/answer/02_menu_toast/index.html)・[question/answer/02_menu_toast/script.js](question/answer/02_menu_toast/script.js)

<details>
<summary>問題の内容を開く</summary>

メモカードの「⋯」ボタンで開くメニューと、操作の結果を知らせる通知を作ります。CSSは完成しています。先に`02_menu_toast/index.html`の`TODO 1`・`TODO 2`（HTMLだけで書く部分）を書いてから、`02_menu_toast/script.js`の`TODO 3`〜`TODO 5`に取りかかります。

| # | 書く場所 | やること |
|---|---|---|
| 1 | `02_menu_toast/index.html`の各カード | 「⋯」ボタンを押すと、そのカードのメニュー（`.menu-popup`）が開閉し、外側のクリックやEscキーで閉じるようにする（`popover`属性と`popovertarget`属性を使う。JavaScriptは書かない） |
| 2 | `02_menu_toast/index.html`の`#toast` | 外側をクリックしても閉じないポップアップにする |
| 3 | `showToast(message)` | 通知の文字を`message`にして開き、2秒後に閉じる。2秒以内にもう一度呼ばれたら、そこからまた2秒数え直す（前のタイマーを`clearTimeout()`で取り消してから`setTimeout()`する）。すでに開いているポップアップに`showPopover()`するとエラーになるので、`toast.matches(':popover-open')`で調べて、開いていないときだけ開く |
| 4 | メニューの中のボタン | 各メニューに`'click'`を1回だけ登録し、`event.target.dataset.action`（`copy` / `delete`）で押されたボタンを判定する。メニューを`hidePopover()`で閉じ、「『買い物リスト』をコピーしました」「『買い物リスト』を削除しました」のように`showToast()`する。タイトルは`menu.closest('.card').querySelector('h2').textContent`（この問題では、実際にコピー・削除はしなくてよい） |
| 5 | メニューの開閉 | メニューが開いたら「⋯」ボタンの`aria-expanded`を`"true"`に、閉じたら`"false"`にする。`'toggle'`イベントの`event.newState`（`'open'` / `'closed'`）を使う。ボタンは`` document.querySelector(`[popovertarget="${menu.id}"]`) `` |

| 確認する操作 | 確認したいこと |
|---|---|
| 「⋯」を押す | メニューが開き、外側クリック・Esc・もう一度「⋯」で閉じる |
| 1枚目のメニューを開いたまま、2枚目の「⋯」を押す | 1枚目が閉じて2枚目が開く |
| 「コピー」を押す | メニューが閉じ、右下に通知が出て2秒後に消える |
| 通知が出ている間に、別のカードで「削除」を押す | 通知の文字が変わり、そこから2秒後に消える |
| Elementsパネルを見ながら開閉する | 「⋯」ボタンの`aria-expanded`が切り替わる |

</details>

---

## 3. モーダルウィンドウ

> [example/03_modal/index.html](example/03_modal/index.html) / [example/03_modal/script.js](example/03_modal/script.js)

**モーダルウィンドウ**は、画面の手前に窓を出し、閉じるまで後ろの画面を操作できなくするUIです。2節のポップアップと違い、閉じるまで他の操作をさせないので、ユーザーにその内容に集中してほしいときに使います。作品の詳細表示や、確認のメッセージに使います。HTMLには、そのための`<dialog>`要素があります。

```html
<dialog id="work-dialog">
    <div class="dialog-body">
        <h2 id="dialog-title"></h2>
        <button type="button" id="dialog-close">閉じる</button>
    </div>
</dialog>
```

```javascript
dialogTitle.textContent = button.dataset.title;   // 中身を書き換えてから
dialog.showModal();                               // 開く

closeButton.addEventListener('click', () => dialog.close());   // 閉じる

dialog.addEventListener('click', (event) => {     // 暗い背景をクリックしたら閉じる
    if (event.target === dialog) {
        dialog.close();
    }
});
```

### ポイント

| 書き方 | 説明 |
|---|---|
| `dialog.showModal()` | モーダルとして開く。後ろの画面は操作できなくなり、**Escキーで閉じる動作**と、フォーカスをダイアログの中に移す動作をブラウザが自動で付けてくれる |
| `dialog.close()` | 閉じる。フォーカスは開く前の要素に戻る |
| `dialog.open` | 今開いているか（`true`/`false`） |
| `dialog::backdrop` | モーダルの後ろの暗い背景をCSSで指定する疑似要素 |
| `body:has(dialog[open]) { overflow: hidden; }`（CSS） | 開いている間、後ろのページをスクロールさせない。`:has()`は「〜を含む要素」を選ぶ疑似クラス |
| 背景クリックの判定 | 背景をクリックすると`event.target`が`<dialog>`自身になる。`<dialog>`に`padding`を付けると、その余白のクリックも背景と同じ扱いになってしまうので、中身を別の要素（`.dialog-body`）で包み、余白はそちらに付ける |

`confirm()`（06_js_events 3節）も小さなモーダルウィンドウですが、見た目を変えられず、中にボタンやリンクを置けません。自分でデザインした窓を出したいときは`<dialog>`を使います。

### 確認してから送信する

「削除しますか？」のような確認を`<dialog>`で出すときは、`confirm()`のように「答えが出るまで待つ」ことができません。そこで、フォームの送信をいったん止めてダイアログを開き、「OK」が押されたら、覚えておいたフォームを送信します。

```javascript
let pendingForm = null;   // 確認中のフォーム

deleteForm.addEventListener('submit', (event) => {
    event.preventDefault();          // いったん送信を止める（06_js_events 3節）
    pendingForm = deleteForm;
    dialog.showModal();
});

okButton.addEventListener('click', () => {
    dialog.close();
    pendingForm.submit();            // 覚えておいたフォームを送信する
});

cancelButton.addEventListener('click', () => dialog.close());
```

`フォーム.submit()`は、JavaScriptからフォームを送信します。このとき`submit`イベントは**起きない**ので、上の`submit`の処理（送信を止めてダイアログを開く）がもう一度動くことはありません。完成例の[02_backend/100_memo_api](../../02_backend/100_memo_api/)の削除ボタンが、この書き方です。

### 動作確認

`example/03_modal/index.html`をブラウザで開いて確認します。

| 確認する操作 | 確認したいこと |
|---|---|
| 「メモ帳アプリ」を押す | 画面が暗くなり、手前に「メモ帳アプリ」の説明が表示される。後ろの作品はクリックできない |
| 「閉じる」を押す・Escキーを押す・暗い背景をクリックする | いずれの方法でも閉じる |
| ダイアログの中（文章のあたり）をクリックする | 閉じない |
| 少し下にスクロールしてから作品を開き、マウスホイールを回す | 後ろのページがスクロールしない。閉じるとスクロールできる |
| キーボードだけで、作品にTabで移動してEnterで開き、Escで閉じる | 閉じた後、フォーカスが元の作品のボタンに戻っている |

---

## 4. スライドショー

> [example/04_slideshow/index.html](example/04_slideshow/index.html) / [example/04_slideshow/script.js](example/04_slideshow/script.js)

スライドショー（カルーセル）は、複数の画像や内容を1枚ずつ順番に見せるUIです。ここでは、前へ・次へボタン・何枚目かを示すドット・一定時間ごとの自動再生を作ります。

```javascript
let current = 0;   // 今何枚目か（状態）

const show = (n) => {
    current = (n + slides.length) % slides.length;   // 範囲外なら回り込ませる
    slides.forEach((slide, index) => {
        slide.classList.toggle('active', index === current);
    });
};

prevButton.addEventListener('click', () => show(current - 1));
nextButton.addEventListener('click', () => show(current + 1));

// 自動再生
let timerId = setInterval(() => show(current + 1), 3000);   // 3秒ごとに次へ
slideshow.addEventListener('mouseenter', () => clearInterval(timerId));   // ホバー中は止める
```

### ポイント

| 書き方 | 説明 |
|---|---|
| 「今何枚目か」を変数で持つ | 前へ・次へ・ドット・自動再生は、すべて`show(番号)`を呼ぶだけにする。表示の処理を1か所にまとめると、ずれが起きない |
| `(n + 枚数) % 枚数` | `%`は割った余り。最後の次（`n = 枚数`）は`0`に、最初の前（`n = -1`）は最後に回り込む |
| `forEach((要素, index) => …)` | コールバックの2つ目の引数で、何番目か（0始まり）がわかる |
| `setInterval(関数, ミリ秒)` | 一定時間ごとに関数を呼び続ける。戻り値の番号を`clearInterval(番号)`に渡すと止まる |
| `setTimeout(関数, ミリ秒)` | 一定時間後に**1回だけ**関数を呼ぶ（参考） |
| `mouseenter`/`mouseleave`・`focusin`/`focusout` | マウスを乗せている間・ボタンにフォーカスがある間は自動再生を止める。読んでいる途中で切り替わらないようにするため |
| CSSの重ね方 | すべてのスライドをGridの同じマス（`grid-area: 1 / 1`）に重ね、表示中のものだけ`opacity: 1`にする。`transition`でふわっと切り替わる |

自動で動き続ける表示は、内容を読み切れない人や、動きで気分が悪くなる人もいます。止める手段を用意し、OSの「動きを減らす」設定（`prefers-reduced-motion`、04_css_layout 5節）のときは自動再生しないようにします。

### 動作確認

`example/04_slideshow/index.html`をブラウザで開いて確認します。

| 確認する操作 | 確認したいこと |
|---|---|
| 何もせずに待つ | 3秒ごとにスライドがふわっと切り替わり、下のドットも移動する |
| スライドの上にマウスを乗せたまま待つ | 切り替わらない（「一時停止中」と表示される）。マウスを外すと再開する |
| 「›」を3回押す | 1→2→3→1と、最後の次は最初に戻る。「‹」では逆に回る |
| 2つ目のドットを押す | 2枚目が表示される |
| Tabキーで「›」ボタンにフォーカスする | フォーカスがある間は自動再生が止まる |


### 練習問題3：モーダルウィンドウで作品ギャラリーを作る

> 問題：[question/03_gallery/index.html](question/03_gallery/index.html)・[question/03_gallery/script.js](question/03_gallery/script.js) ｜ 解答：[question/answer/03_gallery/index.html](question/answer/03_gallery/index.html)・[question/answer/03_gallery/script.js](question/answer/03_gallery/script.js)

<details>
<summary>問題の内容を開く</summary>

3節（モーダルウィンドウ）と4節（スライドショー）を組み合わせて、作品を順番に見られるギャラリーを作ります。HTMLとCSSは完成しています。

| # | 仕様 |
|---|---|
| 1 | 一覧の作品（`.thumb`ボタン）をクリックすると、`<dialog>`を`showModal()`で開き、その作品の色（`data-color`）・タイトル（`data-title`）と「2 / 5」のような番号を表示する |
| 2 | ダイアログの「‹」「›」ボタンで、前・次の作品に切り替える（最後の次は最初、最初の前は最後） |
| 3 | ダイアログが開いている間は、← →キーでも前・次に切り替えられる |
| 4 | 「閉じる」ボタン・Escキー・暗い背景のクリックで閉じる |

`03_gallery/script.js`には次の4つを書きます。

| # | やること | ヒント |
|---|---|---|
| 1 | `show(n)`：n番目の作品をダイアログに表示する。`current`をnにし（範囲外なら回り込ませる）、`viewer`の背景色と文字、`counter`の「2 / 5」を更新する | 回り込み：`(n + thumbs.length) % thumbs.length`。背景色は`viewer.style.background`。`current`は0始まりなので、表示は+1する |
| 2 | 一覧の作品がクリックされたら、その作品を`show()`してから`dialog.showModal()`で開く | 親の`#gallery`に1回だけイベントを登録し、`event.target.closest('.thumb')`で押された作品を探す。何番目かは`thumbs.indexOf(押された作品)` |
| 3 | `#prev`・`#next`で`show(current - 1)` / `show(current + 1)`、`#close`で`dialog.close()`。暗い背景のクリックでも閉じる | 背景のクリックは`event.target === dialog`のとき |
| 4 | ダイアログが開いている間（`dialog.open`が`true`）だけ、← →キーで前・次に切り替える | `document`に`keydown`を登録し、`event.key`が`'ArrowLeft'` / `'ArrowRight'`かを見る |

| 確認する操作 | 確認したいこと |
|---|---|
| 3番目の作品を押す | ダイアログが開き、その作品の色・タイトルと「3 / 5」が表示される |
| 「›」を3回押す | 5番目の次は1番目に戻る |
| ← →キーを押す | 前・次に切り替わる。ダイアログを閉じた後は、キーを押しても何も起きない |
| 「閉じる」・Escキー・暗い背景のクリック | どれでも閉じる |

</details>

---

## 5. スクロール動作

> [example/05_scroll/index.html](example/05_scroll/index.html) / [example/05_scroll/script.js](example/05_scroll/script.js)

縦に長いページでは、スクロールに合わせて表示を変えると読みやすくなります。ここでは、よく使う4つの動きを作ります。

### なめらかなスクロール（CSS）

ページ内リンク（`<a href="#works">`）で移動するとき、一瞬で飛ばずになめらかにスクロールさせるのは、CSSの1行でできます。

```css
html {
    scroll-behavior: smooth;
}

section {
    scroll-margin-top: 70px;   /* 上に固定したヘッダーの分だけ、止まる位置を下げる */
}
```

### scrollイベントで表示を変える

```javascript
window.addEventListener('scroll', () => {
    const y = window.scrollY;                       // 一番上から何px下までスクロールしたか

    header.classList.toggle('scrolled', y > 10);    // 少しでもスクロールしたらヘッダーに影
    toTop.hidden = y < 300;                         // 300px以上で「トップへ戻る」を表示

    const max = document.documentElement.scrollHeight - window.innerHeight;
    progress.style.width = `${(y / max) * 100}%`;   // どこまで読んだかのバー
});
```

### JavaScriptでスクロールさせる

```javascript
window.scrollTo({ top: 0, behavior: 'smooth' });                          // ページの一番上へ
document.getElementById('contact').scrollIntoView({ behavior: 'smooth' });  // その要素が見える位置へ
```

### 画面に入った要素をふわっと表示する（IntersectionObserver）

```javascript
const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
        if (entry.isIntersecting) {                // 画面に入った
            entry.target.classList.add('visible');
            observer.unobserve(entry.target);      // 1回表示したら監視をやめる
        }
    });
}, { threshold: 0.2 });                            // 20%見えたら「入った」とみなす

document.querySelectorAll('.fade-in').forEach((el) => observer.observe(el));
```

### ポイント

| 書き方 | 説明 |
|---|---|
| `window.scrollY` | ページの一番上から、何pxスクロールしたか |
| `document.documentElement.scrollHeight` / `window.innerHeight` | ページ全体の高さ / 画面に見えている部分の高さ。差がスクロールできる最大の量 |
| `scroll`イベント | スクロール中に何度も（1秒に数十回）発生する。中の処理は、クラスの付け外しなど軽いものにする |
| `Math.floor(数値)` | 小数点以下を切り捨てる。読了率を整数のパーセントで表示するときに使う（`Math.floor(3.9)` → `3`） |
| `要素.style.width = '50%'` | JavaScriptでCSSを直接書き込む。計算した幅や色を入れるときに使う（07_js_dom 1節） |
| `window.scrollTo({ top, behavior: 'smooth' })` | 指定した位置までスクロールする |
| `要素.scrollIntoView({ behavior: 'smooth' })` | その要素が見える位置までスクロールする |
| `IntersectionObserver` | 要素が画面に入った・出たときだけ知らせてくれる。「画面に入ったら〜する」は、`scroll`イベントで位置を計算するより、こちらの方が軽くて簡単 |
| `scroll-behavior: smooth`（CSS） | ページ内リンクの移動をなめらかにする |
| `scroll-margin-top`（CSS） | 固定ヘッダーに見出しが隠れないよう、ジャンプ先の止まる位置をずらす |

なめらかなスクロールや、ふわっと表示する動きは、OSで「動きを減らす」を設定している人には不要なこともあります。サンプルでは`prefers-reduced-motion`のときに`scroll-behavior`を戻しています（04_css_layout 5節）。

3節のモーダルウィンドウでは、開いている間に後ろのページがスクロールしないよう、`body:has(dialog[open]) { overflow: hidden; }`を指定しています。スクロールを止めたいときは`overflow: hidden`を使う、と覚えておきましょう。

### 動作確認

`example/05_scroll/index.html`をブラウザで開いて確認します。

| 確認する操作 | 確認したいこと |
|---|---|
| ヘッダーの「作品」を押す | 「作品」の見出しまでなめらかにスクロールし、見出しがヘッダーに隠れずに止まる |
| 少しスクロールする | ヘッダーの下に影が付き、青いバーが伸びていく。一番下までスクロールするとバーが右端まで届く |
| 300px以上スクロールする | 右下に「↑」ボタンが出る。押すとなめらかに一番上に戻り、ボタンが消える |
| ゆっくり下にスクロールする | カードが画面に入るたびに、下からふわっと表示される |
| 「連絡先へ移動（JavaScript）」を押す | 「連絡先」までなめらかにスクロールする |


### 練習問題4：目次付きの長い記事を、スクロールで読みやすくする

> 問題：[question/04_scroll_article/index.html](question/04_scroll_article/index.html)・[question/04_scroll_article/script.js](question/04_scroll_article/script.js) ｜ 解答：[question/answer/04_scroll_article/index.html](question/answer/04_scroll_article/index.html)・[question/answer/04_scroll_article/script.js](question/answer/04_scroll_article/script.js)

<details>
<summary>問題の内容を開く</summary>

`04_scroll_article/index.html`のHTMLは完成しています。`<style>`の`TODO 1`・`TODO 2`と、`04_scroll_article/script.js`の`TODO 3`〜`TODO 5`を書きます。

| # | 書く場所 | やること |
|---|---|---|
| 1 | `<style>`の最初 | 目次のリンクで移動するとき、なめらかにスクロールする。ただし、OSで「動きを減らす」を設定している人には、なめらかにしない |
| 2 | `section` | 移動したとき、節の見出しが上の固定ヘッダー（高さ56px）に隠れないよう、止まる位置を「56px＋少しの余白」だけ下げる |
| 3 | `onScroll()` | ヘッダーの右端に「読了 ◯%」と表示する。読了率＝スクロールした量（`window.scrollY`）÷スクロールできる最大の量（`document.documentElement.scrollHeight - window.innerHeight`）×100。小数は`Math.floor()`で切り捨て、一番下で100% |
| 4 | `onScroll()`と、その下 | 400px以上スクロールしたら「↑ トップへ」ボタンを表示し（それより上なら`hidden`）、押すとなめらかに一番上へ戻る |
| 5 | 一番下 | 今読んでいる節の目次のリンクに`aria-current="true"`を付け、他のリンクからは外す（CSSで`[aria-current="true"]`が青く太字になる）。下で説明する`IntersectionObserver`を使う |

TODO 5では、`IntersectionObserver`の`rootMargin`を使います。

```javascript
new IntersectionObserver(コールバック, { rootMargin: '-50% 0px -50% 0px' });
```

`rootMargin`は「画面の範囲を、上下左右にどれだけ広げる（マイナスなら縮める）か」です。上下を`-50%`にすると、判定する範囲が「画面の上下の真ん中の線」だけになるので、`isIntersecting`が`true`になるのは「真ん中の線を横切っている節」だけになります。

コールバックの中で、`isIntersecting`が`true`の節（`entry.target`）の`id`と、`href`が一致する目次のリンクに印を付けます。リンクの`href`は`link.getAttribute('href')`で`'#usage'`のように取り出せます（`link.href`だと完全なURLになる）。印を外すのは`要素.removeAttribute('aria-current')`です。最後に、すべての`section`を`observe()`します。

| 確認する操作 | 確認したいこと |
|---|---|
| 目次の「3. 使い方」を押す | なめらかに移動し、見出しがヘッダーに隠れずに止まる |
| ゆっくりスクロールする | 読了率が増えていき、今読んでいる節の目次が青くなる |
| 一番下までスクロールする | 「読了 100%」になる |
| 「↑ トップへ」を押す | 一番上に戻り、ボタンが消える |

</details>

---

## 次のステップ

続きは [10_js_data](../10_js_data/) です。JSON形式のデータを読み込み・保存し、データから画面を作る方法を学びます。
