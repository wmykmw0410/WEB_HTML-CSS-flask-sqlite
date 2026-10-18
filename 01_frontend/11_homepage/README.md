# 09 オリジナルHPを仕上げる

> フロントエンド編 ／ 前の章：[10_js_data](../10_js_data/) ／ 次の章：[02_backend/01_intro](../../02_backend/01_intro/)（バックエンド編）

01_html_basics〜10_js_data の制作課題で少しずつ作ってきたオリジナルHP（[00_my_homepage/](../00_my_homepage/)）を完成させる章です。新しい文法はほとんど出てきません。代わりに、「人に見せられる品質」に仕上げるための確認と、細かい作り込みを行います。

最後に、補足として、作ったHPをインターネットに公開する方法を紹介します。

## 目次

1. [ファビコンとOGP](#1-ファビコンとogp) — ブラウザのタブやSNSでの見え方
2. [画像の扱い](#2-画像の扱い) — サイズ・形式・読み込みの工夫
3. [品質チェック](#3-品質チェック) — Validator・Lighthouse・実機での確認
4. [最終チェックリスト](#4-最終チェックリスト)
- [制作課題：オリジナルHP（ステップ5）](#制作課題オリジナルhpステップ5)
- [完成版の作例：フロントエンド編の機能をすべて盛り込んだHP](#完成版の作例フロントエンド編の機能をすべて盛り込んだhp)
- [補足：GitHub Pagesで公開する](#補足github-pagesで公開する)

---

## フォルダ構成

```
01_frontend/11_homepage/
├── README.md
├── challenge/             制作課題（オリジナルHP）ステップ5：10_js_dataの完成例 ＋ ファビコン・OGPのTODO
│   ├── index.html / about.html / works.html / contact.html   <head>にTODOあり
│   ├── css/style.css / js/script.js / data/works.json        完成済み
│   ├── img/avatar.png                                        （favicon.svg は自分で作る）
│   └── answer/            完成例（img/favicon.svg とOGPを追加したもの）
└── sample/                完成版の作例：フロントエンド編の機能をすべて盛り込んだHP
    ├── index.html / about.html / works.html / contact.html
    ├── css/style.css
    ├── js/common.js / home.js / about.js / works.js / contact.js
    ├── data/works.json    作品のデータ（詳しい説明・工夫した点を追加）
    └── img/
```

`fetch()`を使うので、`python -m http.server`で起動して確認してください。

```bash
cd 01_frontend/11_homepage
python -m http.server 8000
# → http://localhost:8000/challenge/ （完成例は http://localhost:8000/challenge/answer/）
```

---

## 1. ファビコンとOGP

### ファビコン

**ファビコン**は、ブラウザのタブやブックマークに表示される小さなアイコンです。

```html
<link rel="icon" href="img/favicon.svg" type="image/svg+xml">
```

SVG形式なら、テキストエディタで書けて、どの大きさでもきれいに表示されます。完成例の[img/favicon.svg](challenge/answer/img/favicon.svg)は、角丸の四角形に頭文字を1文字置いただけのものです。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
  <rect width="64" height="64" rx="14" fill="#2f7d6d"/>
  <text x="32" y="44" font-size="34" font-family="sans-serif" font-weight="bold" fill="#ffffff" text-anchor="middle">T</text>
</svg>
```

### OGP

**OGP**（Open Graph Protocol）は、URLがSNSやチャットで共有されたときに表示されるタイトル・説明・画像を指定する`meta`タグです。

```html
<meta property="og:type" content="website">
<meta property="og:title" content="ホーム | 山田 太郎">
<meta property="og:description" content="Web開発を学習中の山田太郎のポートフォリオサイトです。">
<meta property="og:image" content="https://（公開したURL）/img/avatar.png">
```

| プロパティ | 内容 |
|---|---|
| `og:title` | 共有されたときのタイトル（`<title>`と同じでよい） |
| `og:description` | 説明文（`<meta name="description">`と同じでよい） |
| `og:image` | 表示される画像。本来は`https://`から始まる**完全なURL**で書く必要があるので、公開後に書き換える |

---

## 2. 画像の扱い

| 項目 | やること | 理由 |
|---|---|---|
| ファイルサイズ | 1枚あたり数百KB以下にする。スマホで撮った写真（数MB）はそのまま使わず、縮小してから使う | 大きい画像は表示が遅くなり、スマホの通信量も増える |
| 表示サイズに合わせる | 横幅300pxで表示する画像なら、600px程度（高解像度の画面向けに2倍）に縮小しておく | 表示より極端に大きい画像は無駄になる |
| 形式 | 写真は`.jpg`か`.webp`、イラストや図は`.png`か`.svg` | 形式によって得意な画像が違う |
| `width`・`height`属性 | 実際の縦横比に合う値を書く | 読み込み中に場所を確保して、レイアウトのガタつきを防ぐ（01_html_basics 2節） |
| `alt` | 内容を説明する。装飾だけの画像は`alt=""` | 02_html_semantic_form 1節 |
| `loading="lazy"` | ページの下の方にある画像に付ける | 画面に近づくまで読み込みを遅らせ、最初の表示を速くする |

```html
<img src="img/work-memo.webp" alt="メモ帳アプリの一覧画面" width="600" height="400" loading="lazy">
```

画像の縮小は、Macなら「プレビュー」の「ツール → サイズを調整」、Windowsなら「フォト」の「サイズ変更」でできます。

---

## 3. 品質チェック

### HTMLの文法

[W3C Markup Validation Service](https://validator.w3.org/#validate_by_input)に各ページのHTMLを貼り付け、エラーが0件になることを確認します（01_html_basics 0節）。

### Lighthouse

**Lighthouse**は、Chromeの開発者ツールに組み込まれている、ページの品質を点数で採点する機能です。

1. 確認したいページを開き、開発者ツールの**Lighthouse**タブを開く
2. Mode は「Navigation」、Device は「Mobile」を選ぶ
3. 「Analyze page load」を押す

| カテゴリ | 何を見ているか | よくある指摘 |
|---|---|---|
| Performance | 表示の速さ | 画像が大きすぎる（2節） |
| Accessibility | 誰でも使えるか | `alt`が無い・文字と背景のコントラストが低い・`label`が無い |
| Best Practices | 安全で一般的な作り方か | Consoleにエラーが出ている |
| SEO | 検索エンジンに伝わるか | `<title>`がどのページも同じ・リンクの文字が「こちら」 |

指摘の項目をクリックすると、どの要素が原因かが表示されます。すべてのカテゴリで**90点以上**を目標にしましょう。

### いろいろな環境で見る

| 確認 | やり方 |
|---|---|
| 画面幅 | デバイスツールバーで375px・768px・1100pxを見る。横スクロールが出ないこと |
| 別のブラウザ | Chrome以外（Safari・Edge・Firefoxなど）でも開いてみる |
| キーボードだけで操作 | `Tab`キーだけで全リンク・ボタン・入力欄に移動でき、フォーカス位置が見えること |
| スマホの実機 | パソコンとスマホを同じWi-Fiにつなぎ、`python -m http.server 8000 --bind 0.0.0.0`で起動して、スマホのブラウザで`http://（パソコンのIPアドレス）:8000`を開く（IPアドレスの調べ方は[00_docs/web_basic](../../00_docs/web_basic/#9-ipアドレス)を参照） |

---

## 4. 最終チェックリスト

[00_my_homepage/](../00_my_homepage/)のサイトについて、次をすべて満たしたら完成です。

**内容**

- [ ] 4ページ以上あり、各ページの目的（何を伝えるページか）がはっきりしている
- [ ] 知られて困る個人情報を載せていない（[00_my_homepage/README.md](../00_my_homepage/)の注意を再確認）
- [ ] 誤字脱字が無い。リンク切れが無い

**HTML（01_html_basics）**

- [ ] 全ページに`<title>`・`lang="ja"`・`viewport`がある
- [ ] セマンティックタグで構造を表し、見出しレベルを飛ばしていない
- [ ] W3C Validatorのエラーが0件

**CSS（03_css_basics）**

- [ ] 1つの`style.css`を全ページで共有し、配色はCSS変数で管理している
- [ ] 375px・768px・1100pxで崩れない
- [ ] `:hover`と`:focus-visible`のスタイルがある

**JavaScript（05_js_basics〜10_js_data）**

- [ ] ハンバーガーメニュー・一覧の絞り込み・お問い合わせの入力チェックが動く
- [ ] 一覧はJSONから作られ、読み込みに失敗したときのメッセージがある
- [ ] どのページを操作してもConsoleにエラーが出ない

**仕上げ（この章）**

- [ ] ファビコンとOGPを設定した
- [ ] 画像のサイズを小さくし、`width`・`height`・`alt`を付けた
- [ ] Lighthouseの4カテゴリがすべて90点以上

---

## 制作課題：オリジナルHP（ステップ5）

> [challenge/](challenge/) — 雛形 ｜ [challenge/answer/](challenge/answer/) — 完成例 ｜ 自分のHP：[00_my_homepage/](../00_my_homepage/)

これまでと同じく、まず`challenge/`で練習し、次に自分のHPに反映します。

### challenge/ の内容

| ファイル | 内容 |
|---|---|
| `*.html` | 10_js_dataの完成例。各ページの`<head>`に、ファビコンとOGPのTODOコメントがある |
| `img/` | `avatar.png`だけがある。`favicon.svg`は1節を参考に自分で作る |
| `css/`・`js/`・`data/` | 完成済み |

### やること

1. `img/favicon.svg`を作り、全ページの`<head>`で読み込む（1節）
2. 全ページにOGPの`meta`を書く（1節）
3. 自分のHPで、2節の画像の扱いと3節の品質チェックを行う
4. 4節の最終チェックリストをすべて満たしたら、オリジナルHPの完成

### 動作確認：challenge/

| 確認する操作 | 確認したいこと |
|---|---|
| `python -m http.server`で起動して`challenge/`を開く | ブラウザのタブに、自分で作ったファビコンが表示される |
| 開発者ツールのElementsで`<head>`を開く | 4ページすべてに`og:title`などのOGPの`meta`がある |
| `challenge/answer/`と見比べる | 同じ種類のタグが`<head>`に入っている |

---

## 完成版の作例：フロントエンド編の機能をすべて盛り込んだHP

> [sample/](sample/)

制作課題の完成例（`challenge/answer/`）は、各ステップの必須要件だけを満たした最小限のサイトです。[sample/](sample/)は、それに06_js_events・07_js_dom・08_js_render・09_js_ui・10_js_dataで学んだ機能を**すべて**盛り込んだ完成版の作例です。自分のHPに機能を足すときの見本にしてください。

```bash
cd 01_frontend/11_homepage/sample
python -m http.server 8000
# → http://localhost:8000/
```

### 盛り込んだ機能

| 機能 | ページ | ファイル | 学んだ章・節 |
|---|---|---|---|
| 表示設定（ライト・ダーク・OSに合わせる）のポップアップ。選んだ設定は`localStorage`に保存 | 全ページ（ヘッダーの⚙） | `js/common.js` | 09_js_ui 2節・10_js_data 4節・04_css_layout 5節 |
| ハンバーガーメニュー | 全ページ | `js/common.js` | 06_js_events 1・3節 |
| ツールチップ（ホバーとフォーカス） | 全ページ（⚙）・プロフィール（技術名） | `js/common.js` | 06_js_events 3節 |
| ヘッダーの影・読んだ量のバー・トップへ戻るボタン・なめらかなスクロール | 全ページ | `js/common.js`・CSS | 09_js_ui 5節 |
| スクロールしたらふわっと表示（`IntersectionObserver`） | 全ページ | `js/common.js` | 09_js_ui 5節 |
| 作品のスライドショー（`works.json`から作る。自動再生・ホバー中は停止） | ホーム | `js/home.js` | 09_js_ui 4節・10_js_data 2節 |
| 基本情報・スキル・経歴のタブ切り替え（← → キー対応） | プロフィール | `js/about.js` | 09_js_ui 1節 |
| `works.json`からカードを作る・技術での絞り込み | 制作実績 | `js/works.js` | 10_js_data 2・3・5節・08_js_render 3節 |
| 作品の詳細を出すモーダルウィンドウ（開いている間は後ろをスクロールさせない） | 制作実績 | `js/works.js` | 09_js_ui 3節 |
| 文字数カウンター・入力チェック・送信後に自動で消える通知 | お問い合わせ | `js/contact.js` | 06_js_events 2・3節・09_js_ui 2節 |
| ファビコン・OGP | 全ページ | `<head>` | この章の1節 |
| 動きを減らす設定のときは、自動再生・ふわっと表示・なめらかなスクロールをやめる | 全ページ | CSS・`js/home.js` | 04_css_layout 5節 |

### ファイルの分け方

JavaScriptは、全ページ共通の動きを`common.js`に、ページごとの動きを`home.js`・`about.js`・`works.js`・`contact.js`に分けています。各ページは`common.js`と自分のページのファイルの2つを読み込みます。1つのファイルに全部を書くより、どこに何があるかがわかりやすく、そのページで使わない処理も読み込まずに済みます（バックエンド編の`02_memo_app_frontend`でも、同じように役割でファイルを分けます）。

`css/style.css`は、前半が制作課題ステップ5の完成例と同じで、後半に追加した機能のスタイルを、機能ごとにコメントで区切って書いています。

### 動作確認

| 確認する操作 | 確認したいこと |
|---|---|
| ヘッダーの⚙を押して「ダーク」を選び、別のページに移動する・再読み込みする | 暗い配色のまま表示される（`localStorage`に保存されている） |
| ホームで待つ・スライドにマウスを乗せる | 5秒ごとに作品が切り替わる。マウスを乗せている間は止まる |
| プロフィールで「スキル」タブを開き、技術名にマウスを乗せる | タブが切り替わり、技術名の下に説明が表示される |
| 制作実績で「Python」を押してから、カードを押す | 2件に絞り込まれ、カードを押すと詳細のモーダルが開く。開いている間は後ろがスクロールしない |
| お問い合わせで何も入力せずに送信し、次に正しく入力して送信する | 最初はエラーが表示されて名前の欄に移動し、正しく送ると右下に通知が出て3秒で消える |
| どのページでも下までスクロールする | ヘッダーに影が付き、青緑のバーが伸び、カードがふわっと表示され、右下に「↑」が出る |
| 幅375pxで全ページを見る | ☰でメニューが開閉し、どのページも横にはみ出さない |

---

## 補足：GitHub Pagesで公開する

ここまでで、HPはパソコンの中で完成しています。**GitHub Pages**を使うと、HTML・CSS・JavaScriptだけでできたサイト（静的サイト）を、無料でインターネットに公開できます。公開は必須ではありません。公開したい人だけ、次の注意を読んでから進めてください。

### 公開する前の注意

- 公開したページは**世界中の誰でも**見られます。もう一度、個人情報が載っていないか確認する
- **GitHubのリポジトリ（ソースコード）も公開されます**。HPのファイル以外（メモや下書き、パスワードなど）を同じリポジトリに入れない
- お問い合わせフォームは、静的サイトなので**実際には送信されません**。本当に問い合わせを受け付けたい場合は、Googleフォームなどの外部サービスへのリンクに置き換える
- 公開後に削除しても、検索エンジンや他人の保存によって残る可能性がある

### 手順

GitやGitHubの基本操作は[00_docs/github](../../00_docs/github/)にまとめてあります。初めての人は先に読んでください。

1. GitHubで**新しいリポジトリ**を作る。名前は`my-homepage`など自由。**Public**を選ぶ（無料プランのGitHub PagesはPublicリポジトリのみ）
2. [00_my_homepage/](../00_my_homepage/)を**カリキュラムのフォルダの外にコピー**し、その中身だけをリポジトリにpushする。このカリキュラムのフォルダ自体がgitで管理されている場合、その中で`git init`すると「リポジトリの中のリポジトリ」になって混乱するため、別の場所に分ける。`index.html`がリポジトリの一番上の階層に来るようにする

    ```bash
    cp -r 01_frontend/00_my_homepage ~/my-homepage   # カリキュラムの外（ホームフォルダ）にコピー
    cd ~/my-homepage
    rm README.md                               # このフォルダの説明用READMEは公開しなくてよい
    git init
    git add .
    git commit -m "Initial commit"
    git branch -M main
    git remote add origin https://github.com/（ユーザー名）/my-homepage.git
    git push -u origin main
    ```

3. GitHubのリポジトリのページで **Settings → Pages** を開く
4. 「Build and deployment」の Source で **Deploy from a branch** を選び、Branch を **main**・フォルダを **/ (root)** にして **Save** を押す
5. 1〜2分待ってページを再読み込みすると、`https://（ユーザー名）.github.io/my-homepage/`というURLが表示される。これが公開されたHPのアドレス

公開後に内容を変更したいときは、コピー先（`~/my-homepage`）のファイルを編集して`git add`・`git commit`・`git push`すれば、数分で反映されます。公開後はコピー先の方を正本として育てていきましょう。

### 公開後に確認すること

| 確認 | 理由 |
|---|---|
| 全ページが表示され、リンクで移動できる | ファイル名の大文字・小文字の違いは、パソコンでは動いても公開先では動かないことがある（`About.html`と`about.html`は別物） |
| 制作実績が表示される | GitHub Pagesは`https://`のWebサーバーなので、`fetch()`も動く |
| OGPの`og:image`を完全なURLに書き換える | `https://（ユーザー名）.github.io/my-homepage/img/avatar.png`のように書き換えて、もう一度pushする |
| スマホで開いてみる | 自分のスマホから、公開したURLにアクセスできる |

## 次のステップ

これでフロントエンド編は終わりです。続きは、バックエンド編のイントロダクション [02_backend/01_intro](../../02_backend/01_intro/) です。コードを貼り付けながら、FlaskとSQLiteで動くメモ帳を1時間で作り、サーバー側の全体像をつかみます。
