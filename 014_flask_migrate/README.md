# 014 Flask-Migrate

Flask-Migrate を使って、モデルの変更をコマンド一本で DB に反映する方法を学びます。

## 前提

- 013_flask_sqlalchemy を終えていること
- `flask-migrate` がインストール済みであること

```bash
pip install flask-migrate
```

## フォルダ構成

```
014_flask_migrate/
├── README.md
├── example/
│   ├── 01_basic.py        Flask-Migrate の基本セットアップ
│   └── 02_app/            実用アプリ（タスク管理）
│       ├── app.py
│       ├── static/style.css
│       └── templates/
│           ├── index.html
│           └── new_task.html
├── question/               練習問題
│   ├── question.py         問題
│   └── answer/
│       └── question.py     解答
└── challenge/              013_flask_sqlalchemyの続き（000_my_appに組み込む機能の変更分）
    ├── challenge.py
    ├── forms.py
    ├── memos.json
    ├── static/
    ├── templates/
    └── answer/
        ├── challenge.py
        ├── forms.py
        ├── memos.json
        ├── static/
        └── templates/
```

---

## Flask-Migrate とは

**Flask-Migrate** は Flask-SQLAlchemy のモデル変更を検出し、**マイグレーションファイル**として記録して DB に適用するライブラリです。内部では **Alembic** を使っています。

### なぜ必要か

009 の `db.create_all()` はテーブルが存在しないときに作るだけで、**既存テーブルへのカラム追加・変更には対応しません**。

```
db.create_all()   → テーブルがなければ作る。既存テーブルは変更しない
Flask-Migrate     → モデルとDBの差分を検出して変更を自動生成・適用できる
```

---

## 1. セットアップ

> [example/01_basic.py](example/01_basic.py)

```python
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy(app)
Migrate(app, db)   # この1行を追加するだけで flask db コマンドが使えるようになる
```

`Migrate(app, db)` を追加したら、`flask db` サブコマンドが有効になります。

---

## 2. マイグレーションの基本コマンド

### 手順（最初のテーブル作成）

```bash
# 1. migrations/ フォルダを初期化（プロジェクトで最初の1回だけ）
flask db init

# 2. モデルを元にマイグレーションファイルを生成
flask db migrate -m "create tasks table"

# 3. DB に適用（テーブルが作成される）
flask db upgrade
```

### コマンド一覧

| コマンド | 説明 |
|---|---|
| `flask db init` | `migrations/` フォルダを作成。最初の1回だけ実行 |
| `flask db migrate -m "説明"` | モデルの変更を検出してマイグレーションファイルを生成 |
| `flask db upgrade` | 未適用のマイグレーションを DB に適用 |
| `flask db downgrade` | 1つ前のバージョンに戻す |
| `flask db history` | マイグレーションの履歴を一覧表示 |
| `flask db current` | 現在適用されているバージョンを確認 |

### 動作確認：3つのコマンドを実行した後の状態

| 確認する操作 | 確認したいこと |
|---|---|
| `flask db init`実行後、フォルダを確認する | `migrations/`フォルダが新規作成され、`migrations/versions/`は空の状態 |
| `flask db migrate -m "create tasks table"`実行後 | `migrations/versions/`に1つマイグレーションファイル（`xxxx_create_tasks_table.py`）が生成される。**この時点ではまだDBに反映されていない** |
| `flask db upgrade`実行前に`.db`ファイルを確認する | `tasks`テーブルはまだ存在しない |
| `flask db upgrade`実行後 | `.db`ファイルに`tasks`テーブルが作成される。`flask db current`を実行すると、直前に生成したマイグレーションのリビジョンIDが表示される |

**正常な状態の見分け方**：`flask db migrate`は「変更点を記録するファイルを作るだけ」で、実際のDBはまだ変わりません。DBが実際に変わるのは`flask db upgrade`を実行した後です。この2段階を混同していないか、`migrate`だけ実行してテーブルが無いと勘違いしていないか確認してください。

---

## 3. マイグレーションファイルの中身

`flask db migrate` を実行すると `migrations/versions/` に以下のようなファイルが自動生成されます。

```python
# migrations/versions/xxxx_create_tasks_table.py

def upgrade():
    # DB を新しい状態に変更する処理（flask db upgrade で実行）
    op.create_table('tasks',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('content', sa.String(200), nullable=False),
    )

def downgrade():
    # DB を1つ前の状態に戻す処理（flask db downgrade で実行）
    op.drop_table('tasks')
```

- `upgrade()` — 新しいバージョンに進む処理
- `downgrade()` — 1つ前のバージョンに戻す処理
- **自動生成された内容を必ず確認してから適用する**（意図しない変更が含まれることがある）

---

## 4. カラムを追加する（ALTER TABLE 相当）

