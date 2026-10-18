# 00 自分だけのオリジナルHP

フロントエンド編のゴールは、**自分のことを紹介するオリジナルのホームページ（HP）を完成させる**ことです。このフォルダは、そのHPを作っていく自分専用の作業場所です（バックエンド編の[02_backend/00_my_app](../../02_backend/00_my_app/)と同じ考え方です）。

各章の最後にある「制作課題：オリジナルHP」では、まずその章の`challenge/`で、架空の人物「山田 太郎」のサイトを題材にTODOを埋めて練習します。そのあと、同じことをこのフォルダの自分のサイトに反映して、少しずつ育てていきます（バックエンド編で、各章の`challenge/`のあとに`00_my_app`へ反映するのと同じ流れです）。`challenge/answer/`の完成例は参考にして構いませんが、文章・配色・レイアウトは**自分で考えて**作りましょう。

## 進め方

| ステップ | 章 | このフォルダに加えること | 練習（雛形 ／ 完成例） |
|---|---|---|---|
| 1 | [02_html_semantic_form](../02_html_semantic_form/#制作課題オリジナルhpステップ1) | 4ページのHTML（ホーム・プロフィール・制作実績・お問い合わせ） | [02_html_semantic_form/challenge](../02_html_semantic_form/challenge/) ／ [answer](../02_html_semantic_form/challenge/answer/) |
| 2 | [04_css_layout](../04_css_layout/#制作課題オリジナルhpステップ2) | `css/style.css`（全ページ共通の見た目・レスポンシブ対応） | [04_css_layout/challenge](../04_css_layout/challenge/) ／ [answer](../04_css_layout/challenge/answer/) |
| 3 | [08_js_render](../08_js_render/#制作課題オリジナルhpステップ3) | `js/script.js`（ハンバーガーメニュー・絞り込み・フォームの入力チェック） | [08_js_render/challenge](../08_js_render/challenge/) ／ [answer](../08_js_render/challenge/answer/) |
| 4 | [10_js_data](../10_js_data/#制作課題オリジナルhpステップ4) | `data/works.json`（制作実績をデータとして分離し、`fetch()`で表示） | [10_js_data/challenge](../10_js_data/challenge/) ／ [answer](../10_js_data/challenge/answer/) |
| 5 | [11_homepage](../11_homepage/) | 仕上げ（ファビコン・OGP・品質チェック）と、補足として公開 | [11_homepage/challenge](../11_homepage/challenge/) ／ [answer](../11_homepage/challenge/answer/) |

タブ・モーダルウィンドウ・スライドショー・ダークテーマなど、さらに機能を足したくなったら、フロントエンド編の機能をすべて盛り込んだ完成版の作例 [11_homepage/sample](../11_homepage/sample/) を参考にしてください。

## フォルダ構成（完成時）

```
00_my_homepage/
├── index.html        ホーム
├── about.html        プロフィール
├── works.html        制作実績（作品がまだ無ければ「好きなもの紹介」などでもよい）
├── contact.html      お問い合わせ
├── css/style.css     ステップ2
├── js/script.js      ステップ3
├── data/works.json   ステップ4
└── img/              画像（アイコン・ファビコンなど）
```

ページの構成は自由に変えて構いません。ただし、各ステップの「必須要件」は満たすようにしてください。各章で学んだ内容を、漏れなく使う練習になっています。

## 個人情報についての注意

このHPは、11_homepage の補足でインターネットに公開できます。公開を考えて、最初から次の点に気をつけましょう。

- 本名・住所・電話番号・学校名や勤務先・顔写真など、**知らない人に知られて困る情報は載せない**（ニックネームやイラストのアイコンで十分）
- メールアドレスをページに直接書かない（お問い合わせフォームを使う）
- 他の人が作った画像や文章を、許可なく使わない

## 進捗チェック

- [ ] ステップ1：HTML（02_html_semantic_form）
- [ ] ステップ2：CSS（04_css_layout）
- [ ] ステップ3：JavaScript（08_js_render）
- [ ] ステップ4：データの分離（10_js_data）
- [ ] ステップ5：仕上げ（11_homepage）
