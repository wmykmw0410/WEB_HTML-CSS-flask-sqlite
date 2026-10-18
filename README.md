# Webアプリ開発カリキュラム（フロントエンド ＋ バックエンド）

Webアプリを基礎から作れるようになるための、番号付きチャプター集です。**フロントエンド編**（ブラウザで動くHTML・CSS・JavaScript）と、**バックエンド編**（サーバーで動くPython・Flask・データベース）の2部構成になっています。

```
次回:

メモ:
```

---

## 全体像

```
├── 00_docs/      環境構築・Webページが表示されるしくみ・用語集・Pythonの文法リファレンス・GitHubの使い方
│
├── 01_frontend/  フロントエンド編
│     ゴール：オリジナルHP（自分を紹介するサイト。補足として公開方法も）
│
└── 02_backend/   バックエンド編
      01_intro：FlaskとSQLiteのメモ帳を、コードを貼り付けながら1時間で体験する
      02_memo_app_frontend：まずブラウザだけで動くメモアプリ（localStorage に保存）を完成させる
      03〜17：その保存先を「ブラウザ」から「サーバー」へ移し、
              データベース・ログイン・アプリの構造化までを学ぶ（完成形は 02_backend/100_memo_api）
```

バックエンド編では、1つの**メモ帳アプリ**が一貫した題材です。最初の章で、フロントエンド編で学んだJavaScriptを使って「ブラウザだけで動く版」を完成させ、そこから「データをサーバーに保存する版」へ作り替えていくことで、サーバーが何のためにあるのかを体験しながら学べます。

---

## 進捗

### フロントエンド編
- [ ] 01_frontend/01_html_basics — 開発環境と開発者ツール・HTML文書の骨組み・テキストと基本タグ・表
- [ ] 01_frontend/02_html_semantic_form — セマンティックHTMLとアクセシビリティ・フォーム
- [ ] 01_frontend/03_css_basics — CSSの書き方と単位・セレクタ・カスケードと詳細度・ボックスモデル・文字と装飾
- [ ] 01_frontend/04_css_layout — Flexbox・Grid・position・レスポンシブ対応・CSS変数とトランジション
- [ ] 01_frontend/05_js_basics — JavaScriptの読み込みとデバッグ・最小限の基本文法・真偽の判定・関数とコールバック
- [ ] 01_frontend/06_js_events — イベント（クリック・入力・submit）・入力チェック（ブラウザで動かす）
- [ ] 01_frontend/07_js_dom — DOM操作（要素の取得・書き換え・作成・XSS）
- [ ] 01_frontend/08_js_render — 配列メソッド・データから画面を作る・絞り込み
- [ ] 01_frontend/09_js_ui — タブ・ポップアップ・モーダルウィンドウ・スライドショー・スクロール
- [ ] 01_frontend/10_js_data — JSON・`fetch()`・`async`/`await`・エラー処理・`localStorage`・データから画面を作る・HTTPメソッドの体験
- [ ] 01_frontend/11_homepage — オリジナルHPの仕上げ（フロントエンド編のゴール）
- [ ] 01_frontend/00_my_homepage — 自分のオリジナルHP（各章の制作課題で育てる）

### バックエンド編：完成形（最初に触ってみる）
- [ ] 02_backend/100_memo_api — バックエンド編の完成形（統合アプリ）

### バックエンド編：出発点
- [ ] 02_backend/01_intro — FlaskとSQLiteを1時間で体験する（イントロダクション）
- [ ] 02_backend/02_memo_app_frontend — ブラウザだけで動くメモアプリの完成と、その限界

### バックエンド編：Flaskの基礎
- [ ] 02_backend/03_function — 関数の基本・デコレータ
  - [ ] サンプル ex01〜ex14
  - [ ] 練習問題 question01〜09