モデルにカラムを追加して再度 `flask db migrate` → `flask db upgrade` を実行するだけです。

```python
# モデルに is_completed を追加
class Task(db.Model):
    id           = db.Column(db.Integer, primary_key=True)
    content      = db.Column(db.String(200), nullable=False)
    is_completed = db.Column(db.Boolean, default=False)   # ← 追加
```

```bash
flask db migrate -m "add is_completed column"
flask db upgrade
```

生成されるマイグレーションファイル：

```python
def upgrade():
    with op.batch_alter_table('tasks') as batch_op:
        batch_op.add_column(sa.Column('is_completed', sa.Boolean(), nullable=True))

def downgrade():
    with op.batch_alter_table('tasks') as batch_op:
        batch_op.drop_column('is_completed')
```

> **SQLite の注意点**: SQLite は `ALTER TABLE` でのカラム変更が制限されているため、Flask-Migrate は `batch_alter_table` を使ってテーブルの再作成で対応します。

### 動作確認：既存データを保ったままカラムが追加されるか

| 確認する操作 | 確認したいこと |
|---|---|
| カラム追加前に何件かタスクを登録しておく | 例えば3件のタスクが存在する状態にする |
| `flask db migrate -m "add is_completed column"` → `flask db upgrade`を実行する | エラーなく完了する |
| `.db`ファイルの中身を確認する（`sqlite3`コマンドや拡張機能で） | **既存の3件のデータが消えずに残っており**、新しく追加された`is_completed`列には`NULL`（または`nullable=False`なら指定したデフォルト値）が入っている |

**正常な状態の見分け方**：カラム追加のマイグレーションは既存データを消しません。もし`nullable=False`なのにデフォルト値を指定していないカラムを追加しようとすると、既存行にどんな値を入れればいいか分からずマイグレーションがエラーになります。エラーが出た場合は`nullable=True`にするか`server_default`を指定してください。

---

## 5. 実用アプリ（タスク管理）

> [example/02_app/app.py](example/02_app/app.py)

Flask-Migrate を組み込んだタスク管理アプリです。

### 起動手順

```bash
cd 014_flask_migrate/example/02_app

# 初回のみ
flask db init
flask db migrate -m "init"
flask db upgrade

# アプリ起動
python app.py
```

### ルート一覧

| URL | メソッド | 説明 |
|---|---|---|
| `/` | GET | タスク一覧（未完了 / 完了済み） |
| `/new` | GET | タスク作成フォーム |
| `/new` | POST | タスクを DB に保存して一覧へリダイレクト |
| `/tasks/<id>/complete` | POST | タスクを完了にする |
| `/tasks/<id>/uncompleted` | POST | タスクを未完了に戻す |

### 動作確認：タスクの完了・未完了の切り替えが反映されるか

```bash
cd 014_flask_migrate/example/02_app
```

| 確認する操作 | 確認したいこと |
|---|---|
| `http://127.0.0.1:5038/new`からタスクを追加する | 一覧（`/`）の「未完了」に追加したタスクが表示される |
| 一覧でタスクの「完了」ボタンを押す | そのタスクが「未完了」の欄から消え、「完了済み」の欄に移動する |
| 「未完了に戻す」ボタンを押す | 「完了済み」から「未完了」に戻る |
| アプリを再起動する | 再起動前の完了/未完了の状態がそのまま保持されている（`.db`ファイルに保存されているため） |

**正常な状態の見分け方**：タスクが「未完了」と「完了済み」のどちらか一方にだけ表示され、両方に重複して表示されないことを確認してください。

---

## 6. 練習問題

> [question/question.py](question/question.py) — 問題 ｜ [question/answer/question.py](question/answer/question.py) — 解答

### 問題：メモアプリに Flask-Migrate を組み込もう

`question/question.py` を開き、コメントの指示に従ってコードを完成させてください（ステップ1のモデル定義とステップ2のINSERT/SELECT）。以下の手順で実装・実行してください。

```bash
cd 014_flask_migrate/question
flask --app question db init
flask --app question db migrate -m "create memos table"
flask --app question db upgrade
python question.py
```

#### ステップ

| ステップ | 内容 |
|---|---|
| 1 | `Memo` モデル（id / title / body）を定義して Flask-Migrate をセットアップする |
| 2 | `flask db init` → `flask db migrate` → `flask db upgrade` を実行してテーブルを作成する |
| 3 | `Memo` モデルに `created_at`（`db.String`）カラムを追加して再マイグレーションする |
| 4 | `flask db history` と `flask db current` でバージョンを確認する |

### 動作確認：マイグレーション履歴が積み重なっていくか

