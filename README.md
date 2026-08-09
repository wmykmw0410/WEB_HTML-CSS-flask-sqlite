# Flask学習カリキュラム

Flaskを基礎から学ぶための番号付きチャプター集です。各チャプターは1つのテーマを独立したサンプルで学ぶ構成になっています。

```
次回:

メモ:
```

---

## 進捗

### 完成形（最初に触ってみる）
- [ ] 100_bookstore_api — 統合アプリ

### 基礎
- [ ] 001_web_basic — Webサイトの仕組み
- [ ] 002_html_css — HTML/CSSの基礎
- [ ] 003_function — 関数の基本・デコレータ
  - [ ] ex01〜ex11
- [ ] 004_flask_basic — Hello World・ルーティング・render_template
- [ ] 005_redirect — redirect・url_for
- [ ] 006_jinja2 — Jinja2
- [ ] 007_with — with文・コンテキストマネージャー
- [ ] 008_request — request・HTTPメソッド

### データ処理とフォーム
- [ ] 009_forms — WTForms・Flask-WTF・CSRF
- [ ] 010_sql — SQL基礎（SQLite CLI）
- [ ] 011_sqlite — sqlite3モジュール
- [ ] 012_sqlalchemy — SQLAlchemy ORM
- [ ] 013_flask_sqlalchemy — Flask-SQLAlchemy
  - [ ] question01〜06
- [ ] 014_flask_migrate — Flask-Migrate

### 認証・構造化
- [ ] 015_login — Flask-Login
- [ ] 016_typehints — 型ヒント（Optional・Union）
- [ ] 017_blueprint — Blueprint・gオブジェクト
- [ ] 018_ownership_crud — 所有権とCRUDのフルセット

### 応用機能
- [ ] 019_cart — カート機能・注文確定
- [ ] 020_testing — pytest・test_client
- [ ] 021_webapi — requestsで外部APIを呼び出す
- [ ] 022_flask_api — jsonify・JSON API
- [ ] 023_crud_api — JSON APIのフルCRUD化
- [ ] 024_role_management — ロールベースの認可
- [ ] 025_async — 非同期処理（asyncio）
  - [ ] question01〜05

### 自分のアプリへの統合
- [ ] 000_my_app — 学んだ内容を積み上げる

---

## 進め方

1. まず[100_bookstore_api](100_bookstore_api/)を実行し、最終的にどんなアプリができあがるのかを体験する
2. `001`から順番にチャプターを進める
3. 各チャプターは`README.md`（学習内容）と`example/`（サンプルコード）で構成される
4. 学んだ内容は、[000_my_app](000_my_app/)という**自分だけの統合アプリ**に少しずつ積み上げていく（詳細は後述）

## 動作確認済みのライブラリバージョン

各チャプターの`pip install`では特にバージョンを指定していませんが、このカリキュラムは以下のバージョンで動作確認しています。インストール時にエラーが出る場合は、まずこのバージョンに合わせてみてください。

| パッケージ | バージョン |
|---|---|
| Flask | 2.3.3 |
| Flask-WTF | 1.2.2 |
| Flask-Login | 0.6.3 |
| Flask-SQLAlchemy | 3.0.3 |
| Flask-Migrate | 4.0.4 |
| SQLAlchemy | 2.0.48 |
| requests | 2.33.1 |
| httpx | 0.28.1 |

```bash
pip install Flask==2.3.3 Flask-WTF==1.2.2 Flask-Login==0.6.3 Flask-SQLAlchemy==3.0.3 Flask-Migrate==4.0.4 SQLAlchemy==2.0.48 requests==2.33.1 httpx==0.28.1
```

## チャプター一覧

| # | チャプター | 学ぶ内容 |
|---|---|---|
| 001 | [web_basic](001_web_basic/) | Webサイトの仕組み（HTTP・サーバの役割・MVTモデル・ネットワーク基礎）の座学イントロダクション |
| 002 | [html_css](002_html_css/) | HTML/CSSの基礎（タグ・ボックスモデル・Flexbox/Grid）。ブックストアのトップページを静的HTML/CSSで再現する |
| 003 | [function](003_function/) | Pythonの関数の基本（引数・戻り値・スコープ）・デコレータ・`@app.route()`の仕組み |
| 004 | [flask_basic](004_flask_basic/) | Hello World・ルーティング・動的URL・render_template・エラーハンドリング |
| 005 | [redirect](005_redirect/) | `redirect()`・`url_for()`（内部/外部リダイレクト・引数付きURL生成） |
| 006 | [jinja2](006_jinja2/) | Jinja2（変数展開・for/if・テンプレート継承・フィルター） |
| 007 | [with](007_with/) | with文・コンテキストマネージャー・ファイル操作・`os.path` |
| 008 | [request](008_request/) | `request`・HTTPメソッド（GET/POST/PUT/DELETE）・クエリパラメータでの絞り込み |
| 009 | [forms](009_forms/) | WTForms・Flask-WTF・CSRF・session・ファイルアップロード |
| 010 | [sql](010_sql/) | SQL基礎（SQLite CLI、Python/Flask不使用） |
| 011 | [sqlite](011_sqlite/) | Python標準の`sqlite3`モジュール |
| 012 | [sqlalchemy](012_sqlalchemy/) | SQLAlchemy ORM（素のSQLAlchemy） |
| 013 | [flask_sqlalchemy](013_flask_sqlalchemy/) | Flask-SQLAlchemy（`db.Model`・`db.session`） |
| 014 | [flask_migrate](014_flask_migrate/) | Flask-Migrate（`flask db`コマンドでのマイグレーション） |
| 015 | [login](015_login/) | Flask-Login・パスワードハッシュ化・ログイン機能 |
| 016 | [typehints](016_typehints/) | Python型ヒント（基本の型・`Optional`・`Union`） |
| 017 | [blueprint](017_blueprint/) | Blueprint・`g`オブジェクト |
| 018 | [ownership_crud](018_ownership_crud/) | ここまでの総合（書籍の所有権とCRUDのフルセット） |
| 019 | [cart](019_cart/) | セッションを使ったカート機能・注文確定（Order） |
| 020 | [testing](020_testing/) | 自動テスト（`pytest`・Flaskの`test_client`） |
| 021 | [webapi](021_webapi/) | `requests`で外部APIを呼び出す（クライアント側） |
| 022 | [flask_api](022_flask_api/) | `jsonify`・JSON API・地図表示 |
| 023 | [crud_api](023_crud_api/) | JSON APIのフルCRUD化（POST/PUT/DELETE・入力検証） |
| 024 | [role_management](024_role_management/) | ロールベースの認可（管理者/一般、is_admin） |
| 025 | [async](025_async/) | 非同期処理（`asyncio`・Flaskの`async`ビューとその限界） |

### 完成形（最初に触ってみる）

| # | チャプター | 学ぶ内容 |
|---|---|---|
| 100 | [bookstore_api](100_bookstore_api/) | `018`〜`024`の集大成（所有権・ロール管理・カート・フルCRUD APIを統合したブックストア） |

## 000_my_app について

学んだ内容を自分のアプリに積み上げていく専用チャプターです。使い方・進捗チェックリストは[000_my_app/README.md](000_my_app/)を参照してください。

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
