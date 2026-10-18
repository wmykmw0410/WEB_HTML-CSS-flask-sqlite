# 02 メモアプリを完成させる

> バックエンド編 ／ 前の章：[01_intro](../01_intro/) ／ 次の章：[03_function](../03_function/)

バックエンド編の出発点となる章です。まずは、フロントエンド編で学んだHTML・CSS・JavaScriptだけを使って、**ブラウザだけで動くメモアプリ**を作ります。メモの追加・詳細表示・編集・削除・ピン留め・絞り込み・検索ができ、データは`localStorage`に保存されるので、ページを閉じても消えません。

画面は、バックエンド編の完成形[100_memo_api](../100_memo_api/)と**同じデザイン・同じ操作**です（CSSは100と同じファイル）。違いはデータの保存先だけで、100ではサーバー（Flask＋データベース）に、この章ではブラウザの`localStorage`に保存します。

新しい文法はほとんど使いません。フロントエンド編で学んだことを組み合わせて、1つのアプリを設計して作り上げることがこの章の目的です。そして、完成したアプリを使ってみて「ブラウザだけでは何ができないのか」を確かめます（章の最後の「このアプリの限界とバックエンド編」）。その限界を、次の`03_function`からサーバー側の技術で1つずつ解決していくのが、バックエンド編の流れです。

## 前提

| チャプター | 使う知識 |
|---|---|
| 01_frontend/02_html_semantic_form・01_frontend/04_css_layout | HTMLとCSSの読み方（この章のHTMLとCSSは用意済み） |
| 01_frontend/05_js_basics・01_frontend/06_js_events・01_frontend/07_js_dom・01_frontend/08_js_render | 基本文法・コールバック関数・DOM操作・イベント・`preventDefault()` |
| 01_frontend/09_js_ui | 通知（`popover`）・確認ダイアログ（`<dialog>`）・スクロール（この章では完成済みの`common.js`で使う） |
| 01_frontend/10_js_data | JSON・`fetch()`・`localStorage`・「データを変える → 保存 → 描画」 |

## 目次