- [ ] 02_backend/04_flask_basic — Hello World・ルーティング・render_template
- [ ] 02_backend/05_redirect — redirect・url_for
- [ ] 02_backend/06_jinja2 — Jinja2
- [ ] 02_backend/07_with — with文・コンテキストマネージャー
- [ ] 02_backend/08_request — request・HTTPメソッド

### バックエンド編：データ処理とフォーム
- [ ] 02_backend/09_forms — WTForms・Flask-WTF・CSRF
- [ ] 02_backend/10_sql — SQL基礎（SQLite CLI）
- [ ] 02_backend/11_sqlite — sqlite3モジュール
- [ ] 02_backend/12_sqlalchemy — SQLAlchemy ORM
- [ ] 02_backend/13_flask_sqlalchemy — Flask-SQLAlchemy
  - [ ] question01〜06
- [ ] 02_backend/14_flask_migrate — Flask-Migrate

### バックエンド編：認証・構造化
- [ ] 02_backend/15_login — Flask-Login
- [ ] 02_backend/16_typehints — 型ヒント（Optional・Union）
- [ ] 02_backend/17_blueprint — Blueprint・gオブジェクト

### 自分のアプリへの統合
- [ ] 02_backend/00_my_app — バックエンド編で学んだ内容を積み上げる

---

## 進め方

1. [00_docs/setup/frontend.md](00_docs/setup/frontend.md)の手順で、ブラウザ・VS Code・拡張機能を用意してから、[フロントエンド編](01_frontend/)を`01_html_basics`から順に進める。URLやリクエストなど、Webサイトがどう動いているかは、必要に応じて[00_docs/web_basic](00_docs/web_basic/)で確かめる。各章の最後にある「制作課題」で、[01_frontend/00_my_homepage](01_frontend/00_my_homepage/)に自分のオリジナルHPを少しずつ作っていく
2. [02_backend/100_memo_api](02_backend/100_memo_api/)を実行し（[00_docs/setup/backend.md](00_docs/setup/backend.md)の環境が必要）、バックエンド編で最終的にどんなアプリができあがるのかを体験する
3. [00_docs/setup/backend.md](00_docs/setup/backend.md)の手順で、Python・仮想環境・ライブラリ・VS Codeの拡張機能を用意してから、[バックエンド編](02_backend/)を`01_intro`から`17_blueprint`まで順に進める。学んだ内容は[02_backend/00_my_app](02_backend/00_my_app/)という**自分だけの統合アプリ**に少しずつ積み上げていく（詳細は後述）

各チャプターは`README.md`（学習内容）・`example/`（サンプルコード）・`question/`（練習問題）・`challenge/`（演習）で構成されています（章によって一部が無い場合があります）。

## 動作確認済みのライブラリバージョン

環境構築の手順は[00_docs/setup/backend.md](00_docs/setup/backend.md)にまとめています。各チャプターの`pip install`では特にバージョンを指定していませんが、このカリキュラムは以下のバージョンで動作確認しています。インストール時にエラーが出る場合は、まずこのバージョンに合わせてみてください。

| パッケージ | バージョン |
|---|---|
| Flask | 2.3.3 |
| Flask-WTF | 1.2.2 |
| Flask-Login | 0.6.3 |
| Flask-SQLAlchemy | 3.0.3 |
| Flask-Migrate | 4.0.4 |
| SQLAlchemy | 2.0.48 |

同じ内容を[00_docs/setup/requirements.txt](00_docs/setup/requirements.txt)にまとめているので、仮想環境を有効にしてから、リポジトリのルートで次のコマンドを実行すればまとめてインストールできます。

```bash
pip install -r 00_docs/setup/requirements.txt
```

## チャプター一覧

### フロントエンド編（[01_frontend/](01_frontend/)）

Webページが表示されるしくみ（リクエストとレスポンス・URL・ステータスコード・HTTPS・IPアドレス・開発者ツールのNetworkタブ）は、補足資料の[00_docs/web_basic](00_docs/web_basic/)にまとめています。

