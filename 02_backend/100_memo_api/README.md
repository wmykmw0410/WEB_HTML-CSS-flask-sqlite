# 100 メモ帳アプリ（完成形）

バックエンド編（`02_backend/02_memo_app_frontend`〜`02_backend/17_blueprint`）で学んだ内容を1つにまとめたメモ帳アプリです。Flask・Jinja2・WTForms・Flask-SQLAlchemy・Flask-Migrate・Flask-Login・Blueprintで作られていて、**バックエンド編で学んだことだけ**で読めるようになっています。

画面（HTML・CSS・JavaScript）には、**フロントエンド編で学んだ内容**を取り入れています。見た目と操作は、[02_memo_app_frontend](../02_memo_app_frontend/)で作ったブラウザ版のメモアプリと同じです。違いは、データをブラウザ（`localStorage`）ではなくサーバーのデータベースに保存することと、ログインした人だけがメモを追加・編集・削除できることです。

## 目次

- [フォルダ構成](#フォルダ構成)
- [必要なパッケージ](#必要なパッケージ)
- [起動方法](#起動方法)
- [画面の機能](#画面の機能)
- [どの章の内容か](#どの章の内容か)
- [フロントエンド編から取り入れた項目](#フロントエンド編から取り入れた項目)
- [動作確認](#動作確認)
- [発展課題：編集・削除・ピン留めを自分で作る](#発展課題編集削除ピン留めを自分で作る)

---

## フォルダ構成

```
app/
├── app.py               アプリの作成・設定・Blueprintの登録・LoginManager・初期データの投入（init_db）
├── models.py            User・Memo（db = SQLAlchemy()）
├── forms.py             LoginForm・RegisterForm・MemoForm・ActionForm（削除・ピン留めのボタン用）
├── auth/views.py        認証の Blueprint（register / login / logout）
├── memos/views.py       メモの Blueprint（index / detail / create / update / delete / toggle_pin）
├── memos.json           初期データ（5件）
├── migrations/          マイグレーション（テーブルの作成）
├── static/
│   ├── style.css        モバイルファースト・ダークモード・フォーカス表示など
│   ├── script.js        通知・確認ダイアログ・絞り込み・入力チェック・下書き保存など
│   └── favicon.svg
├── templates/
│   ├── base.html        共通の枠（description・ファビコン・OGP・ナビ・通知・確認ダイアログ・トップへ戻るボタン）
│   ├── auth/            login.html・register.html
│   └── memos/
│       ├── index.html   メモ一覧（カテゴリ・キーワードの絞り込み）
│       ├── detail.html  メモ詳細
│       ├── create.html  メモ追加（_form.html を include。下書き保存あり）
│       ├── update.html  メモ編集（_form.html を include）
│       └── _form.html   追加・編集で共通のフォーム
├── Dockerfile・entrypoint.sh・docker-compose.yml   Dockerで動かすための設定
└── requirements.txt
```

## 必要なパッケージ

| パッケージ | バージョン | 用途 |
|---|---|---|
| Flask | 2.3.3 | Webフレームワーク本体 |
| Flask-WTF | 1.2.2 | フォーム・CSRF保護（`02_backend/09_forms`） |
| Flask-SQLAlchemy | 3.0.3 | ORM（`Memo`・`User`のモデル、`02_backend/13_flask_sqlalchemy`） |
| Flask-Migrate | 4.0.4 | マイグレーション（`flask db`コマンド、`02_backend/14_flask_migrate`） |
| Flask-Login | 0.6.3 | ログイン・セッション管理（`02_backend/15_login`） |

```bash
pip install Flask==2.3.3 Flask-WTF==1.2.2 Flask-Login==0.6.3 Flask-SQLAlchemy==3.0.3 Flask-Migrate==4.0.4
```

その他のチャプターも含めた一覧は[ルートのREADME](../../README.md#動作確認済みのライブラリバージョン)を参照してください。

## 起動方法

### ローカルで直接起動する場合

`migrations/`フォルダ（テーブルを作るマイグレーション）が入っているので、`flask db upgrade`だけでデータベースができます。`python app.py`で起動すると、メモが1件も無ければ`memos.json`の初期データ（5件）が入ります。

```bash
cd 02_backend/100_memo_api/app
flask db upgrade
python app.py
# → http://localhost:5085/ を開く
```

メモの一覧と詳細は誰でも見られます。追加・編集・削除・ピン留めは、`http://localhost:5085/auth/register`で登録してログインしてから行います。

### Dockerで起動する場合

`python app.py`（開発用サーバー）の代わりに、本番向けのWSGIサーバー（`gunicorn`）で動かすDocker構成も用意しています。

```bash
cd 02_backend/100_memo_api/app
docker compose up --build
```

マイグレーションの適用と初期データの投入も含めて、コンテナ起動時に自動で行われます（`entrypoint.sh`）。Dockerはこのカリキュラムでは扱わないため、使わない場合は上の手順で起動してください。

---

## 画面の機能

| ルート | メソッド | ログイン | 説明 |
|---|---|---|---|
| `/` | GET | 不要 | `/memos/`にリダイレクト |
| `/memos/` | GET | 不要 | メモ一覧（ピン留めを先頭に新しい順）。`?category=仕事`でサーバー側の絞り込み、JavaScriptでのカテゴリ・キーワードの絞り込みも利用可 |
| `/memos/<id>` | GET | 不要 | メモ詳細（無いIDは404） |
| `/memos/new` | GET/POST | 必要 | メモ追加。保存すると詳細ページへ |
| `/memos/<id>/edit` | GET/POST | 必要 | メモ編集 |
| `/memos/<id>/delete` | POST | 必要 | メモ削除（確認ダイアログを出してから送信） |
| `/memos/<id>/pin` | POST | 必要 | ピン留めのON/OFF。切り替えたら、押したページ（一覧・詳細）に戻る |
| `/auth/register` | GET/POST | 不要 | 新規登録 |
| `/auth/login` | GET/POST | 不要 | ログイン |
| `/auth/logout` | GET | 必要 | ログアウト |

ログインが必要なページを開くと、ログインページに移動します（`login_manager.login_view`）。

---

## どの章の内容か

| 使っているもの | 場所 | 章 |
|---|---|---|
| `@memos_bp.route()`・`<int:memo_id>`・`abort(404)`・`render_template()` | `memos/views.py` | [04_flask_basic](../04_flask_basic/) |
| `redirect()`・`url_for()` | `memos/views.py`・`auth/views.py` | [05_redirect](../05_redirect/) |
| `{% extends %}`・`{% block %}`・`{% for %}`・`{% if %}`・`include`・`self.title()`・`request.endpoint` | `templates/` | [06_jinja2](../06_jinja2/) |
| `os.path.join()`・`with open()`で`memos.json`を読む | `app.py` | [07_with](../07_with/) |
| `request.args.get('category')`・`methods=['GET', 'POST']`・`request.method`・`request.referrer` | `memos/views.py` | [08_request](../08_request/) |
| `FlaskForm`・`validate_on_submit()`・`form.csrf_token`・`flash()` | `forms.py`・`templates/` | [09_forms](../09_forms/) |
| `db.Model`・`Memo.query.filter_by()`・`order_by()`・`db.session.add()` / `delete()` / `commit()` | `models.py`・`memos/views.py` | [13_flask_sqlalchemy](../13_flask_sqlalchemy/) |
| `Migrate(app, db)`・`flask db upgrade` | `app.py`・`migrations/` | [14_flask_migrate](../14_flask_migrate/) |
| `LoginManager`・`UserMixin`・`@login_required`・`login_user()`・`current_user`・パスワードのハッシュ化 | `app.py`・`models.py`・`auth/views.py` | [15_login](../15_login/) |
| 型ヒント（`-> str \| Response`・`Optional[User]`） | `*.py` | [16_typehints](../16_typehints/) |
| `Blueprint`・`app.register_blueprint()`・`db.init_app(app)` | `app.py`・`auth/views.py`・`memos/views.py` | [17_blueprint](../17_blueprint/) |

削除・ピン留めのボタンは、入力欄の無い小さなフォーム（`ActionForm`）です。POSTで送るフォームにはCSRFトークンが必要なので（09_forms）、入力欄が無くても`FlaskForm`を使い、テンプレートで`{{ action_form.csrf_token }}`を出力しています。

---

## フロントエンド編から取り入れた項目

記号は、`style.css`・`script.js`・テンプレートのコメントに書いてある記号と同じです。

### HTML・テンプレート

| # | 項目 | 使っている場所 | 学ぶ章 |
|---|---|---|---|
| H1 | メモのカードと詳細を`article`に、期限を`<time datetime>`に、詳細の項目を`dl`に | `memos/index.html`・`detail.html` | [01_frontend/02_html_semantic_form](../../01_frontend/02_html_semantic_form/) 1節・[01_html_basics](../../01_frontend/01_html_basics/) 2節 |
| H2 | ナビの今いるページのリンクに`aria-current="page"`（`request.endpoint`で判定） | `base.html` | 01_frontend/02_html_semantic_form 制作課題・06_jinja2 3-6 |
| H3 | 絞り込みボタン・ピン留めボタンの状態を`aria-pressed`で伝える | `memos/index.html` | [01_frontend/08_js_render](../../01_frontend/08_js_render/) 練習問題3 |
| H4 | リンクの文字を「こちら」にしない。`autocomplete`・`required`などの属性 | `auth/login.html`・`register.html`・`memos/_form.html` | 01_frontend/02_html_semantic_form 1・2節 |
| H5 | ページごとの`<meta name="description">`・ファビコン・OGP（`self.title()`でタイトルを2回使う） | `base.html`・各テンプレートの`block description`・`static/favicon.svg` | 01_frontend/01_html_basics 1節・[11_homepage](../../01_frontend/11_homepage/) 1節・06_jinja2 3-5 |
| H6 | 追加・編集のフォームを`_form.html`にまとめて`include`する | `memos/_form.html`・`create.html`・`update.html` | 06_jinja2 3-4 |

### CSS

| # | 項目 | 学ぶ章 |
|---|---|---|
| C1 | `box-sizing: border-box`を全体のリセットにする | [01_frontend/03_css_basics](../../01_frontend/03_css_basics/) 4節 |
| C2 | キーボード操作のときだけ枠を出す`:focus-visible` | 01_frontend/03_css_basics 2節・11_homepage 最終チェックリスト |
| C3 | モバイルファースト（`min-width`で広い画面用を足す）。ナビの並びは`grid-template-areas`で切り替え、カードの列数は`auto-fill`＋`minmax()`で自動 | [01_frontend/04_css_layout](../../01_frontend/04_css_layout/) 2・4節・練習問題3 |
| C4 | ダークモード。OSの設定に従い、ボタン（◐）でも切り替えられる（`data-theme`） | 01_frontend/04_css_layout 5節・[10_js_data](../../01_frontend/10_js_data/) 4節「応用」 |
| C5 | カードの`:hover`で浮き上がる`transition`。「動きを減らす」設定の人には止める | 01_frontend/04_css_layout 5節 |
| C6 | ヘッダーを`position: sticky`で上に固定し、スクロールしたら影を付ける | 01_frontend/04_css_layout 3節・[09_js_ui](../../01_frontend/09_js_ui/) 5節 |
| C7 | フォームの`:focus`の輪と、`:user-invalid`の赤枠 | 01_frontend/04_css_layout 練習問題4 |

### JavaScript

| # | 項目 | 学ぶ章 |
|---|---|---|
| J2 | `flash()`のメッセージを、右下に出て3秒で消える通知（`popover="manual"`・`role="status"`）で表示する。JavaScriptが動かないときは、ふつうの一覧として表示される | 01_frontend/09_js_ui 2節 |
| J3 | 削除の確認を`<dialog>`のモーダルにする（送信を止めてダイアログを開き、OKで`フォーム.submit()`） | 01_frontend/09_js_ui 3節「確認してから送信する」 |
| J4 | 一覧を、カテゴリとキーワードの両方で絞り込む。件数と0件のメッセージも出す | 01_frontend/08_js_render 3節・練習問題3 |
| J5 | 選んだカテゴリと配色を`localStorage`に覚える（使えない環境に備えて`try`/`catch`で囲む） | 01_frontend/10_js_data 4節・練習問題3 |
| J6 | メモ追加フォームの入力を`localStorage`に下書き保存し、開き直したときに復元する | 01_frontend/10_js_data 4節（サンプル03） |
| J7 | 送信前に、タイトルと本文の入力をJavaScriptでもチェックする | 01_frontend/06_js_events 練習問題2 |
| J8 | 「トップへ戻る」ボタンと、カードが画面に入ったらふわっと表示する動き（`IntersectionObserver`） | 01_frontend/09_js_ui 5節 |

**JavaScriptのチェックだけに頼らない**：J7の入力チェックは、ブラウザの開発者ツールで無効にできます。データを守るのはサーバー側（WTForms）のチェックで、JavaScriptのチェックは「送信する前に気づける」ための補助です（[09_forms](../09_forms/)）。

---

## 動作確認

| 確認する操作 | 確認したいこと |
|---|---|
| ログインせずに一覧・詳細を開く | メモは見られるが、★・編集・削除のボタンは表示されない |
| ログインせずに`/memos/new`を開く | ログインページに移動し、「ログインしてください。」と通知が出る |
| 登録してログインする | 右下に「ようこそ、◯◯ さん！」と通知が出て、3秒で消える |
| 一覧で「仕事」を押してから、検索欄に文字を入れる | 両方の条件に合うメモだけが残り、「◯件中 ◯件を表示」が変わる。0件なら「該当するメモはありません」 |
| 「仕事」を選んだままリロードする | 「仕事」が選ばれた状態で開く（J5） |
| `/memos/?category=仕事`を開く | サーバー側で絞り込まれ、仕事のメモだけがHTMLに含まれている（ページのソースで確認） |
| ☆を押す | ページが読み込み直され、★に変わってピン留めのメモの中に移動する。「ピン留めしました。」の通知が出る |
| 「削除」を押す | 暗い背景の確認ダイアログが出る。キャンセル・Esc・背景のクリックでは削除されない。OKなら削除され、一覧に戻る |
| 「メモを追加」で何も入力せずに「保存する」を押す | 送信されず、欄の下にエラーが出て、タイトル欄に移動する |
| 「メモを追加」で途中まで入力し、別のページに移ってから戻る | 入力した内容が復元され、「下書きを復元しました」と表示される |
| 詳細ページで「編集」を押し、タイトルを変えて保存する | 詳細ページに戻り、タイトルが変わっている |
| `/memos/999`を開く | 404になる |
| ◐を押してからリロードする | 選んだ配色のまま開く |
| デバイスツールバーで幅375pxにする | ハンバーガーメニュー（☰）になり、カードが1列になる |
| ページをクリックしてから`Tab`キーで移動する | フォーカスしているリンク・ボタンに橙色の枠が出る |

---

## 発展課題：編集・削除・ピン留めを自分で作る

04〜17章の練習問題で作ったのは、メモの「一覧・詳細・追加」と「ログイン」までです。このアプリにある**編集・削除・ピン留め**は、各章の練習問題では作っていません。どれも01〜17章で学んだ書き方の組み合わせで作れるので、17章を終えたら、自分の手で追加してみましょう。

### 出発点

[17_blueprint/challenge/answer](../17_blueprint/challenge/answer/)をフォルダごとコピーして使います（[00_my_app](../00_my_app/)で育ててきた自分のアプリに追加してもかまいません）。17章の解答では、メモのルートは`application/memos/views.py`（Blueprint名`memos`）、テンプレートは`templates/`にあります。

```bash
cd コピーしたフォルダ
flask --app app db init
flask --app app db migrate -m "create memos and users tables"
flask --app app db upgrade
python app.py   # http://127.0.0.1:5052/ で、17章と同じ画面が開くことを確認する
```

3つの機能は、どれもログインした人だけが使えるようにします（`@login_required`、テンプレートでは`{% if current_user.is_authenticated %}`でボタンを出し分ける）。

### 課題1：編集

登録済みのメモのタイトル・カテゴリ・本文・期限を書き換えられるようにします。

| エンドポイント | メソッド | 処理 |
|---|---|---|
| `/memos/<int:memo_id>/edit` | GET | 今の内容を入れたフォーム（`edit_memo.html`）を表示する |
| `/memos/<int:memo_id>/edit` | POST（チェック成功） | メモを書き換えて保存し、flash「メモを更新しました。」とともに詳細ページへリダイレクトする |
| `/memos/<int:memo_id>/edit` | POST（チェック失敗） | エラーメッセージ付きでフォームを再表示する |
| 存在しないIDのとき | — | `abort(404)`で404にする |

**ヒント**

- フォームは追加と同じ`MemoForm`を使う。`edit_memo.html`は`new_memo.html`をコピーして、見出しとタイトルを「メモを編集」に変えればよい（共通部分を`include`でまとめると、このアプリの`memos/_form.html`と同じ形になる：[06_jinja2](../06_jinja2/) 3-4）
- 初めて開いたとき（`request.method == 'GET'`）だけ、`form.title.data = memo.title`のように今の内容をフォームに入れる。POSTのときにも入れてしまうと、入力した内容が元に戻ってしまう（[08_request](../08_request/)）
- 取り出した`memo`の属性を書き換えて`db.session.commit()`すれば更新される。`db.session.add()`は要らない（[13_flask_sqlalchemy](../13_flask_sqlalchemy/) 5節）
- 期限を空欄にしたときは`form.due_date.data or None`で`None`にしておくと、詳細ページの「期限」欄が消える
- 一覧のカードと詳細ページに「編集」リンク（`url_for('memos.edit_memo', memo_id=memo.id)`）を置く。17章の`memo_detail()`はテンプレートに`title`などしか渡していないので、`memo=memo`も渡すようにする（メモが無いときは`None`になるので、テンプレートでは`{% if memo and current_user.is_authenticated %}`で囲む）

### 課題2：削除

メモをデータベースから消せるようにします。

| エンドポイント | メソッド | 処理 |
|---|---|---|
| `/memos/<int:memo_id>/delete` | POST | メモを削除し、flash「メモを削除しました。」とともに一覧へリダイレクトする |

**ヒント**

- 削除は**POSTだけ**で受け付ける。GETのリンクで消せるようにすると、URLを開いただけ（リンクの先読みなど）で消えてしまう
- POSTで送るフォームにはCSRFトークンが必要（[09_forms](../09_forms/) 4節）。入力欄の無い`ActionForm(FlaskForm)`（`submit`だけを持つ）を`forms.py`に作り、ビューで`ActionForm().validate_on_submit()`が`True`のときだけ削除する。テンプレートには`{{ action_form.csrf_token }}`を出すので、一覧と詳細のビューから`action_form=ActionForm()`を渡す
- 削除は`db.session.delete(memo)` → `db.session.commit()`（13_flask_sqlalchemy 5節）
- 削除ボタンのフォームに`data-confirm="「{{ memo.title }}」を削除しますか？"`を付けると、`static/script.js`（完成済み）が送信の前に確認ダイアログを出してくれる。Python側は何もしなくてよい

### 課題3：ピン留め

大事なメモを一覧の先頭に固定できるようにします。データベースに新しいカラムが必要なので、マイグレーションから始めます。

| 内容 | 処理 |
|---|---|
| `Memo`モデル | `is_pinned`（真偽値。既定は`False`）カラムを追加し、マイグレーションで既存のテーブルに反映する |
| `/memos/<int:memo_id>/pin`（POST） | `is_pinned`を反転して保存し、flash「ピン留めしました。」／「ピン留めを外しました。」を出して、**押したページ**（一覧または詳細）に戻る |
| 一覧の並び順 | ピン留めしたメモを先頭に、それ以外は新しい順（`02_memo_app_frontend`の`sortMemos()`と同じ） |
| 表示 | 一覧のカード左上に☆／★のボタン、詳細ページに「ピン留めする／外す」ボタン |

```bash
# is_pinned をモデルに追加したら
flask --app app db migrate -m "add is_pinned column"
flask --app app db upgrade
```

**ヒント**

- カラムは`db.Column(db.Boolean, nullable=False, default=False, server_default='0')`のように書く。`server_default`が無いと、すでに行がある`memos`テーブルへの追加が`Cannot add a NOT NULL column with default value NULL`で失敗する（既存の5件に入れる値が決まらないため。`default`はPythonから追加するときだけの既定値で、データベースには伝わらない）。[14_flask_migrate](../14_flask_migrate/)で`due_date`を追加したときは`nullable=True`だったので、この問題は起きなかった
- 反転は`memo.is_pinned = not memo.is_pinned`。CSRFの確認は課題2の`ActionForm`をそのまま使う
- 押したページに戻るには`redirect(request.referrer or url_for('memos.memo_list'))`。`request.referrer`は、このリクエストを送ったページのURL（無いときは`None`）
- 並び順は`query.order_by(Memo.is_pinned.desc(), Memo.id.desc())`（[12_sqlalchemy](../12_sqlalchemy/) 2節の`order_by`）
- ☆／★のボタンは、このアプリの`templates/memos/index.html`の`pin-form`と同じ形にすると、`static/style.css`のスタイルがそのまま当たる

### 動作確認

| 確認する操作 | 確認したいこと |
|---|---|
| ログインせずに一覧・詳細を開く | ☆・編集・削除のボタンが表示されない |
| ログインせずに`/memos/1/edit`を開く | ログインページに移動する |
| ログインして、詳細ページで「編集」を押し、タイトルを変えて保存する | 詳細ページに戻り、タイトルが変わっていて「メモを更新しました。」の通知が出る |
| 編集で本文を空にして保存する | フォームが再表示され、エラーが出る。メモは変わっていない |
| `/memos/999/edit`を開く | 404になる |
| 一覧で「削除」を押してキャンセルする／OKを押す | キャンセルでは消えない。OKで消えて一覧に戻り、「メモを削除しました。」の通知が出る |
| 一番古いメモの☆を押す | ★に変わって一覧の先頭に移動し、「ピン留めしました。」の通知が出る |
| 詳細ページで「ピン留めを外す」を押す | 一覧ではなく、同じ詳細ページに戻る |
| `flask db upgrade`のあとに`sqlite3 memos.db "SELECT id, title, is_pinned FROM memos;"`を実行する | 既存のメモが消えずに残り、`is_pinned`が`0`になっている |

**解答例**：このアプリ（100_memo_api）のコードが解答例です。編集は`memos/views.py`の`update()`と`templates/memos/update.html`・`_form.html`、削除は`delete()`、ピン留めは`toggle_pin()`と`models.py`の`is_pinned`を見てください。100ではBlueprintに`url_prefix='/memos'`を付けていて関数名も違う（一覧は`index()`、エンドポイントは`memos.index`）ので、17章の名前に読み替えて比べます。