1. [アプリの設計](#1-アプリの設計) — 画面・データの形・ファイルの役割
2. [進め方](#2-進め方)
3. [ステップ1：データの保存と読み込み](#ステップ1データの保存と読み込みstoragejs)
4. [ステップ2：一覧を表示する](#ステップ2一覧を表示するlistjs)
5. [ステップ3：並び替え・絞り込み・検索](#ステップ3並び替え絞り込み検索listjs)
6. [ステップ4：メモを追加する](#ステップ4メモを追加するformjs)
7. [ステップ5：詳細ページと編集ページ](#ステップ5詳細ページと編集ページdetailjsformjs)
8. [ステップ6：ピン留めと削除](#ステップ6ピン留めと削除listjsdetailjs)
9. [完成したら：全体の動作確認](#完成したら全体の動作確認)
10. [このアプリの限界とバックエンド編](#このアプリの限界とバックエンド編)

---

## フォルダ構成

```
02_backend/02_memo_app_frontend/
├── README.md
└── challenge/                 演習（ここに書き込んでいく）
    ├── index.html             メモ一覧（絞り込み・検索・ピン留め・削除）
    ├── detail.html            メモの詳細（detail.html?id=3 のようにIDを付けて開く）
    ├── new.html               メモの追加（下書きの自動保存つき）
    ├── edit.html              メモの編集（edit.html?id=3）
    ├── css/style.css          スタイル（完成済み。02_backend/100_memo_api と同じ）
    ├── img/favicon.svg
    ├── data/memos.json        初期データ（5件）
    ├── js/
    │   ├── storage.js         データ担当：localStorage への保存・読み込み（ステップ1）
    │   ├── common.js          全ページ共通：通知・確認ダイアログ・配色・メニューなど（完成済み）
    │   ├── list.js            一覧ページ担当（ステップ2・3・6）
    │   ├── detail.js          詳細ページ担当（ステップ5・6）
    │   └── form.js            追加・編集ページ担当（ステップ4・5）
    └── answer/                完成例（同じ構成）
```

HTMLとCSSは完成しています。書くのは`js/`の中の`TODO`の部分だけです。

---

## 1. アプリの設計

コードを書き始める前に、「どんな画面があり、どんなデータを、どのファイルが扱うか」を決めておきます。アプリが大きくなるほど、この設計が大切になります。

### 画面

| ページ | できること | 100_memo_api での同じページ |
|---|---|---|
| `index.html`（一覧） | メモをカードで一覧表示する。カテゴリで絞り込む・キーワードで検索する・★でピン留めする・削除する | `/memos/` |
| `detail.html?id=3`（詳細） | 指定したIDのメモを表示する。編集ページへ移動する・削除する | `/memos/3` |
| `new.html`（追加） | タイトル・カテゴリ・本文・期限を入力して保存する。入力中の内容は下書きとして自動保存される | `/memos/new` |
| `edit.html?id=3`（編集） | 指定したIDのメモの内容を、フォームに入れた状態で開き、更新する | `/memos/3/edit` |

100にある「ログイン」（ログインした人だけが追加・編集・削除できる）は、サーバーが必要な機能なので、この章にはありません。

### データの形

メモ1件は、次のようなオブジェクトです。全メモをこのオブジェクトの**配列**として`localStorage`に保存します。

```json
{
    "id": 1,
    "title": "買い物リスト",
    "category": "家事",
    "body": "牛乳、卵、パン、洗剤を買う。特売は火曜日まで。",
    "due_date": "2026-10-07",
    "is_pinned": true
}
```

| キー | 内容 |
|---|---|
| `id` | メモを区別する番号。詳細・編集・削除のときに「どのメモか」を指定するのに使う。新しいメモほど大きい |
| `due_date` | 期限（`input type="date"`の値と同じ`YYYY-MM-DD`形式）。無ければ`null` |
| `is_pinned` | ピン留めしているか（`true`/`false`） |

キーの名前は、100_memo_apiのデータベース（`memos`テーブル）の列の名前と同じにしています。バックエンド編でデータベースのテーブルを作るときも、この形をほぼそのまま使います。

### ファイルの役割

1つのファイルに全部を書くと、どこに何があるか分からなくなります。そこで**役割ごとにファイルを分けます**。

| ファイル | 担当 | 読み込むページ |
|---|---|---|
| `storage.js` | データの保存・読み込み。**`localStorage`を直接触るのはこのファイルだけ** | 全ページ |
| `common.js` | 全ページ共通の処理（完成済み）。通知`showToast()`・確認ダイアログ`openConfirm()`・ハンバーガーメニュー・配色の切り替え・トップへ戻るボタン・ふわっと表示`observeFadeIn()` | 全ページ |
| `list.js` | 一覧ページの表示と操作 | `index.html` |
| `detail.js` | 詳細ページの表示と削除 | `detail.html` |
| `form.js` | 追加・編集ページのフォーム | `new.html`・`edit.html` |

`<script>`は上から順に読み込まれ、先に読み込んだファイルで定義した関数（`loadMemos`・`showToast`など）を、後のファイルから使えます。そのため、`storage.js`→`common.js`→各ページのファイルの順に読み込みます。

`localStorage`を触る処理を`storage.js`に集めておくと、保存先を変えたくなったときに、このファイルだけを書き換えれば済みます。バックエンド編で保存先をサーバーに移すときに、この分け方が効いてきます。

### common.js の2つの道具

`common.js`の関数のうち、各ページのファイルから呼ぶのは次の2つです。

```javascript
showToast('ピン留めしました');            // 右下に通知を出し、3秒で消す
showToast('保存できませんでした', true);   // 2つ目を true にすると赤い通知

openConfirm('削除しますか？', () => {
    // 「OK」が押されたときだけ、ここが呼ばれる（キャンセル・Esc・背景のクリックでは呼ばれない）
});
```

`openConfirm()`は、`confirm()`（01_frontend/06_js_events 3節）の代わりに、`<dialog>`（01_frontend/09_js_ui 3節）で確認します。`confirm()`のように「答えが出るまで待つ」ことはできないので、OKのときにしてほしい処理を**コールバック関数**（01_frontend/05_js_basics 2節）で渡します。

### 処理の流れ

```
【どのページも、開いたとき】
  initMemos() ── localStorage にあれば読み込む ／ 無ければ data/memos.json を fetch して保存

【一覧ページ】
  render() ──── 並び替え・絞り込み・検索をして、カードを作る
  ★・削除・絞り込み・検索 → 状態（memos・selectedCategory・keyword）を変える
                          → saveMemos()（データを変えたときだけ）→ render()

【詳細・編集ページ】
  URL の ?id=3 から、どのメモかを決める（getIdFromUrl()）

【追加・編集ページで保存】
  入力チェック → memos に追加 or 書き換え → saveMemos() → 詳細ページに移動（location.href）
```

---

## 2. 進め方

`fetch()`を使うので、サーバー経由で開きます。

```bash
cd 02_backend/02_memo_app_frontend
python -m http.server 8000
# → http://localhost:8000/challenge/        自分の実装
#    http://localhost:8000/challenge/answer/ 完成例
```

`challenge/`と`challenge/answer/`は同じアドレス（`localhost:8000`）なので、`localStorage`を共有します。完成例で追加したメモが自分の実装にも表示されるなど、混乱するときは、一覧ページ下の「データを初期状態に戻す」を押してください。

| ステップ | 書くファイル | 内容 | 使う章 |
|---|---|---|---|
| 1 | `storage.js` | `localStorage`への保存・読み込みと、初期データの読み込み | 01_frontend/10_js_data 1〜4節 |
| 2 | `list.js` | データからカードを作って一覧を表示する | 01_frontend/10_js_data 5節 |
| 3 | `list.js` | 並び替え・カテゴリの絞り込み・キーワード検索・選んだカテゴリを覚える | 01_frontend/08_js_render 1節・3節・練習問題3 |
| 4 | `form.js` | フォームの内容から新しいメモを作って保存する | 01_frontend/06_js_events 3節 |
| 5 | `detail.js`・`form.js` | URLのIDからメモを探して表示する・フォームに入れて更新する | この章で解説 |
| 6 | `list.js`・`detail.js` | ★でピン留め（通知を出す）、確認ダイアログを出してから削除 | 01_frontend/10_js_data 5節・01_frontend/09_js_ui 2・3節 |

各ステップを書き終えるたびにブラウザで確認しながら進めます。完成済みの部分（`common.js`全体、`form.js`の文字数カウンター・入力チェック・下書き保存・キャンセルの確認、`list.js`のカードの作成など）は、フロントエンド編の06〜08章で学んだ書き方を組み合わせたものなので、読んで仕組みを確認してください。

---

## ステップ1：データの保存と読み込み（storage.js）

`loadMemos()`・`saveMemos()`・`initMemos()`の3つを書きます。

| 関数 | 内容 |
|---|---|
| `loadMemos()` | `localStorage`から読み出してJSON → 配列にする。保存されていなければ`null` |
| `saveMemos(memos)` | 配列 → JSONにして`localStorage`に保存する |
| `initMemos()` | `async`関数。保存されていればそれを返し、無ければ`data/memos.json`を`fetch()`して保存してから返す。`response.ok`が`false`なら`throw`でエラーにする |

`initMemos()`は、「初めて開いたときだけ初期データを使い、2回目以降は保存したデータを使う」ための関数です。書き終えたら、`initMemos()`の最後にある仮の`return [];`の行は消します。

`storage.js`の後半（`resetMemos()`・`nextId()`・`getIdFromUrl()`・`saveSetting()`・`loadSetting()`）は完成済みです。`saveSetting()`・`loadSetting()`は、選んだカテゴリや下書きのような「保存できたら便利」な値のための関数で、`localStorage`が使えない環境でもページが止まらないよう`try`/`catch`で囲んでいます（01_frontend/10_js_data 4節）。

### 動作確認

| 確認する操作 | 確認したいこと |
|---|---|
| `challenge/`を開き、Applicationタブの Local storage を見る | `memo-app.memos`というキーに、5件のメモのJSONが保存されている（画面の一覧はまだ表示されなくてよい） |
| Consoleで`loadMemos().length`と打つ | `5`と表示される |

---

## ステップ2：一覧を表示する（list.js）

`render()`を書きます。カード1枚を作る`createCard(memo)`は完成済みです（01_frontend/10_js_data の練習問題4・サンプル04と同じく、`createElement`と`textContent`で要素を組み立てています）。作るカードの構造は、100_memo_apiの一覧ページと同じです。

```javascript
const render = () => {
    const visible = getVisibleMemos();   // ステップ3までは全件がそのまま返ってくる
    memoList.textContent = '';
    visible.forEach((memo) => memoList.append(createCard(memo)));
    observeFadeIn(memoList.querySelectorAll('.card'));   // common.js：ふわっと表示
    // 0件のときのメッセージ（#empty）、件数の表示（#list-count：「5件中 5件を表示」）
};
```

| 書くこと | ヒント |
|---|---|
| 0件のときのメッセージ | `emptyMessage.hidden`を、表示するメモがあれば`true`にする。メモが1件も無いときは「メモはまだありません。…」、絞り込みで0件になったときは「該当するメモはありません」 |
| 件数 | `listCount.textContent`に「全メモの件数件中 表示する件数件を表示」 |

### 動作確認

| 確認する操作 | 確認したいこと |
|---|---|
| `challenge/`を開く | 5件のカードが表示され、「5件中 5件を表示」と表示される |
| 1件目のカードを見る | ★・カテゴリのタグ・タイトル・本文・「期限：2026-10-07」・「編集」「削除」が表示されている |

---

## ステップ3：並び替え・絞り込み・検索（list.js）

### 並び替え：`sort()`

100_memo_apiの一覧と同じく、**ピン留めを先頭に、それ以外は新しい順**（`id`が大きい順）に並べます。

```javascript
const sortMemos = (list) => {
    return list.slice().sort((a, b) => {
        if (a.is_pinned !== b.is_pinned) {
            return a.is_pinned ? -1 : 1;
        }
        return b.id - a.id;
    });
};
```

| 書き方 | 説明 |
|---|---|
| `配列.sort((a, b) => 数値)` | 2つの要素`a`・`b`を比べる関数を渡して並べ替える。**マイナスを返すと`a`が前、プラスを返すと`b`が前** |
| `配列.slice()` | 配列のコピーを作る。`sort()`は元の配列そのものを並べ替えてしまうので、コピーしてから並べ替える |
| `b.id - a.id` | `b`の方が大きい（新しい）ときにプラスになるので、`b`が前になる |

### 絞り込みと検索：「状態」を持つ

選択中のカテゴリ（`selectedCategory`）と検索キーワード（`keyword`）を変数として持ち、`getVisibleMemos()`でその両方を満たすメモだけを残します（タイトルか本文にキーワードを含むもの）。ボタンや検索欄の操作では、**変数を書き換えて`render()`を呼ぶだけ**にします。01_frontend/08_js_render 3節の絞り込みのように、カードの`hidden`を直接付け外しはしません。

```javascript
keywordInput.addEventListener('input', () => {
    keyword = keywordInput.value.trim();   // 状態を変える
    render();                              // 状態から作り直す
});
```

こうすると、「絞り込み中に検索する」「検索中にピン留めする」など、操作が組み合わさっても、表示が常に状態と一致します。

| 書くこと | ヒント |
|---|---|
| `selectCategory(category)` | `selectedCategory`を変え、押されたボタンだけ`aria-pressed="true"`にする（01_frontend/08_js_render 練習問題3） |
| 絞り込みボタン | 親の`#filters`に1回だけ`click`を登録し、`event.target.closest('button')`で押されたボタンを探す。`selectCategory()`を呼び、`saveSetting(FILTER_KEY, カテゴリ)`で覚えておく |
| 開いたときの復元 | `start()`の最後で、`loadSetting(FILTER_KEY)`で読んだカテゴリのボタンがあれば（`` filters.querySelector(`button[data-category="${saved}"]`) ``）、そのカテゴリを選ぶ。無ければ`'all'` |

### 動作確認

| 確認する操作 | 確認したいこと |
|---|---|
| 一覧を見る | ★の付いた「買い物リスト」が先頭で、残りは新しい順（旅行の持ち物リスト → アプリのアイデア → 読書メモ → 企画会議メモ） |
| 「仕事」ボタンを押す | 「企画会議メモ」だけが残り、「5件中 1件を表示」になる |
| 「仕事」を選んだままリロードする | 「仕事」が選ばれた状態で開く |
| 「すべて」に戻して、検索欄に「リスト」と入力する | 「買い物リスト」「旅行の持ち物リスト」の2件になる |
| 検索欄に「リスト」が入ったまま「家事」ボタンを押す | 「買い物リスト」だけになる（絞り込みと検索の両方が効いている） |
| 検索欄に「あいうえお」と入力する | 「該当するメモはありません」と表示される |

---

## ステップ4：メモを追加する（form.js）

フォームの`submit`で、入力欄の値から新しいメモを作り、配列に追加して保存します。入力チェックの`validate()`・文字数カウンター・下書きの自動保存は完成済みです。

```javascript
const values = {
    title: titleInput.value.trim(),
    category: categoryInput.value,
    body: bodyInput.value.trim(),
    due_date: dueInput.value || null,   // 空欄（''）は falsy なので null になる
};

const savedId = nextId(memos);
memos.push({ id: savedId, is_pinned: false, ...values });
saveSetting(DRAFT_KEY, '');               // 保存したので下書きは空にする
saveMemos(memos);
location.href = `detail.html?id=${savedId}`;   // 保存したメモの詳細ページへ（100_memo_api と同じ）
```

| 書き方 | 説明 |
|---|---|
| `{ id: 1, ...values }` | **スプレッド構文**。`values`の全プロパティを、そのオブジェクトの中に展開してコピーする |
| `nextId(memos)` | 今ある最大のIDに1を足した番号（`storage.js`で完成済み）。削除したメモのIDを再利用しないので、IDが重複しない |
| `location.href = '…'` | JavaScriptからページを移動する |

ステップ5までは、追加と編集のどちらも、この追加の処理になります（`editingMemo`がまだ`null`のため）。

### 動作確認

| 確認する操作 | 確認したいこと |
|---|---|
| 「メモを追加」を開き、何も入力せずに「保存する」 | タイトルと本文の下にエラーが表示され、タイトル欄に移動する。ページは移動しない |
| タイトルを入力してから、別のページに移って「メモを追加」に戻る | 入力した内容が復元され、「…に保存した下書きを復元しました」と表示される（完成済みの下書き保存） |
| タイトル・本文を入力して「保存する」 | アドレスが`detail.html?id=6`に変わる（詳細ページはステップ5で作るので、今は「指定されたメモが見つかりません。」と表示されてよい） |
| 一覧に戻る | 追加したメモが★付きのメモの次（ピン留め以外の先頭）に表示される |
| Applicationタブで`memo-app.memos`を見る | 6件目として、`id`が`6`のメモが保存されている。`memo-draft`は空になっている |

---

## ステップ5：詳細ページと編集ページ（detail.js・form.js）

一覧のカードのリンクは`detail.html?id=3`、「編集」は`edit.html?id=3`のように、URLの`?`の後ろ（**クエリ文字列**）にメモのIDを付けています。詳細・編集ページでは、このIDを読み取って、どのメモを表示・編集するかを決めます。IDを読み取る`getIdFromUrl()`は、`storage.js`で完成済みです。

```javascript
// storage.js（完成済み）
const getIdFromUrl = () => {
    const params = new URLSearchParams(location.search);   // location.search は '?id=3'
    const id = params.get('id');                            // '3'（無ければ null）
    return id === null ? null : Number(id);                 // 文字列なので数値にする
};

// detail.js・form.js で、そのIDのメモを探す
memo = memos.find((m) => m.id === getIdFromUrl());
```

| 書き方 | 説明 |
|---|---|
| `location.search` | 今のURLのクエリ文字列（`'?id=3'`） |
| `new URLSearchParams(...)`・`.get('id')` | クエリ文字列から値を取り出す。値は**文字列**なので、`Number()`で数値にしてから`id`と比べる |
| `Object.assign(editingMemo, values)` | `values`のプロパティを、`editingMemo`にまとめて上書きする |

| 書くファイル | 書くこと |
|---|---|
| `detail.js`の`start()` | `getIdFromUrl()`のメモを`memos`から探して`memo`に入れる（無ければ、完成済みの処理が「指定されたメモが見つかりません。」を表示する） |
| `detail.js`の`showMemo()` | タイトル（`document.title`も「タイトル - メモ帳」に）・カテゴリ・本文・編集リンク（`edit.html?id=…`）を入れる。期限が無いメモは`#detail-meta`を隠し、あれば`<time>`の`dateTime`と文字を入れる。最後に`#detail-status`を空にして`#detail`を表示する |
| `form.js`の`start()` | 編集ページ（`editId`が`null`でない）では、そのメモを探して`editingMemo`に入れる |
| `form.js`の`fillForm()` | フォームの各欄に`memo`の値を入れる（`due_date`が`null`なら空欄：`memo.due_date ?? ''`） |
| `form.js`の`submit` | `editingMemo`があれば、新しく追加する代わりに`Object.assign()`で書き換え、そのメモの詳細ページへ移動する |

`find()`が返すのは、配列の中に入っているオブジェクト**そのもの**です。そのため、`editingMemo`を書き換えると`memos`配列の中のメモも書き換わり、そのまま`saveMemos(memos)`で保存できます。

クエリ文字列は、`08_request`でサーバー側から読み取る方法も学びます（`request.args.get('id')`）。100_memo_apiでは、`/memos/3`のようにURLのパスにIDを入れる形になります（`04_flask_basic`）。

### 動作確認

| 確認する操作 | 確認したいこと |
|---|---|
| 一覧で「読書メモ：銀河鉄道の夜」のタイトルを押す | アドレスが`detail.html?id=3`になり、内容が表示される。期限の行は無い。タブのタイトルが「読書メモ：銀河鉄道の夜 - メモ帳」 |
| 詳細ページで「編集」を押す | アドレスが`edit.html?id=3`になり、タイトル・カテゴリ・本文が入った状態で表示される。文字数も表示されている |
| タイトルを変えて「保存する」 | 詳細ページに戻り、タイトルが変わっている。一覧での位置は変わらない（`id`は変わらないため） |
| アドレスを`detail.html?id=999`・`edit.html?id=999`に書き換えて開く | 「指定されたメモが見つかりません。」と表示される |
| 編集ページで内容を変えてから「キャンセル」を押す | 確認ダイアログが出る。何も変えずに押すと、確認なしで一覧に戻る |

---

## ステップ6：ピン留めと削除（list.js・detail.js）

カードは`render()`のたびに作り直されるので、★ボタンや削除ボタンに直接イベントを登録しても、次の描画で消えてしまいます。01_frontend/10_js_data 5節と同じく、作り直されない親の`#memo-list`に1回だけイベントを登録し、`event.target`で何が押されたかを判定します。

```javascript
memoList.addEventListener('click', (event) => {
    const card = event.target.closest('.card');
    if (!card) {
        return;
    }
    const id = Number(card.dataset.id);
    const memo = memos.find((m) => m.id === id);

    if (event.target.classList.contains('pin-button')) {
        // is_pinned を反転 → 保存 → 描画 → showToast() で通知
    } else if (event.target.classList.contains('delete-button')) {
        openConfirm(`「${memo.title}」を削除しますか？`, () => {
            // filter() で取り除く → 保存 → 描画 → 通知
        });
    }
});
```

詳細ページの「削除」（`#detail-delete`）も、同じように`openConfirm()`で確認してから取り除き、保存して一覧（`index.html`）に移動します。

### 動作確認

| 確認する操作 | 確認したいこと |
|---|---|
| 「読書メモ」の☆を押す | ★に変わってピン留めのメモの中に移動し、右下に「ピン留めしました」が出て3秒で消える |
| もう一度★を押す | ☆に戻り、元の位置に戻る。「ピン留めを外しました」 |
| 「アプリのアイデア」の「削除」を押して「キャンセル」（またはEsc・背景のクリック） | 何も変わらない |
| もう一度「削除」を押して「OK」 | カードが消え、件数が減り、「メモを削除しました」が出る |
| 詳細ページで「削除」→「OK」 | 一覧に戻り、そのメモが無くなっている |
| リロードする | ピン留め・削除の結果が残っている |

---

## 完成したら：全体の動作確認

| 確認する操作 | 確認したいこと |
|---|---|
| 追加 → 詳細 → 編集 → 一覧 → ピン留め → 削除の流れを一通り行う | すべての操作が反映され、リロードしても残っている |
| ブラウザを完全に終了してから、もう一度開く | データが残っている |
| 「データを初期状態に戻す」→「OK」 | 最初の5件に戻る |
| ◐を押してからリロードする | 選んだ配色のまま開く |
| スマホ幅（375px）で全ページを操作する | ハンバーガーメニュー・カード・フォームが崩れずに使える |
| 全ページでConsoleを確認する | 赤字のエラーが出ていない |
| 100_memo_apiを起動して、同じ操作をしてみる | 見た目と操作がほぼ同じ（違いはログインがあることと、データがサーバーに保存されること） |
| `index.html`をファイルとして直接開く（`file://`） | 「メモを読み込めませんでした…」と表示される（初期データの`fetch()`にはサーバーが必要） |

### 発展課題

| 課題 | ヒント |
|---|---|
| 並び順を選べるようにする（新しい順・期限が近い順・タイトル順） | `<select>`の値を状態として持ち、`sortMemos()`で比較方法を切り替える（`sorters`のように、比べ方の関数をオブジェクトにまとめておくと切り替えやすい） |
| 期限が過ぎたメモ・近いメモを目立たせる | `'YYYY-MM-DD'`の形の文字列は、そのまま`<`で比べると日付の前後を比べられる |
| メモをJSONファイルとして書き出す | `JSON.stringify(memos, null, 2)`の内容を`<textarea>`に表示して、コピーできるようにする |

---

## このアプリの限界とバックエンド編

完成したメモアプリは、ブラウザの中だけで動いています。便利ですが、実際に使ってみると、次のような限界があります。

| 限界 | 理由 | バックエンド編で解決する章 |
|---|---|---|
| 別のパソコンやスマホから、同じメモを見られない | データが**このブラウザの`localStorage`の中だけ**にあるから | サーバーに保存する：`04_flask_basic`〜`14_flask_migrate`（Flaskでページを配信し、データベースに保存する） |
| ブラウザの閲覧データを消すと、メモも消える | 同上 | 同上 |
| 誰が書いたメモか区別できない。他の人と共有できない | ログインの仕組みが無いから | `15_login`（ログイン） |
| 入力チェックを無効にできてしまう | チェックがブラウザ側（JavaScript）だけだから | `09_forms`（サーバー側での入力チェック） |
| データの中身を誰でも書き換えられる | 開発者ツールで`localStorage`を直接編集できるから | サーバー側でデータを管理する：`13_flask_sqlalchemy`・`15_login` |
| 郵便番号から住所を調べるなど、外部のサービスを安全に使えない | APIの鍵などを、ブラウザに置くと誰でも見られるから | サーバーから外部APIを呼び出す（バックエンド編の範囲外） |
| 他のプログラム（スマホアプリなど）からメモを使えない | データがこのブラウザの中にしかないから | JSONを返すルートを作る：`08_request` |

この先のバックエンド編では、このメモアプリと同じデータの形のまま、**保存先をブラウザからサーバー（Flask＋データベース）に移していきます**。この章の`storage.js`が担当していた「データの保存・読み込み」を、サーバーが担当するようになるイメージです。最後の[100_memo_api](../100_memo_api/)で、この章と同じ画面のアプリが、サーバー版として完成します。

## 次のステップ

続きは [03_function](../03_function/) です。Pythonの関数から始めて、Flaskでサーバー側を作っていきます。