| # | チャプター | 学ぶ内容 | オリジナルHP（制作課題） |
|---|---|---|---|
| 01 | [html_basics](01_frontend/01_html_basics/) | 開発環境と開発者ツール・HTML文書の骨組み・テキストと基本タグ・表 | — |
| 02 | [html_semantic_form](01_frontend/02_html_semantic_form/) | セマンティックHTMLとアクセシビリティ・フォーム | ステップ1：4ページのHTML |
| 03 | [css_basics](01_frontend/03_css_basics/) | CSSの書き方と単位・セレクタ・カスケードと詳細度・ボックスモデル・文字と装飾 | — |
| 04 | [css_layout](01_frontend/04_css_layout/) | Flexbox・Grid・position・レスポンシブ対応・CSS変数とトランジション | ステップ2：`style.css` |
| 05 | [js_basics](01_frontend/05_js_basics/) | JavaScriptの読み込みとデバッグ・最小限の基本文法・真偽の判定・関数とコールバック | — |
| 06 | [js_events](01_frontend/06_js_events/) | イベント（クリック・入力・ホバー・フォーカス・submit）・入力チェック（ブラウザで動かす） | — |
| 07 | [js_dom](01_frontend/07_js_dom/) | DOM操作（`querySelector`・属性・要素の作成・XSS） | — |
| 08 | [js_render](01_frontend/08_js_render/) | 配列メソッド（`map`・`filter`・`find`・`includes`）・データから画面を作る（`render()`）・クライアント側での絞り込み | ステップ3：`script.js` |
| 09 | [js_ui](01_frontend/09_js_ui/) | タブ切り替え・ポップアップ（`popover`）・モーダルウィンドウ（`<dialog>`）・スライドショー・スクロール動作 | （自由課題で使う） |
| 10 | [js_data](01_frontend/10_js_data/) | JSON・`fetch()`・`async`/`await`・エラー処理・`localStorage`・データから画面を作る・HTTPメソッドの体験（JSONPlaceholder。発展・任意） | ステップ4：データの分離 |
| 11 | [homepage](01_frontend/11_homepage/) | ファビコン・OGP・画像の最適化・品質チェック・GitHub Pagesでの公開（補足）・全機能を盛り込んだ完成版の作例（`sample/`） | ステップ5：**完成** |

### バックエンド編（[02_backend/](02_backend/)）

| # | チャプター | 学ぶ内容 |
|---|---|---|
| 01 | [intro](02_backend/01_intro/) | イントロダクション：コードを貼り付けながら、FlaskとSQLite（`sqlite3`）で一覧・追加・削除ができるメモ帳を1時間で作り、バックエンド編の全体像をつかむ |
| 02 | [memo_app_frontend](02_backend/02_memo_app_frontend/) | ブラウザだけで動き、`localStorage`に保存して追加・編集・削除できるメモ帳アプリを作る（HTML・CSSは用意済み。フロントエンド編のJavaScriptを使う）（アプリの設計・ファイルの分割・クエリ文字列）。完成したアプリの限界から、サーバーが必要な理由を確かめる |
| 03 | [function](02_backend/03_function/) | Pythonの関数の基本（引数・戻り値・スコープ）・デコレータ・`@app.route()`の仕組み |
| 04 | [flask_basic](02_backend/04_flask_basic/) | Hello World・ルーティング・動的URL・render_template・エラーハンドリング |
| 05 | [redirect](02_backend/05_redirect/) | `redirect()`・`url_for()`（内部/外部リダイレクト・引数付きURL生成） |
| 06 | [jinja2](02_backend/06_jinja2/) | Jinja2（変数展開・for/if・テンプレート継承・フィルター） |
| 07 | [with](02_backend/07_with/) | with文・コンテキストマネージャー・ファイル操作・`os.path` |
| 08 | [request](02_backend/08_request/) | `request`・HTTPメソッド（GET/POST/PUT/DELETE）・クエリパラメータでの絞り込み |
| 09 | [forms](02_backend/09_forms/) | WTForms・Flask-WTF・CSRF・session・ファイルアップロード |
| 10 | [sql](02_backend/10_sql/) | SQL基礎（SQLite CLI、Python/Flask不使用） |
| 11 | [sqlite](02_backend/11_sqlite/) | Python標準の`sqlite3`モジュール |
| 12 | [sqlalchemy](02_backend/12_sqlalchemy/) | SQLAlchemy ORM（素のSQLAlchemy） |
| 13 | [flask_sqlalchemy](02_backend/13_flask_sqlalchemy/) | Flask-SQLAlchemy（`db.Model`・`db.session`） |
| 14 | [flask_migrate](02_backend/14_flask_migrate/) | Flask-Migrate（`flask db`コマンドでのマイグレーション） |
| 15 | [login](02_backend/15_login/) | Flask-Login・パスワードハッシュ化・ログイン機能 |
| 16 | [typehints](02_backend/16_typehints/) | Python型ヒント（基本の型・`Optional`・`Union`） |
| 17 | [blueprint](02_backend/17_blueprint/) | Blueprint・`g`オブジェクト |

