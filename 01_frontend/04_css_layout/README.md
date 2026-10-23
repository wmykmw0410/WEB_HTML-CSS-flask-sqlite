# 04 ボックスモデルとレイアウト

> フロントエンド編 ／ 前の章：[03_css_basics](../03_css_basics/) ／ 次の章：[05_js_basics](../05_js_basics/)

この章のゴールは、**レイアウトを自力で組めるようになる**ことです。まず、すべてのレイアウトの土台になるボックスモデルとdisplayを学び、要素を1列に並べるFlexbox・格子状に並べるGrid・画面幅に合わせて切り替えるレスポンシブ対応、配色をまとめて管理するCSS変数、フォームの装飾の順に進みます。

章の最後の制作課題では、[02_html_semantic_form](../02_html_semantic_form/)で書いたオリジナルHPのHTMLに`style.css`を書いて、見た目を付けます。

> 開発者ツールの**Computed**パネル（ボックスモデルの図）と**デバイスツールバー**（画面幅の切り替え）、Elementsパネルの**Flex / Grid バッジ**をよく使います（[01_html_basicsの0節](../01_html_basics/#0-はじめに学習環境と開発者ツール)）。

## 目次

1. [ボックスモデルとdisplay](#1-ボックスモデルとdisplay)
2. [Flexbox](#2-flexbox)
3. [Grid](#3-grid)
4. [レスポンシブ対応](#4-レスポンシブ対応)
5. [CSS変数](#5-css変数)
6. [フォームの装飾](#6-フォームの装飾)
- [制作課題：オリジナルHP（ステップ2）](#制作課題オリジナルhpステップ2)
- [参考リンク](#参考リンク)

---

## フォルダ構成

```
01_frontend/04_css_layout/
├── README.md
├── example/                      サンプル（1つのサンプル＝1つのフォルダ）
│   ├── 01_box_model/             ボックスモデル・box-sizing・マージン相殺・display・overflow
│   │   └── index.html
│   ├── 02_flexbox/               Flexbox（主軸/交差軸・配置・折り返し・伸び縮み・実用パターン）
│   │   ├── index.html
│   │   └── img/sample.png
│   ├── 03_grid/                  Grid（fr・minmax・auto-fill/auto-fit・span・template-areas）
│   │   └── index.html
│   ├── 04_responsive/            レスポンシブ（viewport・モバイルファースト・clamp）
│   │   ├── index.html
│   │   └── img/sample.png
│   └── 05_variables/             CSS変数・ダークモード
│       └── index.html
├── question/                     練習問題（4問。問題文はREADMEの各節の最後）
│   ├── 01_box_model/             練習問題1：箱の大きさを計算し、レイアウトを直す
│   │   └── index.html
│   ├── 02_flexbox/               練習問題2：Flexboxでヘッダーとプロフィールカードを作る
│   │   ├── index.html
│   │   └── img/sample.png
│   ├── 03_grid_dashboard/        練習問題3：Gridでレスポンシブなダッシュボードを作る
│   │   └── index.html
│   ├── 04_form_style/            練習問題4：フォームを装飾する
│   │   └── index.html
│   └── answer/                   解答（問題と同じ名前のフォルダ。中のファイル構成も問題と同じ）
│       ├── 01_box_model/
│       ├── 02_flexbox/
│       ├── 03_grid_dashboard/
│       └── 04_form_style/
└── challenge/                         制作課題（オリジナルHP）ステップ2：HTMLは完成済み、css/style.css にTODOを書く
    └── answer/                        完成例
```

---

## 1. ボックスモデルとdisplay

> [example/01_box_model/index.html](example/01_box_model/index.html)

CSSでは、すべての要素が**箱（ボックス）**として扱われます。

```
┌─────────────── margin（外側の余白・背景色は付かない） ───────────────┐
│  ┌───────────── border（枠線） ─────────────────┐                     │
│  │  ┌───────── padding（内側の余白・背景色が付く） ─────────┐  │       │
│  │  │              content（中身：width / height）        │  │       │
│  │  └──────────────────────────────────────────────────┘  │       │
│  └────────────────────────────────────────────────────────┘       │
└──────────────────────────────────────────────────────────────────┘
```

### box-sizing: border-box

デフォルト（`content-box`）では`width`は**中身だけ**の幅で、実際の見た目は`padding`と`border`の分だけ広がります。

```css
.box {
    width: 200px;
    padding: 20px;
    border: 4px solid #3f6fd1;
    /* 見た目の幅 = 200 + 20×2 + 4×2 = 248px */
}
```

`box-sizing: border-box`にすると`width`に`padding`と`border`が含まれ、サイズ計算が直感的になります。実務では**CSSファイルの最初に次のリセットを書く**のが定番です。

```css
*, *::before, *::after {
    box-sizing: border-box;
}
```

`*`は「すべての要素」を選びます。`::before`・`::after`は、要素の中身の前後に内容を足す機能（疑似要素）ですが、ここでは「すべての要素と、その前後に足された内容」にもまとめて`box-sizing`を当てている、と読んでください。

### 省略記法

```css
padding: 16px;                 /* 4辺すべて */
padding: 8px 24px;             /* 上下 | 左右 */
padding: 4px 24px 16px;        /* 上 | 左右 | 下 */
padding: 4px 8px 16px 32px;    /* 上 | 右 | 下 | 左（時計回り） */
margin: 0 auto;                /* 上下0・左右自動 → 幅のあるブロック要素の中央寄せ */
```

### 覚えておきたい挙動

| 挙動 | 説明 |
|---|---|
| `margin: 0 auto` | `width`（または`max-width`）を持つブロック要素を左右中央に寄せる |
| `max-width` | 「これ以上広がらない」上限。`width`より柔軟で、狭い画面では自然に縮む |
| マージンの相殺 | 上下に隣接する`margin`は**足し算されず、大きい方だけ**になる（左右では起きない） |
| `overflow` | 中身がはみ出したときの扱い。`visible`（はみ出す）・`hidden`（切る）・`auto`（必要ならスクロール） |

### display

| 値 | 振る舞い |
|---|---|
| `block` | 横幅いっぱい・前後で改行。`width`/`height`/上下`margin`が効く |
| `inline` | 文章の中に並ぶ。`width`/`height`が**効かない** |
| `inline-block` | 横に並びつつ`width`/`height`も効く（ボタン・バッジ向き） |
| `none` | 表示しない（場所も取らない） |
| `flex` / `grid` | 子要素のレイアウト方式を切り替える（この章の2・3節） |

### 動作確認：箱の大きさを測る

| 確認する操作 | 確認したいこと |
|---|---|
| `01_box_model/index.html`を開き、2つの箱を見比べる | 同じ`width: 200px`なのに、上（`content-box`）の方が広い |
| 開発者ツールで上の箱を選び、Computedのボックス図を見る | 中身200・padding20・border4が図示され、要素にマウスを乗せると248px幅でハイライトされる |
| 「マージンの相殺」の2つの箱の間隔を開発者ツールで確認 | 間隔は50pxではなく30px |
| `.center`の`margin: 0 auto`を開発者ツールで無効化する | 中央にあった箱が左に寄る |


### 練習問題1：箱の大きさを計算し、レイアウトを直す

> 問題：[question/01_box_model/index.html](question/01_box_model/index.html) ｜ 解答：[question/answer/01_box_model/index.html](question/answer/01_box_model/index.html)

<details>
<summary>問題の内容を開く</summary>

**前半：予想する（A1〜A4）**

`01_box_model/index.html`の`<style>`の「前半」のルールを読んで、HTMLのA1〜A4の直前のコメント「予想：」の後ろに答えを書き込みます。書き終えたらブラウザで開き、開発者ツールのComputedのボックス図や、要素にマウスを乗せたときのサイズ表示で答え合わせをします。

| # | 予想すること |
|---|---|
| A1 | 見た目の幅（`border`の外側から外側まで）は何pxか |
| A2 | 見た目の幅は何pxか。そのとき中身（content）の幅は何pxか |
| A3 | 2つの箱の間隔は何pxか |
| A4 | 上・右・下・左の`padding`はそれぞれ何pxか |

後半のB1を書くとA1も`border-box`に変わってしまうので、前半の答え合わせはB1を書く**前に**行います。

**後半：書く（B1〜B6）**

`<style>`の「後半」の`TODO B1`〜`TODO B6`を埋めます。HTMLは変更しません。

| # | やること | 確認したいこと |
|---|---|---|
| B1 | すべての要素（`::before`・`::after`も含む）の`box-sizing`を`border-box`にする | `.card`の幅が600pxからはみ出さない |
| B2 | `.page`を最大幅600px・左右中央寄せ・左右の内側余白16pxにする | 広い画面で、ページが中央に置かれる |
| B3 | `.badge`を、横に並んだまま幅と高さが効くようにし、28px × 28pxにする | 「3」「12」のバッジが丸になる（`span`なので、そのままでは幅が効かない） |
| B4 | `.hidden-note`を表示しない（場所も取らない） | 「（このメモは非表示です）」が消え、その場所も詰まる |
| B5 | `.log`を高さ100pxにし、はみ出した中身は必要なときだけスクロールできるようにする | ログの欄の中でスクロールできる |
| B6 | `.card`の内側の余白を「上16px・左右24px・下32px」にする（1行の省略記法で） | Computedのボックス図で、`padding`が指定どおりになっている |

</details>

---

## 2. Flexbox

> [example/02_flexbox/index.html](example/02_flexbox/index.html)

Flexboxは、子要素を**1方向（横 または 縦）**に並べるレイアウト方式です。`display: flex`を付けた要素が**flexコンテナ**、その**直下の子**が**flexアイテム**になります。

```
flex-direction: row のとき
          主軸（main axis）→ justify-content で配置
     ┌──────────────────────────────────────┐
  交 │ ┌────┐ ┌────┐ ┌────┐                    │
  差 │ │ 1  │ │ 2  │ │ 3  │                    │
  軸 │ └────┘ └────┘ └────┘                    │
  ↓  └──────────────────────────────────────┘
  align-items で配置
```

```css
nav {
    display: flex;
    align-items: center;   /* 交差軸（縦）方向を中央揃え */
    gap: 16px;             /* アイテム同士の間隔 */
}

nav .push-right {
    margin-left: auto;     /* この要素以降を右端に押し出す */
}
```

### コンテナに指定するプロパティ

| プロパティ | 主な値 | 説明 |
|---|---|---|
| `flex-direction` | `row`（既定）/ `column` | 主軸の向き。`column`にすると縦に並び、主軸と交差軸が入れ替わる |
| `justify-content` | `flex-start` / `center` / `flex-end` / `space-between` / `space-around` | **主軸**方向の配置 |
| `align-items` | `stretch`（既定）/ `flex-start` / `center` / `flex-end` | **交差軸**方向の配置 |
| `flex-wrap` | `nowrap`（既定）/ `wrap` | 入りきらないときに折り返すか |
| `gap` | `16px`など | アイテム同士の間隔（外側には付かない） |

### アイテムに指定するプロパティ

| プロパティ | 説明 |
|---|---|
| `flex: 1` | 余った幅を分け合う（`flex: 2`の要素は`flex: 1`の2倍もらう） |
| `flex: 1 1 180px` | 「伸びる比率 縮む比率 基本の幅」。`flex-wrap: wrap`と組み合わせると「最小180pxで、入らなければ折り返す」列が作れる |
| `flex-shrink: 0` | 画面が狭くなっても縮ませない（アイコン画像など） |
| `margin-left: auto` | その要素の左の余白を最大まで取り、右端に寄せる |

### よく使う3パターン

| パターン | 書き方 |
|---|---|
| ナビゲーション（左にロゴ、右端にログイン） | `display: flex; align-items: center; gap` ＋ 右端の要素に`margin-left: auto` |
| 上下左右中央 | `display: flex; justify-content: center; align-items: center;` |
| 画像＋文章（メディアオブジェクト） | `display: flex; gap` ＋ 画像に`flex-shrink: 0` |

### 動作確認：主軸と交差軸

| 確認する操作 | 確認したいこと |
|---|---|
| `02_flexbox/index.html`を開く | 各`justify-content`・`align-items`の値で、アイテムの位置がどう変わるかが並んで表示される |
| 開発者ツールで`.container.row`の横に出る`flex`バッジをクリック | アイテムと隙間（`gap`）が図示される |
| 「4. flex-wrap」の`.wrap`の`flex-wrap`を無効化する | アイテムが折り返さずに縮んで1行に詰め込まれる |
| 「A. ナビゲーション」の`.push-right`の`margin-left: auto`を無効化する | 「ログイン」が右端から離れ、「新規作成」のすぐ右に来る |


### 練習問題2：Flexboxでヘッダーとプロフィールカードを作る

> 問題：[question/02_flexbox/index.html](question/02_flexbox/index.html) ｜ 解答：[question/answer/02_flexbox/index.html](question/answer/02_flexbox/index.html)

<details>
<summary>問題の内容を開く</summary>

`02_flexbox/index.html`のHTMLは完成しています。`<style>`の`TODO 1`〜`TODO 8`を埋めて、次の完成イメージにします。

```
(1) ヘッダー
    ┌──────────────────────────────────────────────────┐
    │ メモ帳   一覧  新規作成                 [ログイン] │
    └──────────────────────────────────────────────────┘
      ↑左寄せ                                   ↑右端

(2) プロフィールカード（上下左右中央に配置）
              ┌─────────────────────┐
              │ (画像)  山田 太郎     │
              │         メモ 42件     │
              │ [フォロー] [メッセージ]│ ← ボタンは横並びで同じ幅
              └─────────────────────┘

(3) フッター：3つの列を横に並べ、画面が狭いと折り返す
```

| # | 書く場所 | やること |
|---|---|---|
| 1 | `.site-header` | 子要素を横並びにし、縦方向は中央揃え、間隔は20px |
| 2 | `.login` | この要素だけを右端に寄せる（ヒント：`margin-left`） |
| 3 | `.stage` | 中の`.profile`を上下左右の中央に配置する |
| 4 | `.profile-top` | 画像と名前を横並びにし、縦方向は中央揃え、間隔は12px |
| 5 | `.actions` | ボタンを横並び、間隔8px |
| 6 | `.actions button` | 2つのボタンが余った幅を均等に分け合うようにする |
| 7 | `.site-footer` | 3つの列を横に並べ、画面が狭いときは折り返す。間隔は24px |
| 8 | `.site-footer section` | 各列は「最小180px・余ったら均等に伸びる」ようにする（ヒント：`flex: 1 1 180px`） |

| 確認する操作 | 確認したいこと |
|---|---|
| ブラウザで開く | 完成イメージのとおりに表示される |
| ウィンドウの幅を狭くする | フッターの列が折り返して、縦に並ぶ |
| 開発者ツールのElementsで`flex`バッジを押す | 並び方と隙間が図示される |

</details>

---

## 3. Grid

> [example/03_grid/index.html](example/03_grid/index.html)

Gridは、子要素を**行と列の2方向**で格子状に並べるレイアウト方式です。

```css
.card-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 16px;
}

.page {
    display: grid;
    grid-template-columns: 200px 1fr;
    grid-template-areas:
        "header header"
        "side   main"
        "footer footer";
}
.page header { grid-area: header; }
```

### ポイント

| 書き方 | 説明 |
|---|---|
| `grid-template-columns: 100px 200px 100px` | 3列をそれぞれの幅で |
| `1fr 2fr 1fr` | `fr`＝余った幅を比率で分ける単位 |
| `repeat(4, 1fr)` | 同じ指定を繰り返す（4等分） |
| `200px 1fr` | 固定幅のサイドバー＋残り全部 |
| `minmax(160px, 1fr)` | 最小160px・最大1fr |
| `repeat(auto-fill, minmax(160px, 1fr))` | 入るだけ列を作る。**メディアクエリなしで列数が自動で変わる** |
| `auto-fill` と `auto-fit` の違い | アイテムが少ないとき、`auto-fill`は空の列を残し、`auto-fit`は空の列を潰してアイテムを広げる |
| `grid-column: span 2` / `grid-row: span 2` | 横 / 縦に2マス分使う |
| `grid-column: 1 / -1` | 1本目の線から最後の線まで（横幅いっぱい） |
| `grid-template-areas` + `grid-area` | 領域に名前を付け、文字の「絵」でレイアウトを描く |
| `place-items: center` | 中身を上下左右中央に（Gridでの中央寄せ） |

### Flexbox と Grid の使い分け

| | Flexbox | Grid |
|---|---|---|
| 方向 | 1方向（行 **または** 列） | 2方向（行 **と** 列） |
| 得意なもの | ナビ・ボタンの並び・カードの中身 | カード一覧・ページ全体の骨組み |
| 考え方 | 中身の大きさに合わせて並べる | 先に枠（格子）を決めて、そこに配置する |

実際のページでは**両方を組み合わせる**のが普通です（ページの骨組みはGrid、ヘッダーの中はFlexbox）。

### 動作確認：列の自動調整

| 確認する操作 | 確認したいこと |
|---|---|
| `03_grid/index.html`を開き、ウィンドウ幅を変える | `auto-fill`・`auto-fit`の行で列数が自動で増減する |
| 広い画面で`auto-fill`と`auto-fit`を見比べる | `auto-fill`はアイテム2つが左に寄って空きが残り、`auto-fit`は2つが横幅いっぱいに広がる |
| 開発者ツールで`.page`の`grid`バッジをクリック | 領域名（header/side/main/footer）が図示される |
| ウィンドウ幅を600px以下にする | `.page`が縦1列（header→main→aside→footer）に組み替わる |

---

## 4. レスポンシブ対応

> [example/04_responsive/index.html](example/04_responsive/index.html)

画面の幅（スマホ・タブレット・PC）に応じてレイアウトを切り替えることを**レスポンシブ対応**と呼びます。

### `<meta name="viewport">`

```html
<meta name="viewport" content="width=device-width, initial-scale=1">
```

このタグが無いと、スマホのブラウザは「PC用のページだろう」と判断して、約980px幅で描画したものを縮小表示します。文字が極小になり、メディアクエリも意図通りに効きません。**すべてのページに必ず書きます**。

### メディアクエリとモバイルファースト

```css
/* まずスマホ用（1列）を書く */
.box-grid {
    display: grid;
    grid-template-columns: 1fr;
}

/* 600px「以上」になったら2列 */
@media (min-width: 600px) {
    .box-grid { grid-template-columns: repeat(2, 1fr); }
}

/* 900px「以上」になったら3列 */
@media (min-width: 900px) {
    .box-grid { grid-template-columns: repeat(3, 1fr); }
}
```

| 書き方 | 考え方 |
|---|---|
| **モバイルファースト**（`min-width`） | 小さい画面用を基本に書き、広い画面用を**足していく**。シンプルなレイアウトに要素を足す方が書きやすく、現在の主流 |
| デスクトップファースト（`max-width`） | PC用を基本に書き、狭い画面用で**打ち消していく** |

ブレークポイント（切り替わる幅）は「この幅でレイアウトが崩れ始めたら」で決めます。目安として600px前後（スマホ/タブレット）・900px前後（タブレット/PC）がよく使われます。

### メディアクエリ以外の道具

| 書き方 | 説明 |
|---|---|
| `max-width: 960px; margin: 0 auto; padding: 0 16px;` | 広い画面では中央に寄せ、狭い画面では左右に余白を残す「コンテナ」 |
| `img { max-width: 100%; height: auto; }` | 画像を親の幅からはみ出させない定番の指定 |
| `font-size: clamp(1.5rem, 4vw + 1rem, 2.75rem)` | 最小・推奨・最大を指定し、画面幅に応じてなめらかに変化させる |
| `repeat(auto-fill, minmax(200px, 1fr))` | 2節の自動列数。メディアクエリなしでレスポンシブになる |

### 動作確認：ブレークポイント

| 確認する操作 | 確認したいこと |
|---|---|
| `04_responsive/index.html`を開き、デバイスツールバー（`Cmd + Shift + M`）で幅を375px→700px→1000pxと変える | 黄色の表示が「スマホ幅：1列」→「タブレット幅：2列」→「PC幅：3列」に変わり、箱の列数も変わる |
| 同じ操作でナビゲーションを見る | スマホ幅では縦並び、600px以上で横並びになる |
| 見出しの大きさを見ながら幅を変える | 段階的ではなく、なめらかに大きさが変わる（`clamp`） |
| 一番下の画像を見る | `width="1200"`なのに画面からはみ出さない |
| `<meta name="viewport">`をコメントアウトし、デバイスツールバーのスマホ幅で確認（確認後は必ず戻す） | ページ全体が縮小表示され、3列のまま小さく表示される |


### 練習問題3：Gridでレスポンシブなダッシュボードを作る

> 問題：[question/03_grid_dashboard/index.html](question/03_grid_dashboard/index.html) ｜ 解答：[question/answer/03_grid_dashboard/index.html](question/answer/03_grid_dashboard/index.html)

<details>
<summary>問題の内容を開く</summary>

2節（Grid）と4節（レスポンシブ）を組み合わせる問題です。`03_grid_dashboard/index.html`のHTMLは完成しています。「モバイルファースト」で、まずスマホ用を書き、`@media (min-width)`で広い画面用を追加します。

```
スマホ（〜767px）         PC（768px〜）
┌──────────┐              ┌──────────────────────────────┐
│  header  │              │            header            │
├──────────┤              ├────────┬─────────────────────┤
│  stats   │              │        │        stats        │
├──────────┤              │  side  ├─────────────────────┤
│  memos   │              │        │        memos        │
├──────────┤              ├────────┴─────────────────────┤
│  side    │              │            footer            │
├──────────┤              └──────────────────────────────┘
│  footer  │                 side の幅は 220px 固定
└──────────┘
```

| # | 書く場所 | やること |
|---|---|---|
| 1 | `.layout` | `display: grid`にし、`grid-template-areas`でスマホ用の5段を定義する |
| 2 | `.layout`の下 | 各要素に`grid-area`で名前を付ける（`header` / `stats` / `memos` / `side` / `footer`） |
| 3 | `.stats` | `display: grid`で2列（`repeat(2, 1fr)`）、間隔12px |
| 4 | `.memo-list` | `auto-fill`＋`minmax(180px, 1fr)`で自動的に列数が変わるグリッドにする。間隔12px |
| 5 | 「PC用（768px以上）」 | `@media (min-width: 768px)`を書き、`.layout`の列を「`220px 1fr`」にして`grid-template-areas`をPC用に変える。`.stats`は4列にする |

| 確認する操作 | 確認したいこと |
|---|---|
| デバイスツールバーで幅375pxにする | 5つの領域が縦に1列で並び、数値カードは2列 |
| 幅を1000pxにする | `side`が左に220pxで並び、数値カードは4列 |
| 幅を少しずつ変える | メモのカードの列数が、メディアクエリ無しで自動的に変わる |

</details>

---

## 5. CSS変数

> [example/05_variables/index.html](example/05_variables/index.html)

### CSS変数（カスタムプロパティ）

```css
:root {
    --color-primary: #3f6fd1;
    --radius: 8px;
}

.button {
    background: var(--color-primary);
    border-radius: var(--radius);
}
```

| 書き方 | 説明 |
|---|---|
| `--名前: 値;` | 変数の定義。`:root`（＝`html`要素）に書くとページ全体で使える |
| `var(--名前)` | 変数の値を使う。`var(--名前, 代わりの値)`で未定義のときの値も指定できる |
| 要素ごとの上書き | `.card.accent { --color-primary: #d1723f; }`のように書くと、その要素の中だけ値が変わる |

色をあちこちに直接書くと、配色を変えるときに全部探して直す必要があります。変数にまとめておけば**1か所の変更で済み**、ダークモードも変数の差し替えだけで作れます。

```css
@media (prefers-color-scheme: dark) {
    :root {
        --color-bg: #16181d;
        --color-text: #e6e8ec;
    }
}
```

### 動作確認

| 確認する操作 | 確認したいこと |
|---|---|
| `05_variables/index.html`を開く | カードとボタンが、定義した変数の色・角丸・余白で表示される |
| 開発者ツールで`:root`の`--color-primary`を`green`に書き換える | 全部のボタンの色が一度に変わる（ただし`.accent`の中は上書きしているので変わらない） |
| OSの外観をダークモードにする（またはDevToolsのRendering → Emulate CSS media feature `prefers-color-scheme: dark`） | 背景・文字・カードの色が暗い配色に切り替わる |

---

## 6. フォームの装飾

入力欄をクリックしたとき・不正な値を入れたときの見た目を付けます。そのために、属性や状態で要素を選ぶセレクタを使います。

### フォームの装飾で使うセレクタ

次の練習問題4と、制作課題で使うセレクタです。基本のセレクタ（[03_css_basicsの3・4節](../03_css_basics/#3-基本のセレクタ)）に、属性や状態で選ぶ書き方を足します。

| 記法 | 対象 |
|---|---|
| `input[type="text"]` | 属性セレクタ。`type`が`text`の`input`だけ（`[属性名="値"]`の形で、属性の値で選ぶ） |
| `:focus` | フォーカスされている要素（入力欄をクリックしたときなど） |
| `:focus-visible` | **キーボード操作で**フォーカスされている要素（Tabキーで移動したとき）。マウスでクリックしたときは当たらない |
| `:user-invalid` | ユーザーが入力を操作した後に、値が不正な入力欄。ページを開いた直後は当たらない（`:invalid`は開いた直後から当たる） |

```css
input[type="email"]    { border: 1px solid #c8ced8; }  /* 属性セレクタ */
input:focus            { border-color: #3f6fd1; }      /* フォーカス中 */
a:focus-visible        { outline: 3px solid #d1723f; } /* キーボードでフォーカス中 */
input:user-invalid     { border-color: #d1495b; }      /* 操作したあとに不正 */
```

### 練習問題4：フォームを装飾する

> 問題：[question/04_form_style/index.html](question/04_form_style/index.html) ｜ 解答：[question/answer/04_form_style/index.html](question/answer/04_form_style/index.html)

<details>
<summary>問題の内容を開く</summary>

[02_html_semantic_formの練習問題2](../02_html_semantic_form/#練習問題2ユーザー登録フォームのhtmlを書く)と同じ項目のユーザー登録フォームのHTMLが入っています（スタイルを当てやすいように、03_css_basicsで学んだ`class`・`id`が付いています）。`<style>`の`TODO 1`〜`TODO 5`を埋めて、`02_backend/15_login`の「ユーザー登録」画面として使える見た目にします。白いカードの中に、横幅いっぱいの入力欄がラベルの下に並び、登録ボタンは横幅いっぱいの青いボタンにします。

| # | やること |
|---|---|
| 1 | `.field`の中の`label`をブロック要素にし、太字・下に4pxの余白 |
| 2 | `type`が`text` / `email` / `password`の`input`を、横幅いっぱい・`padding` 8px・枠線`1px solid var(--color-border)`・角丸6pxにする（属性セレクタを使う） |
| 3 | 入力欄にフォーカスしたとき（`:focus`）、枠線の色を`var(--color-primary)`にし、`outline`を消して`box-shadow: 0 0 0 3px rgb(63 111 209 / 0.25)`を付ける |
| 4 | ユーザーが操作した後に不正な値だったとき（`:user-invalid`）、枠線の色を`var(--color-error)`にする（`:invalid`だとページを開いた瞬間から赤くなってしまう。違いを試してみる） |
| 5 | 登録ボタンを横幅いっぱい・背景`var(--color-primary)`・白文字・枠線なし・`padding` 10px・角丸6px・`cursor: pointer`にし、`:hover`で`opacity: 0.85`にする |

| 確認する操作 | 確認したいこと |
|---|---|
| `Tab`キーで入力欄を移動する | フォーカス中の入力欄の枠が青くなり、外側に薄い青の輪が出る |
| パスワードを3文字で入力して、欄の外をクリックする | 枠が赤くなる |
| ページを開いた直後に見る | まだ何も入力していないので、どの枠も赤くない |
| 開発者ツールで`:root`の`--color-primary`を`green`に変える | フォーカスの枠とボタンの色が一度に変わる |

</details>

---

## 制作課題：オリジナルHP（ステップ2）

> [challenge/](challenge/) — 雛形 ｜ [challenge/answer/](challenge/answer/) — 完成例 ｜ 自分のHP：[00_my_homepage/](../00_my_homepage/)

ステップ1で書いたHPのHTMLに、`css/style.css`を作って見た目を付けます。**HTMLはなるべく変えずにCSSで見た目を作る**のが基本です（クラスを追加するのは構いません）。

制作課題は、毎回次の2段階で進めます。

1. **`challenge/`で練習する**：架空の人物「山田 太郎」のサイトを題材に、ファイルの中のTODOコメントに沿って書きます。書けたら`challenge/answer/`の完成例と見比べます。
2. **自分のHPに反映する**：同じことを、[00_my_homepage/](../00_my_homepage/)の自分のサイトに行います。こちらは文章・配色・レイアウトを自分で考えて作ります。下の「必須要件」は、自分のHPで満たすべき要件です。

### challenge/ の内容

| ファイル | 内容 |
|---|---|
| `*.html` | 02_html_semantic_formの完成例に、`<link rel="stylesheet" href="css/style.css">`を足したもの（完成済み） |
| `css/style.css` | TODOコメントだけが、上から節の順に並んでいる。ここに書き込んでいく |

### 必須要件

| 要件 | 使う節 |
|---|---|
| 全ページで同じ`css/style.css`を`<link>`で読み込む（`<style>`タグや`style`属性は使わない） | 03_css_basics 1 |
| `:root`にCSS変数で配色を定義し、色は変数を通して使う（メインカラー・背景・文字・枠線の4色以上） | 5 |
| `*, *::before, *::after { box-sizing: border-box; }`のリセットを書く | 1 |
| ヘッダーのサイト名とナビゲーションを**Flexbox**で横に並べる | 2 |
| カードなどの一覧を**Grid**で並べる（制作実績・スキルなど） | 3 |
| **モバイルファースト**で書き、`@media (min-width: ...)`で広い画面のレイアウトを足す。幅375px・768px・1100pxのどれでも横スクロールが出ない | 4 |
| リンクとボタンに`:hover`と`:focus-visible`のスタイルを付ける（[フォームの装飾で使うセレクタ](#フォームの装飾で使うセレクタ)） | 03_css_basics 3、この章の6 |
| フォームの入力欄を横幅いっぱいにし、`:focus`で枠の色を変える | 6 |
| 開発者ツールで、意図しないルールが**取り消し線**で負けていないか確認する | 03_css_basics 補足 |

### 進め方のヒント

1. 配色を3〜5色決めて、`:root`に変数として書く（配色に迷ったら、メインカラー1色＋白・グレー系で十分）
2. 全ページ共通の部分（`body`・ヘッダー・フッター・`.container`）から書き、1ページずつ仕上げる
3. デバイスツールバーで、こまめにスマホ幅を確認する。崩れたら、その幅で「どの要素がはみ出しているか」をElementsで探す
4. [challenge/answer/css/style.css](challenge/answer/css/style.css)は、どの部分にどの節の内容を使っているかの参考にする

### 動作確認：challenge/

| 確認する操作 | 確認したいこと |
|---|---|
| `challenge/index.html`を開く | `challenge/answer/index.html`とほぼ同じ見た目になっている（色や余白は違っていてよい） |
| デバイスツールバーで375px・768px・1100pxに切り替える | どの幅でも横スクロールが出ない。768px以上でホームのプロフィール欄が2列になる |
| 4ページを行き来する | 1つの`style.css`で、全ページの見た目がそろっている |

---

## 参考リンク

| リンク | 内容 |
|---|---|
| [MDN：CSS リファレンス](https://developer.mozilla.org/ja/docs/Web/CSS/Reference) | すべてのCSSプロパティの説明 |
| [MDN：CSS レイアウト入門](https://developer.mozilla.org/ja/docs/Learn/CSS/CSS_layout) | Flexbox・Grid・レスポンシブをさらに詳しく |
| [Flexbox Froggy](https://flexboxfroggy.com/#ja) / [Grid Garden](https://cssgridgarden.com/#ja) | カエルや畑を動かしながら Flexbox / Grid を練習できるゲーム |
| [Can I use](https://caniuse.com/) | そのCSS機能がどのブラウザで使えるか |

## 次のステップ

続きは [05_js_basics](../05_js_basics/) です。ページに動きを付けるJavaScriptの基本文法を学びます。