| 確認する操作 | 確認したいこと |
|---|---|
| ステップ2完了後に`flask --app question db current` | 最初のマイグレーション（テーブル作成）のリビジョンIDが表示される |
| ステップ3（`created_at`追加）完了後に`flask --app question db history` | マイグレーションが**2件**、新しい順に表示される（テーブル作成 → `created_at`追加） |
| ステップ3完了後に`flask --app question db current` | 2件のうち**新しい方**（`created_at`追加）のリビジョンIDに変わっている |

**正常な状態の見分け方**：`flask db history`に表示される件数は、これまでに`flask db migrate`を実行した回数と一致します。件数が増えていない場合は`flask db migrate`を実行し忘れて`flask db upgrade`だけ行っていないか確認してください（`upgrade`は既存のマイグレーションを適用するだけで、新しい変更を検出しません）。

---

## 7. 練習問題：メモデータの管理に Flask-Migrate を組み込もう

> [challenge/challenge.py](challenge/challenge.py) — 問題 ｜ [challenge/answer/challenge.py](challenge/answer/challenge.py) — 解答

### 問題：db.create_all() から Flask-Migrate に切り替えて due_date カラムを追加しよう

`013_flask_sqlalchemy`で作ったメモ一覧・詳細・メモ追加フォーム・リダイレクト（`challenge/challenge.py`にすでに実装済み）は、これまで`db.create_all()`でテーブルが無ければ作るだけでした。これを`Flask-Migrate`で管理する方式に変更し、既存の`memos`テーブルに`due_date`（期限）カラムを追加します。

この課題は`python challenge.py`だけでは完結せず、`flask db`コマンドを挟みながら進めます。

```bash
cd 014_flask_migrate/challenge

# 問題1：Migrate(app, db) を追加したら、まず既存のテーブルをマイグレーション管理下に置く
flask --app challenge db init
flask --app challenge db migrate -m "create memos table"
flask --app challenge db upgrade
python challenge.py   # これまで通り動くことを確認

# 問題2：Memo モデルに due_date カラムを追加したら、再度マイグレーション
flask --app challenge db migrate -m "add due_date column"
flask --app challenge db upgrade

# 問題3：ルートを due_date 対応にしたら、メモ追加フォームで動作確認
python challenge.py
```

#### 仕様

| 問題 | 内容 |
|---|---|
| 1 | `Migrate(app, db)` を追加してマイグレーションを有効にする（`db.create_all()`は使わない） |
| 2 | `Memo`モデルに`due_date`カラムを追加する（既存の5件のデータが壊れないよう`nullable`にする） |
| 3 | `/memos/<int:memo_id>`で`memo.due_date`から`due_date_line`を作り、`/memos/new`で`new.due_date = form.due_date.data`を設定する |

#### ヒント

- モデルへのカラム追加は`db.Column(db.String, nullable=True)`のように書く（本章セクション4）。`nullable`にしないと、既存の5件（due_dateを持たない行）へのマイグレーションが失敗する
- `flask db migrate`を実行すると`memos.due_date`カラムの追加が自動検出される（セクション3・4）
- `due_date_line`は`memo.due_date`が未設定（`None`）のときに空文字にしておくと、テンプレート側の`{% if due_date_line %}`で表示を切り替えられる
- フォーム（`forms.py`）とテンプレート（`new_memo.html`・`detail.html`）の`due_date`対応はすでに用意されているので、Pythonコードのみ変更すればよい。`forms.py`の`due_date`フィールドには`wtforms.validators`の`Optional()`（入力必須にしない）が使われている。`016_typehints`で学ぶ`typing.Optional`とは**別物**（こちらはWTFormsのバリデーター）なので注意
- 見た目やCSRFの仕組みは`013_flask_sqlalchemy`から変更不要

### 動作確認：db.create_all()からの移行後も既存メモが壊れていないか

```bash
cd 014_flask_migrate/challenge
python challenge.py
```

| 確認する操作 | 確認したいこと |
|---|---|
| 問題1の`flask db upgrade`実行後に`http://127.0.0.1:5039/`にアクセスする | `013_flask_sqlalchemy`から引き継いだ既存の5件のメモが、これまで通り表示される |
| 問題2の`flask db migrate -m "add due_date column"` → `upgrade`実行後 | エラーなく完了する（`nullable=True`にしていれば、既存5件に`due_date`が無くてもマイグレーションが失敗しない） |
| 問題3完了後、既存メモ（`due_date`未設定）の詳細ページを見る | エラーにならず、期限の表示欄が空になっている（`due_date_line`が空文字になる分岐が効いている） |
| 問題3完了後、`/memos/new`で期限を指定して新しいメモを追加する | 詳細ページに指定した期限が表示される |

**正常な状態の見分け方**：カラム追加の前後で、既存のメモ（元々あった5件）が消えたり内容が変わったりしていないことが最も重要な確認ポイントです。既存メモの詳細ページでエラーになる場合は、`nullable`の指定漏れか、`due_date`が`None`のケースを考慮していないテンプレート分岐を疑ってください。
