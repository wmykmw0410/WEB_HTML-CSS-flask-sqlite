# フロントエンド編

ブラウザの中で動く**HTML**（構造）・**CSS**（見た目）・**JavaScript**（動き）を学びます。Python・Flaskはまだ使いません。

## ゴール

**自分を紹介するオリジナルHPの完成**がフロントエンド編のゴールです。4ページ以上のサイトを、各章の「制作課題」で少しずつ作り、11_homepage で仕上げます（補足として公開方法も紹介）。作る場所は[00_my_homepage/](00_my_homepage/)です。

ここで学ぶHTML・CSS・JavaScriptは、バックエンド編の最初の章 [02_backend/02_memo_app_frontend](../02_backend/02_memo_app_frontend/) で、ブラウザだけで動くメモ帳アプリを作るときにそのまま使います。

## 章の構成

Webページが表示されるしくみ（リクエストとレスポンス・URL・ステータスコードなど）は、補足資料の[00_docs/web_basic](../00_docs/web_basic/)にまとめています。章の中でわからない言葉が出てきたときに読んでください。

| 章 | 学ぶこと | オリジナルHP（制作課題） |
|---|---|---|
| [01_html_basics](01_html_basics/) | 開発環境と開発者ツール・HTML文書の骨組み・テキストと基本タグ・表 | — |
| [02_html_semantic_form](02_html_semantic_form/) | セマンティックHTMLとアクセシビリティ・フォーム | ステップ1：4ページのHTML |
| [03_css_basics](03_css_basics/) | CSSの書き方・文字と色と単位・基本のセレクタ・classとid・背景と装飾・（補足）カスケードと詳細度 | — |
| [04_css_layout](04_css_layout/) | ボックスモデルとdisplay・Flexbox・Grid・レスポンシブ対応・CSS変数・フォームの装飾 | ステップ2：`style.css` |
| [05_js_basics](05_js_basics/) | JavaScriptの読み込みとデバッグ・最小限の基本文法・真偽の判定・関数とコールバック | — |
| [06_js_events](06_js_events/) | イベント（クリック・入力・ホバー・フォーカス・submit）・入力チェック（ブラウザで動かす） | — |
| [07_js_dom](07_js_dom/) | DOM操作（`querySelector`・属性・要素の作成・XSS） | — |
| [08_js_render](08_js_render/) | 配列メソッド（`map`・`filter`・`find`・`includes`）・データから画面を作る（`render()`）・クライアント側での絞り込み | ステップ3：`script.js` |
| [09_js_ui](09_js_ui/) | タブ切り替え・ポップアップ（`popover`）・モーダルウィンドウ（`<dialog>`）・スライドショー・スクロール動作 | （自由課題で使う） |
| [10_js_data](10_js_data/) | JSON・`fetch()`・`async`/`await`・エラー処理・`localStorage`・データから画面を作る・HTTPメソッドの体験（JSONPlaceholder。発展・任意） | ステップ4：データの分離 |
| [11_homepage](11_homepage/) | ファビコン・OGP・画像の最適化・品質チェック・GitHub Pagesでの公開（補足）・全機能を盛り込んだ完成版の作例（`sample/`） | ステップ5：**完成** |

## 各章の構成

| フォルダ | 内容 |
|---|---|
| `README.md` | 学習内容（各節に「動作確認」の表あり） |
| `example/` | 各節のサンプル。**1つのサンプルが1つのフォルダ**（例：`example/01_structure/`）になっていて、中の`index.html`をブラウザで開き、書き換えながら動きを確かめる |
| `question/` | 練習問題。**1つの問題が1つのフォルダ**（例：`question/01_profile_page/`）。解答は`question/answer/`の下の、問題と同じ名前のフォルダにある。問題文はREADMEの各節の最後（「練習問題◯」）にあり、学ぶ順に取り組める。ファイルには、書く場所を示す`TODO`の目印だけを置いている |

サンプル・問題のフォルダの中は、どれも同じ名前のファイルでできています。

| ファイル | 内容 |
|---|---|
| `index.html` | ブラウザで開くページ |
| `script.js` | JavaScript（05_js_basics 以降） |
| `css/style.css` | 外部CSSファイル（03_css_basics の練習問題1・サンプル1など、一部だけ） |
| `img/`・`data/` | そのページで使う画像・JSONデータ |
| `challenge/` | 制作課題（オリジナルHP）の雛形。架空の人物「山田 太郎」のサイトを題材に、TODOコメントに沿って書く。完成例は`answer/`。練習のあと、同じことを[00_my_homepage/](00_my_homepage/)の自分のHPに反映する |

## ページの開き方

ブラウザ・VS Code・拡張機能（Live Server）・Pythonの用意は、[00_docs/setup/frontend.md](../00_docs/setup/frontend.md)にまとめています。章をまたいで出てくる用語は、[00_docs/glossary](../00_docs/glossary/)（用語集）で引けます。

01〜07章のページは、HTMLファイルをブラウザで直接開くだけで動きます。10_js_data・11_homepageの`fetch()`を使うページは、簡易サーバーを起動して開きます（10_js_data の0節を参照）。

```bash
cd 01_frontend/10_js_data
python -m http.server 8000
# → http://localhost:8000/
```
