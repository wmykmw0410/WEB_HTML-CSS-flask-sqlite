# VSCodeのおすすめ拡張機能

このカリキュラムを進める上で役立つVSCode拡張機能と、それぞれの基本的な使い方をまとめます。拡張機能は左端のアイコンバーの四角が4つ並んだアイコン（Extensions）から検索してインストールします。

## 目次

- [Python開発](#python開発)
- [HTML/CSS/フロントエンド](#htmlcssフロントエンド)
- [データベース確認](#データベース確認)
- [JSON APIの動作確認](#json-apiの動作確認)
- [Docker](#docker)
- [Git操作](#git操作)
- [日本語化](#日本語化)

---

## Python開発

### Python（Microsoft）

Python開発の基本になる拡張機能です。インストールすると自動的に**Pylance**（後述）も一緒に入ります。

- **インストール**: マーケットプレイスで`Python`を検索（発行元: Microsoft）
- **使い方**:
  - ファイル右下、またはコマンドパレット（`Cmd+Shift+P` / `Ctrl+Shift+P`）から`Python: Select Interpreter`を実行し、使うPythonのバージョンを選ぶ
  - `.py`ファイルを開くと自動で構文ハイライト・補完が効くようになる
  - エディタ右上の▷ボタン、またはターミナルで`python app.py`を実行してデバッグ実行もできる（左端の「実行とデバッグ」アイコンから`F5`でブレークポイントを使ったステップ実行も可能）

### Pylance（Microsoft）

Python拡張機能に同梱される、型チェック・補完機能です。`016_typehints`以降、このカリキュラムのコードには型ヒント（`Optional`・`Union`など）が多く登場するため、恩恵を受けやすくなっています。

- **使い方**: 変数や関数にカーソルを合わせると、推論された型がポップアップで表示される。関数の引数と違う型の値を渡すと波線で警告してくれる

---

## HTML/CSS/フロントエンド

### Live Server（Ritwick Dey）

`.html`ファイルを保存するたびに自動でブラウザをリロードしてくれる拡張機能です。`002_html_css`のようにFlaskを使わず`.html`を直接開いて確認する場面で便利です。

- **使い方**: `.html`ファイルをエディタで開いた状態で右クリック →`Open with Live Server`。ブラウザが自動で開き、以後ファイルを保存するたびに自動更新される

### Jinja（wholroyd）

Flaskのテンプレート（`{% %}`・`{{ }}`）にシンタックスハイライトを効かせる拡張機能です。`.html`の中にJinja2構文が混ざっていても見やすくなります（`006_jinja2`以降で使うテンプレートファイル全般）。

- **使い方**: インストールするだけで、`templates/`以下の`.html`ファイルを開くと自動的にJinja構文がハイライトされる

---

## データベース確認

### SQLite Viewer（Florian Klampfer など）

`.sqlite`ファイルの中身をGUIで確認できる拡張機能です。`010_sql`・`011_sqlite`以降、各チャプターで生成される`instance/*.sqlite`の中身をSQLを書かずに見たいときに便利です。

- **使い方**: サイドバーのエクスプローラーで`.sqlite`ファイルをクリックすると、テーブル一覧とデータがGUIで表示される（`flask db upgrade`などでDBファイルを作成した後に確認するとよい）

---

## JSON APIの動作確認

### Thunder Client（Ranga Vadhineni）

VSCode内でHTTPリクエストを送信できる拡張機能です。`curl`コマンドの代わりに使えます。`021_webapi`・`022_flask_api`・`023_crud_api`のようにJSON APIを作るチャプターで、POST/PUT/DELETEのリクエストをGUIで組み立てて試せます。

- **使い方**:
  1. 左端のアイコンバーの雷マークから`Thunder Client`を開く
  2. `New Request`でメソッド（GET/POST/PUTなど）とURL（例: `http://127.0.0.1:5082/api/memos`）を指定する
  3. `Body`タブで`JSON`を選び、`{"title": "テスト", "category": "仕事", "body": "本文"}`のように送信データを書く
  4. `Send`を押すとレスポンス（ステータスコード・JSON）が下に表示される
  5. ログインが必要なAPI（`023_crud_api`以降）は、先に`/auth/login`にPOSTしてセッションCookieを取得する必要がある（Thunder ClientはCookieを自動で保持する）

---

## Docker

### Docker（Microsoft）

Dockerイメージ・コンテナをGUIで確認できる拡張機能です。[Dockerでのデプロイ](docker.md)で作った`100_memo_api`のコンテナを扱う際に便利です。

- **使い方**: 左端のアイコンバーのクジラアイコンから、ビルド済みイメージ・起動中のコンテナの一覧を確認できる。コンテナを右クリックして`View Logs`を選べば、`docker logs`コマンドを打たなくてもログをその場で確認できる

---

## Git操作

### GitLens（GitKraken）

Gitの変更履歴をエディタ上に表示する拡張機能です。[GitHubにリポジトリをpushする手順](github.md)で学ぶ`git`コマンドを、GUIでも確認・補完できます。

- **使い方**: コードの各行の右側に、その行を最後に変更したコミット情報が薄く表示される（`git blame`に相当）。サイドバーの「Source Control」アイコンから、コミット履歴やブランチの様子もグラフで確認できる

---

## 日本語化

### Japanese Language Pack for Visual Studio Code（Microsoft）

VSCode自体のメニュー・設定画面を日本語表示にする拡張機能です。

- **使い方**: インストール後、右下に表示される`Change Language and Restart`をクリックすると日本語UIに切り替わる（コマンドパレットから`Configure Display Language`でも変更可能）
