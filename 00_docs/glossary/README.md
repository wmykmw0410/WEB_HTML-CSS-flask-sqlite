# 用語集

このカリキュラムで、章をまたいで何度も出てくる用語をまとめます。意味を忘れたときに引き、詳しい説明は「詳しく学ぶ章」の節で読み直してください。

## 目次

- [Webのしくみ](#webのしくみ)
- [HTML・CSS](#htmlcss)
- [JavaScript](#javascript)
- [Python](#python)
- [Flask](#flask)
- [フォームとセキュリティ](#フォームとセキュリティ)
- [データベース](#データベース)
- [ログイン](#ログイン)
- [開発環境](#開発環境)

---

## Webのしくみ

| 用語 | 意味 | 詳しく学ぶ章 |
|---|---|---|
| **クライアント** | サービスを利用する側。Webではブラウザのこと | [web_basic](../web_basic/) 1節 |
| **サーバー** | クライアントからの依頼に応えて、データやページを返す側のコンピュータ（またはプログラム） | [web_basic](../web_basic/) 1節 |
| **フロントエンド** | ブラウザの中で動く部分（HTML・CSS・JavaScript） | [web_basic](../web_basic/) 2節 |
| **バックエンド** | サーバーの中で動く部分（Python・Flask・データベース） | [web_basic](../web_basic/) 2節 |
| **URL** | Web上の場所を表す住所。`https://example.com/memos?category=仕事`のように、スキーム・ドメイン・パス・クエリなどからなる | [web_basic](../web_basic/) 3節 |
| **HTTP** | ブラウザとサーバーがやりとりするときの決まり（プロトコル）。暗号化したものが**HTTPS** | [web_basic](../web_basic/) 6節 |
| **リクエスト** | クライアントからサーバーへ送る「このページをください」「このデータを保存して」という依頼。メソッド・URL・ヘッダー・ボディからなる | [web_basic](../web_basic/) 4節・[08_request](../../02_backend/08_request/) |
| **レスポンス** | リクエストに対してサーバーが返す返事。ステータスコード・ヘッダー・ボディ（HTMLやJSONなど）からなる | [web_basic](../web_basic/) 4節 |
| **HTTPメソッド** | リクエストの種類。GET（取得）・POST（送信・作成）・PUT（丸ごと更新）・PATCH（一部更新）・DELETE（削除）など | [web_basic](../web_basic/) 4節・[08_request](../../02_backend/08_request/) 1節 |
| **ステータスコード** | レスポンスの結果を表す3桁の数字。200（成功）・302（リダイレクト）・404（見つからない）・500（サーバー内部のエラー）など | [web_basic](../web_basic/) 5節・[04_flask_basic](../../02_backend/04_flask_basic/) 5節 |
| **ヘッダー** | リクエストやレスポンスに付く補足情報。データの種類（`Content-Type`）やCookieなどを伝える | [web_basic](../web_basic/) 4節 |
| **静的サイト／動的サイト** | 静的サイトは、いつ誰が見ても同じファイルを返すサイト。動的サイトは、人や条件によってサーバーが内容を作って返すサイト | [web_basic](../web_basic/) 7節 |
| **ドメイン・DNS** | ドメインは`example.com`のような人が覚えやすい名前。DNSは、ドメインをIPアドレスに変換するしくみ | [web_basic](../web_basic/) 8節 |
| **IPアドレス** | ネットワーク上のコンピュータの番号。`127.0.0.1`（自分自身）など | [web_basic](../web_basic/) 9節 |
| **ポート** | 1台のコンピュータの中で、どのプログラムに通信を届けるかを表す番号。`http://127.0.0.1:5000/`の`5000` | [04_flask_basic](../../02_backend/04_flask_basic/) 1節 |
| **API** | プログラムどうしがやりとりするための窓口。Webでは、URLにリクエストを送るとJSONでデータを返すものを指すことが多い（**Web API**・**JSON API**） | [10_js_data](../../01_frontend/10_js_data/) 6節・[08_request](../../02_backend/08_request/) 2節 |
| **CRUD** | データに対する4つの基本操作。Create（作成）・Read（読み取り）・Update（更新）・Delete（削除） | [web_basic](../web_basic/) 4節・[10_sql](../../02_backend/10_sql/) |
| **開発者ツール** | ブラウザに付いている、HTML・CSS・通信の中身などを確かめる道具。F12キーで開く | [web_basic](../web_basic/) 10節・[01_html_basics](../../01_frontend/01_html_basics/) 0節 |

---

## HTML・CSS

| 用語 | 意味 | 詳しく学ぶ章 |
|---|---|---|
| **要素・タグ・属性** | `<a href="...">リンク</a>`全体が要素、`<a>`・`</a>`がタグ、`href="..."`が属性 | [01_html_basics](../../01_frontend/01_html_basics/) 1節 |
| **セマンティックHTML** | `<header>`・`<nav>`・`<main>`など、内容の意味を表すタグで書くこと | [02_html_semantic_form](../../01_frontend/02_html_semantic_form/) 1節 |
| **アクセシビリティ** | 目や耳が不自由な人、キーボードだけで操作する人なども含めて、誰でも使えるようにすること | [02_html_semantic_form](../../01_frontend/02_html_semantic_form/) 1節 |
| **セレクタ** | CSSで「どの要素に」スタイルを当てるかを指定する書き方。`.memo`・`#flash`・`a:hover`など。JavaScriptの`querySelector()`でも使う | [03_css_basics](../../01_frontend/03_css_basics/) 3節 |
| **カスケード・詳細度** | 同じ要素に複数のスタイルが当たったとき、どれを使うかの決まり | [03_css_basics](../../01_frontend/03_css_basics/) 補足 |
| **ボックスモデル** | 要素を「内容・padding・border・margin」の四角い箱として扱う考え方 | [04_css_layout](../../01_frontend/04_css_layout/) 1節 |
| **Flexbox・Grid** | 要素を横や縦、格子状に並べるCSSのしくみ | [04_css_layout](../../01_frontend/04_css_layout/) 2・3節 |
| **レスポンシブ** | 画面の幅に合わせて、レイアウトを切り替えること。**メディアクエリ**（`@media`）で書く | [04_css_layout](../../01_frontend/04_css_layout/) 4節 |
| **モバイルファースト** | スマホ向けのスタイルを先に書き、広い画面向けのスタイルをメディアクエリで足していく書き方 | [04_css_layout](../../01_frontend/04_css_layout/) 4節 |
| **CSS変数** | `--main-color: #333;`のように値に名前を付け、`var(--main-color)`で使い回すしくみ。ダークモードの切り替えにも使う | [04_css_layout](../../01_frontend/04_css_layout/) 5節 |

---

## JavaScript

| 用語 | 意味 | 詳しく学ぶ章 |
|---|---|---|
| **DOM** | ブラウザが、HTMLを読み込んで作る「要素の木構造」。JavaScriptはDOMを通してページを書き換える | [07_js_dom](../../01_frontend/07_js_dom/) 1節 |
| **イベント** | クリック・入力・送信など、ページの上で起きたできごと。`addEventListener()`で、起きたときの処理を登録する | [06_js_events](../../01_frontend/06_js_events/) 1節 |
| **コールバック関数** | 「あとで呼び出してもらう」ために、別の関数に渡す関数 | [05_js_basics](../../01_frontend/05_js_basics/) 2節 |
| **XSS**（クロスサイトスクリプティング） | 入力された文字列をHTMLとして表示してしまい、悪意あるスクリプトが動いてしまう攻撃。`innerHTML`ではなく`textContent`を使うのが基本の対策 | [07_js_dom](../../01_frontend/07_js_dom/) 1節 |
| **JSON** | `{"title": "買い物", "is_pinned": true}`のように、データを文字で表す書き方。ブラウザとサーバーのやりとりや、ファイルへの保存に使う | [10_js_data](../../01_frontend/10_js_data/) 1節・[07_with](../../02_backend/07_with/) 7節 |
| **非同期処理** | 通信など時間のかかる処理の完了を待たずに、ほかの処理を進めるしくみ。`async`／`await`で書く | [10_js_data](../../01_frontend/10_js_data/) 2節 |
| **fetch()** | JavaScriptからサーバーにリクエストを送る関数 | [10_js_data](../../01_frontend/10_js_data/) 2節 |
| **Ajax** | ページを再読み込みせずに、通信して画面の一部だけを書き換えるやり方 | [10_js_data](../../01_frontend/10_js_data/) 2節 |
| **localStorage** | ブラウザの中にデータ（文字列）を保存するしくみ。ページを閉じても消えないが、そのブラウザの中にしか無い | [10_js_data](../../01_frontend/10_js_data/) 4節・[02_memo_app_frontend](../../02_backend/02_memo_app_frontend/) |

---

## Python

| 用語 | 意味 | 詳しく学ぶ章 |
|---|---|---|
| **引数・戻り値** | 引数は関数に渡す値、戻り値は関数が`return`で返す値 | [03_function](../../02_backend/03_function/) 2〜4節 |
| **None** | 「値が無い」ことを表すPythonの値。`return`を書かない関数は`None`を返す | [03_function](../../02_backend/03_function/) 5節 |
| **スコープ** | 変数が使える範囲。関数の中で作った変数（ローカル変数）は、関数の外からは使えない | [03_function](../../02_backend/03_function/) 6節 |
| **クロージャ** | 外側の関数の変数を覚えたまま、あとから呼び出せる内側の関数 | [03_function](../../02_backend/03_function/) 8節 |
| **デコレータ** | 関数を受け取り、機能を足した関数を返す関数。`@名前`を関数の上に書いて使う。Flaskの`@app.route()`もデコレータ | [03_function](../../02_backend/03_function/) 9・10節 |
| **with文（コンテキストマネージャー）** | ファイルなどを開いて使い、終わったら必ず閉じる処理を、短く安全に書く構文 | [07_with](../../02_backend/07_with/) 1〜3節 |
| **型ヒント** | `def add(a: int, b: int) -> int:`のように、引数や戻り値の型を書いておくこと。実行時には強制されない | [16_typehints](../../02_backend/16_typehints/) 1節 |
| **docstring** | 関数の最初の行に`"""`で囲んで書く、関数の説明文 | [16_typehints](../../02_backend/16_typehints/) 5節 |

---

## Flask

| 用語 | 意味 | 詳しく学ぶ章 |
|---|---|---|
| **フレームワーク** | アプリを作るための土台と決まりごとのセット。FlaskはPythonのWebフレームワーク | [04_flask_basic](../../02_backend/04_flask_basic/) 1節 |
| **ルーティング** | URLと、そのURLにアクセスされたときに動く関数を結びつけること。Flaskでは`@app.route('/memos')`と書く | [04_flask_basic](../../02_backend/04_flask_basic/) 2節 |
| **ビュー関数・エンドポイント** | ビュー関数は、ルートに結びつけた関数。エンドポイントは、その関数の名前（`url_for('index')`の`'index'`） | [04_flask_basic](../../02_backend/04_flask_basic/) 2節 |
| **パスパラメータ** | URLの一部を値として受け取るしくみ。`/memos/<int:memo_id>`の`memo_id` | [04_flask_basic](../../02_backend/04_flask_basic/) 3節・[08_request](../../02_backend/08_request/) 3節 |
| **クエリパラメータ** | URLの`?`より後ろに付ける`キー=値`。`/memos?category=仕事`。Flaskでは`request.args`で受け取る | [04_flask_basic](../../02_backend/04_flask_basic/) 3節・[08_request](../../02_backend/08_request/) 2節 |
| **テンプレート** | 値を差し込む場所を空けておいたHTML。`render_template()`で値を渡してHTMLを作る | [04_flask_basic](../../02_backend/04_flask_basic/) 4節 |
| **Jinja2** | Flaskが使うテンプレートエンジン。`{{ 変数 }}`・`{% for %}`・`{% if %}`などを書ける | [06_jinja2](../../02_backend/06_jinja2/) 1節 |
| **テンプレート継承** | 共通の枠（`base.html`）を作り、ページごとに違う部分（ブロック）だけを書く方法 | [06_jinja2](../../02_backend/06_jinja2/) 2節 |
| **リダイレクト** | 「別のURLを見に行って」とブラウザに伝えるレスポンス。`redirect()`で返す | [05_redirect](../../02_backend/05_redirect/) 1節 |
| **url_for()** | エンドポイントの名前からURLを作る関数。URLを直接書かずに済む | [05_redirect](../../02_backend/05_redirect/) 3・4節 |
| **requestオブジェクト** | 届いたリクエストの中身（メソッド・クエリパラメータ・フォームの値など）を読むためのオブジェクト | [08_request](../../02_backend/08_request/) |
| **jsonify()** | Pythonの辞書やリストを、JSONのレスポンスにして返す関数 | [08_request](../../02_backend/08_request/) 2節 |
| **静的ファイル** | CSS・JavaScript・画像など、加工せずにそのまま返すファイル。Flaskでは`static/`フォルダに置くと`/static/ファイル名`で配信される | [01_intro](../../02_backend/01_intro/) 3節・[04_flask_basic](../../02_backend/04_flask_basic/) の練習問題 |
| **abort()・エラーハンドラー** | `abort(404)`で処理を止めてエラーを返す。`@app.errorhandler(404)`で、エラーのときに表示するページを決める | [04_flask_basic](../../02_backend/04_flask_basic/) 5節 |
| **デバッグモード** | `app.run(debug=True)`で有効になる開発用の設定。コードを保存すると自動で再起動し、エラーの詳細を画面に出す。本番では使わない | [04_flask_basic](../../02_backend/04_flask_basic/) 1節 |
| **アプリケーションコンテキスト** | 「今どのFlaskアプリの処理中か」という状態。ルートの外でデータベースを操作するときは`with app.app_context():`の中で行う | [13_flask_sqlalchemy](../../02_backend/13_flask_sqlalchemy/) 2節 |
| **Blueprint** | ルートを機能ごと（ログイン・メモなど）のファイルに分けるしくみ | [17_blueprint](../../02_backend/17_blueprint/) 1節 |
| **gオブジェクト** | 1回のリクエストの間だけ、データを置いておける場所 | [17_blueprint](../../02_backend/17_blueprint/) 2節 |

---

## フォームとセキュリティ

| 用語 | 意味 | 詳しく学ぶ章 |
|---|---|---|
| **フォーム** | 入力欄と送信ボタンで、データをサーバーに送るしくみ。`<form method="post">` | [02_html_semantic_form](../../01_frontend/02_html_semantic_form/) 2節・[09_forms](../../02_backend/09_forms/) 1節 |
| **バリデーション（入力チェック）** | 送られた値が正しいか（空でないか・長すぎないかなど）を確かめること。ブラウザ側のチェックは無効にできるので、サーバー側でも必ず行う | [09_forms](../../02_backend/09_forms/) 3節 |
| **WTForms・Flask-WTF** | フォームの項目と入力チェックをPythonのクラスで書くライブラリ。Flask-WTFはそれをFlaskで使いやすくし、CSRF対策を加えたもの | [09_forms](../../02_backend/09_forms/) 2〜4節 |
| **CSRF**（クロスサイトリクエストフォージェリ） | ログイン中の人に、別のサイトから気づかないうちにリクエストを送らせる攻撃。フォームに**CSRFトークン**（サーバーが発行した合言葉）を埋め込み、一致しない送信を断って防ぐ | [09_forms](../../02_backend/09_forms/) 4節・[15_login](../../02_backend/15_login/) 1節 |
| **Cookie** | サーバーの指示でブラウザが保存し、次のリクエストから自動で送り返す小さなデータ | [09_forms](../../02_backend/09_forms/) 5節 |
| **セッション** | Cookieを使って、同じ人からの複数のリクエストを「つながり」として扱うしくみ。Flaskでは`session`に値を保存する | [09_forms](../../02_backend/09_forms/) 5節 |
| **PRGパターン** | POSTを受けたら、ページを直接返さずにリダイレクトし、GETで表示し直す書き方。再読み込みで同じ送信が繰り返されるのを防ぐ | [09_forms](../../02_backend/09_forms/) 5節 |
| **flash()** | 次の画面に1回だけメッセージ（「保存しました」など）を表示するしくみ | [15_login](../../02_backend/15_login/) 2節 |
| **SECRET_KEY** | セッションやCSRFトークンを、改ざんされないように署名するための秘密の文字列 | [09_forms](../../02_backend/09_forms/) 4節 |

---

## データベース

| 用語 | 意味 | 詳しく学ぶ章 |
|---|---|---|
| **データベース（DB）** | データを整理して保存し、検索・追加・更新・削除ができるようにしたしくみ | [10_sql](../../02_backend/10_sql/) |
| **テーブル・カラム・レコード** | テーブルは表、カラムは列（項目）、レコードは行（1件のデータ） | [10_sql](../../02_backend/10_sql/) |
| **SQL** | データベースを操作する言語。`SELECT`・`INSERT`・`UPDATE`・`DELETE`など | [10_sql](../../02_backend/10_sql/) |
| **SQLite** | 1つのファイルにデータベースを保存する、手軽なデータベース。Pythonに最初から入っている | [10_sql](../../02_backend/10_sql/)・[11_sqlite](../../02_backend/11_sqlite/) |
| **主キー・外部キー** | 主キーはレコードを1件に特定する列（`id`）。外部キーは、別のテーブルの主キーを指す列 | [10_sql](../../02_backend/10_sql/)（basic 2・7節） |
| **JOIN** | 複数のテーブルを、外部キーなどでつないで1つの表として取り出すこと | [10_sql](../../02_backend/10_sql/)（basic 7節）・[12_sqlalchemy](../../02_backend/12_sqlalchemy/) 3節 |
| **トランザクション** | 複数の操作を「全部成功」か「全部取り消し」のどちらかにまとめるしくみ。確定が`commit`、取り消しが`rollback` | [10_sql](../../02_backend/10_sql/)（advanced 3節）・[11_sqlite](../../02_backend/11_sqlite/) |
| **プレースホルダー** | SQLの中の値を`?`にしておき、値は別に渡す書き方。**SQLインジェクション**（入力でSQLを書き換える攻撃）を防ぐ | [11_sqlite](../../02_backend/11_sqlite/) 3節 |
| **ORM** | テーブルをPythonのクラス、レコードをオブジェクトとして扱い、SQLを書かずにデータベースを操作するしくみ。SQLAlchemyがその代表 | [12_sqlalchemy](../../02_backend/12_sqlalchemy/) |
| **モデル** | ORMで、テーブルを表すクラス。`class Memo(db.Model):` | [12_sqlalchemy](../../02_backend/12_sqlalchemy/) 1節・[13_flask_sqlalchemy](../../02_backend/13_flask_sqlalchemy/) 3節 |
| **リレーション** | テーブルどうしの関係。1対多（1人のユーザーに多くのメモ）・多対多など | [12_sqlalchemy](../../02_backend/12_sqlalchemy/) 4・5節 |
| **マイグレーション** | テーブルの作成や変更の手順をファイルとして記録し、`flask db upgrade`などのコマンドでデータベースに反映するしくみ | [14_flask_migrate](../../02_backend/14_flask_migrate/) |

その他のSQLの用語（クエリ・NULL・DDL／DMLなど）は、[10_sqlの用語集](../../02_backend/10_sql/#用語集)にまとめています。

---

## ログイン

| 用語 | 意味 | 詳しく学ぶ章 |
|---|---|---|
| **認証** | 「あなたは誰か」を確かめること。ユーザー名とパスワードでのログインなど | [15_login](../../02_backend/15_login/) 2・3節 |
| **認可** | 「その人に、その操作をしてよいか」を決めること。ログインした人だけがメモを追加できる、など | [15_login](../../02_backend/15_login/) 2節 |
| **Flask-Login** | ログイン状態をセッションで管理するライブラリ。`login_user()`・`logout_user()`・`current_user`・`@login_required`を使う | [15_login](../../02_backend/15_login/) 2節 |
| **ハッシュ化** | パスワードを、元に戻せない別の文字列に変換して保存すること。データベースが漏れても、元のパスワードがわからない | [15_login](../../02_backend/15_login/) 6節 |

---

## 開発環境

| 用語 | 意味 | 詳しく学ぶ章 |
|---|---|---|
| **ライブラリ（パッケージ）** | ほかの人が作った、再利用できるプログラムのまとまり。Flaskもライブラリ | [setup/backend.md](../setup/backend.md) |
| **pip** | Pythonのライブラリをインストールするコマンド。`pip install -r 00_docs/setup/requirements.txt`で、一覧に書いたライブラリをまとめて入れられる | [setup/backend.md](../setup/backend.md) |
| **仮想環境（venv）** | プロジェクトごとに、ライブラリを分けて入れておく場所。このカリキュラムでは`flaskenv` | [setup/backend.md](../setup/backend.md) |
| **ターミナル** | 文字でコマンドを打ってコンピュータを操作する画面 | [setup/frontend.md](../setup/frontend.md) |
| **ローカルサーバー** | 自分のパソコンの中で動かすサーバー。`python -m http.server`やFlaskの`app.run()`。`127.0.0.1`（`localhost`）でアクセスする | [10_js_data](../../01_frontend/10_js_data/) 0節・[04_flask_basic](../../02_backend/04_flask_basic/) 1節 |
| **curl** | ターミナルからHTTPリクエストを送るコマンド。ブラウザでは送りにくいPOST・PUT・DELETEを試すのに使う | [08_request](../../02_backend/08_request/) 1節 |
| **Git・GitHub** | Gitはファイルの変更履歴を記録する道具。GitHubは、Gitで記録したものをネット上に置いて共有するサービス | [github/](../github/) |
