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
    ├── books.json
    ├── static/
    ├── templates/
    └── answer/
        ├── challenge.py
        ├── forms.py
        ├── books.json
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

---

## 7. 練習問題：書籍データの管理に Flask-Migrate を組み込もう

> [challenge/challenge.py](challenge/challenge.py) — 問題 ｜ [challenge/answer/challenge.py](challenge/answer/challenge.py) — 解答

### 問題：db.create_all() から Flask-Migrate に切り替えて genre カラムを追加しよう

`013_flask_sqlalchemy`で作った書籍一覧・詳細・書籍追加フォーム・リダイレクト（`challenge/challenge.py`にすでに実装済み）は、これまで`db.create_all()`でテーブルが無ければ作るだけでした。これを`Flask-Migrate`で管理する方式に変更し、既存の`books`テーブルに`genre`（ジャンル）カラムを追加します。

この課題は`python challenge.py`だけでは完結せず、`flask db`コマンドを挟みながら進めます。

```bash
cd 014_flask_migrate/challenge

# 問題1：Migrate(app, db) を追加したら、まず既存のテーブルをマイグレーション管理下に置く
flask --app challenge db init
flask --app challenge db migrate -m "create books table"
flask --app challenge db upgrade
python challenge.py   # これまで通り動くことを確認

# 問題2：Book モデルに genre カラムを追加したら、再度マイグレーション
flask --app challenge db migrate -m "add genre column"
flask --app challenge db upgrade

# 問題3：ルートを genre 対応にしたら、書籍追加フォームで動作確認
python challenge.py
```

#### 仕様

| 問題 | 内容 |
|---|---|
| 1 | `Migrate(app, db)` を追加してマイグレーションを有効にする（`db.create_all()`は使わない） |
| 2 | `Book`モデルに`genre`カラムを追加する（既存の5件のデータが壊れないよう`nullable`にする） |
| 3 | `/books/<int:book_id>`で`book.genre`から`genre_line`を作り、`/books/new`で`new.genre = form.genre.data`を設定する |

#### ヒント

- モデルへのカラム追加は`db.Column(db.String, nullable=True)`のように書く（本章セクション4）。`nullable`にしないと、既存の5件（genreを持たない行）へのマイグレーションが失敗する
- `flask db migrate`を実行すると`books.genre`カラムの追加が自動検出される（セクション3・4）
- `genre_line`は`book.genre`が未設定（`None`）のときに空文字にしておくと、テンプレート側の`{% if genre_line %}`で表示を切り替えられる
- フォーム（`forms.py`）とテンプレート（`new_book.html`・`detail.html`）の`genre`対応はすでに用意されているので、Pythonコードのみ変更すればよい。`forms.py`の`genre`フィールドには`wtforms.validators`の`Optional()`（入力必須にしない）が使われている。`016_typehints`で学ぶ`typing.Optional`とは**別物**（こちらはWTFormsのバリデーター）なので注意
- 見た目やCSRF・ファイルアップロードの仕組みは`013_flask_sqlalchemy`から変更不要