### 完成形（最初に触ってみる）

| # | チャプター | 学ぶ内容 |
|---|---|---|
| 100 | [memo_api](02_backend/100_memo_api/) | バックエンド編（01〜17）の集大成。データベース・ログイン・Blueprintで作るメモ帳アプリ（追加・詳細・編集・削除・ピン留め・絞り込み）。画面にはフロントエンド編の内容（モバイルファースト・ダークモード・通知・確認ダイアログ・入力チェック・下書き保存など）を取り入れている |

## 02_backend/00_my_app について

バックエンド編で学んだ内容を自分のアプリに積み上げていく専用チャプターです。`02_backend/02_memo_app_frontend`で完成させたブラウザ版のメモアプリを出発点に、一貫して1つの**メモ帳アプリ**を育てていきます。フロントエンド編のオリジナルHPは[01_frontend/00_my_homepage](01_frontend/00_my_homepage/)で育てます。使い方・進捗チェックリストは[02_backend/00_my_app/README.md](02_backend/00_my_app/)を参照してください。

## 補足資料

[00_docs/](00_docs/)に、学習の横に置いて使う資料をまとめています。

| フォルダ | 内容 |
|---|---|
| [setup/](00_docs/setup/) | 環境構築（[フロントエンド編](00_docs/setup/frontend.md)・[バックエンド編](00_docs/setup/backend.md)）・[VS Codeのおすすめ拡張機能](00_docs/setup/vscode.md)・ライブラリの一覧（[requirements.txt](00_docs/setup/requirements.txt)） |
| [glossary/](00_docs/glossary/) | 用語集（章をまたいで出てくる用語） |
| [python_grammar/](00_docs/python_grammar/) | Pythonの文法リファレンス（基礎・中級・発展） |
| [github/](00_docs/github/) | GitHubにリポジトリをpushする手順 |

## 参考リンク（公式ドキュメント）

| ライブラリ | ドキュメント |
|---|---|
| Flask | https://flask.palletsprojects.com/ |
| Jinja2 | https://jinja.palletsprojects.com/ |
| Werkzeug | https://werkzeug.palletsprojects.com/ |
| Flask-WTF | https://flask-wtf.readthedocs.io/ |
| WTForms | https://wtforms.readthedocs.io/ |
| Flask-Login | https://flask-login.readthedocs.io/ |
| Flask-SQLAlchemy | https://flask-sqlalchemy.palletsprojects.com/ |
| SQLAlchemy | https://docs.sqlalchemy.org/ |
| Flask-Migrate | https://flask-migrate.readthedocs.io/ |
| requests | https://requests.readthedocs.io/ |
| httpx | https://www.python-httpx.org/ |
| pytest | https://docs.pytest.org/ |
