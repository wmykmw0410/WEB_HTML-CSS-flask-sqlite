# 013 Flask-SQLAlchemy

Flask に SQLAlchemy を統合した **Flask-SQLAlchemy** を使います。
012_sqlalchemy で学んだ ORM の知識を前提に、Flask アプリから DB を操作する方法を学びます。

## 前提

- 012_sqlalchemy を終えていること
- 007_with を終えていること（`with` 文の基礎）
- `flask-sqlalchemy` がインストール済みであること

```bash
pip install flask-sqlalchemy
```

## フォルダ構成

```
013_flask_sqlalchemy/
├── README.md
├── example/
│   └── 01_basic.py            基本 CRUD（db.Model / db.session / app_context）
├── question/                  練習問題（1問1ファイル）
│   ├── question01.py〜question06.py
│   └── answer/
│       └── answer01.py〜answer06.py
└── challenge/                 012_sqlalchemyの続き（000_my_appに組み込む機能の変更分）
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

## 012 SQLAlchemy との違い

| 比較 | 012 生 SQLAlchemy | 013 Flask-SQLAlchemy |
|---|---|---|
| モデル基底クラス | `Base = declarative_base()` | `db.Model` |
| カラム定義 | `Column(Integer, ...)` | `db.Column(db.Integer, ...)` |
| テーブル作成 | `Base.metadata.create_all(engine)` | `db.create_all()` |
| セッション | `session = Session()` | `db.session` |
| 取得 | `session.query(Model).all()` | `Model.query.all()` |
| コンテキスト | 不要 | `with app.app_context():` 必須 |

---

## 1. セットアップ

> [example/01_basic.py](example/01_basic.py)

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']     = 'sqlite:///data.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
```

### 設定項目

| キー | 説明 |
|---|---|
| `SQLALCHEMY_DATABASE_URI` | 接続先 DB の URL。SQLite の場合 `sqlite:///ファイル名` |
| `SQLALCHEMY_TRACK_MODIFICATIONS` | 変更追跡（不要なので `False` に設定） |

### `SQLAlchemy(app)` と `db.init_app(app)` の違い

このチャプターでは `db = SQLAlchemy(app)` のように、`app` を作った直後に `db` を結びつけています。ファイルが1つで完結する学習用スクリプトではこれで十分ですが、ファイルを分割する実務のアプリ（`017_blueprint`のchallenge以降で登場）では、もう一つの書き方が使われます。

```python
# db.init_app(app) パターン（017_blueprint以降で使用）

# models.py（app を一切知らない）
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()          # ← app無しで作れる

class Task(db.Model):
    ...
```

```python
# app.py（あとから結びつける）
from flask import Flask
from models import db      # db だけをimportすればよい

app = Flask(__name__)
db.init_app(app)           # ← ここで結びつける
```

| | `db = SQLAlchemy(app)` | `db.init_app(app)` |
|---|---|---|
| `db`を作るタイミング | `app`と同時 | `app`より先に作れる |
| ファイル分割時の依存関係 | `models.py`が`app.py`の`app`をimportする必要が出やすく、循環importになりやすい | `models.py`は`app`を知らなくてよいので循環importが起きない |
| 向いている場面 | 1ファイルで完結する学習用スクリプト（このチャプターの`01_basic.py`など） | `models.py`/`app.py`を分けた実務のアプリ（`017_blueprint`のchallenge・`018_ownership_crud`など） |

**なぜ循環importが問題になるか**：`models.py`が`from app import app`をすると、`app.py`側も`from models import db`をしたい場合に「お互いが起動時にお互いを読み込もうとして失敗する」状態になります。`db.init_app(app)`パターンなら`models.py`は`app`について何も知らないため、この問題が起きません。

このチャプターでは学習のしやすさを優先して`SQLAlchemy(app)`を使いますが、`017_blueprint`のようにファイルを分割するタイミングで`db.init_app(app)`に切り替わることを覚えておいてください。

---

## 2. with 文と app_context

### with 文とは

Python の `with` 文は、**ブロックに入るときの前処理**と**ブロックを抜けるときの後処理**を自動化する仕組みです。

```python
# ファイル操作で馴染みのある例
with open('data.txt', 'w') as f:
    f.write('hello')
# ← ここで f.close() が自動で呼ばれる。例外が起きても必ず閉じる

# as を省略することもできる（変数が不要なとき）
with open('data.txt'):
    pass
```

| | `with` を使わない場合 | `with` を使う場合 |
|---|---|---|
| 後処理 | 自分で `f.close()` を呼ぶ | 自動で呼ばれる |
| 例外が起きたとき | close し忘れる可能性がある | それでも必ず後処理される |

### app_context とは

Flask は内部に**アプリケーションコンテキスト**という状態を持っています。
`db.session` や `current_app` などは、このコンテキストが存在しないと使えません。

```
Flask のリクエスト処理中：コンテキストが自動で作られる
スクリプトとして単独実行するとき：自分でコンテキストを作る必要がある
```

```python
# コンテキストがない状態で db を操作するとエラーになる
tasks = Task.query.all()
# RuntimeError: No application found.

# with app.app_context(): でコンテキストを作ってから操作する
with app.app_context():
    tasks = Task.query.all()   # OK
# ← ブロックを抜けるとコンテキストが自動でクリーンアップされる
```

### @app.route の中では不要

Flask のルート関数はリクエストを受けたときに Flask が自動でコンテキストを作るため、
`with app.app_context():` を書く必要はありません。

```python
@app.route('/tasks')
def task_list():
    tasks = Task.query.all()   # コンテキストは自動で作られている
    return str(tasks)

# スクリプト（if __name__ == '__main__' など）では必要
if __name__ == '__main__':
    with app.app_context():
        db.create_all()        # ← これは必要
```

### まとめ

| 場面 | `with app.app_context():` |
|---|---|
| `@app.route` の中 | 不要（Flask が自動で用意する） |
| スクリプトから DB を操作するとき | 必要 |
| `if __name__ == '__main__':` の中 | 必要 |

### 練習問題

1. `with open('test.txt', 'w') as f:` で `'hello'` を書き込み、`with open('test.txt') as f:` で読み込んで表示してください（`with` 文の基本動作の確認）
2. `with app.app_context():` を使って `db.create_all()` でテーブルを作成してください
3. 1つの `with app.app_context():` ブロックの中で、INSERT → SELECT を続けて実行してください

### 動作確認：app_contextが無いと何が起きるかを実際に見る

| 確認する操作 | 確認したいこと |
|---|---|
| `if __name__ == '__main__':`ブロックの中で、`with app.app_context():`を**一時的にコメントアウト**して`Task.query.all()`を呼ぶ | `RuntimeError: Working outside of application context.`というエラーが発生する（確認後は必ず元に戻す） |
| `with app.app_context():`を戻して同じコードを実行する | エラーが出ず、正常にクエリ結果が返る |
| `@app.route('/tasks')`の中で`with app.app_context():`を**付けて**みる（本来不要） | エラーにはならない（Flaskがすでに用意しているコンテキストの中に、さらにネストしたコンテキストを作るだけで害はないが、冗長なので通常は書かない） |

**正常な状態の見分け方**：`RuntimeError`が出るのは「Flaskのリクエスト処理の外（スクリプト単体実行など）で`app_context`を用意し忘れている」ことを示す、分かりやすいシグナルです。このエラーを見たら、そのコードが`@app.route`の中かどうかをまず確認してください。

---

## 3. モデルの定義

```python
class Task(db.Model):
    __tablename__ = 'tasks'
    id      = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(200), nullable=False)

    def __str__(self):
        return f"Task(id={self.id}, content={self.content})"
```

`db.Model` を継承するだけで Engine / Base / Session を自動で管理してくれます。

---

## 4. テーブル作成

```python
with app.app_context():
    db.drop_all()    # 既存テーブルを削除
    db.create_all()  # モデルを元にテーブルを作成
```

Flask の外で DB を操作するには必ず `app.app_context()` が必要です。

---

## 5. CRUD

### Create

```python
with app.app_context():
    task = Task(content='買い物')
    db.session.add(task)
    db.session.commit()
    print(task)   # commit 後に id が確定する
```

### Read

```python
with app.app_context():
    tasks = Task.query.all()                    # 全件
    task  = Task.query.filter_by(id=1).first()  # 1件（id 指定）
    tasks = Task.query.order_by(Task.id).all()  # 並び替え
    task  = Task.query.get(1)                   # 主キー（id）で1件取得
```

| メソッド | 説明 |
|---|---|
| `.query.all()` | 全件を取得する |
| `.query.filter_by(条件).first()` | 条件に一致する最初の1件を取得（無ければ`None`） |
| `.query.order_by(カラム)` | 並び替え |
| `.query.get(主キー)` | **主キー（通常は`id`）**で1件取得する専用メソッド。`filter_by(id=...).first()`と同じ結果だが、主キー検索に特化していて短く書ける。該当データが無ければ`None` |

### Update

```python
with app.app_context():
    task = Task.query.filter_by(id=1).first()
    task.content = '（更新済み）'
    db.session.add(task)
    db.session.commit()
```

### Delete

```python
with app.app_context():
    task = Task.query.filter_by(id=1).first()
    db.session.delete(task)
    db.session.commit()
```

---

## 6. 練習問題

> [question/](question/) — 問題（1問1ファイル） ｜ [question/answer/](question/answer/) — 解答

### 問題：メモアプリの DB を作ろう

`question/questionN.py` を開き、コメントの指示に従ってコードを完成させてください。各ファイルは独立して実行できるように、必要なテーブル・データをファイル内で作り直してから処理を行う構成になっています。

```bash
python 013_flask_sqlalchemy/question/question01.py
```

#### テーブル仕様（Memo）

| カラム | 型 | 制約 |
|---|---|---|
| id | Integer | PK / autoincrement |
| title | String(100) | NOT NULL |
| body | String(500) | |

#### 問題一覧

| 問題 | 内容 | ポイント | 解答 |
|---|---|---|---|
| 1 | `Memo` モデルを `db.Model` で定義してテーブルを作成する | `with app.app_context():` | [question/answer/answer01.py](question/answer/answer01.py) |
| 2 | 3件の Memo を `db.session.add_all()` で追加する | `with app.app_context():` | [question/answer/answer02.py](question/answer/answer02.py) |
| 3 | `Memo.query.all()` で全件取得して表示する | `with app.app_context():` | [question/answer/answer03.py](question/answer/answer03.py) |
| 4 | id=1 の title を更新する | `with app.app_context():` | [question/answer/answer04.py](question/answer/answer04.py) |
| 5 | id=2 の Memo を削除する | `with app.app_context():` | [question/answer/answer05.py](question/answer/answer05.py) |
| 6 | 最終状態を全件表示する | `with app.app_context():` | [question/answer/answer06.py](question/answer/answer06.py) |

### 動作確認：各問題を実行した結果

| 問題 | 実行コマンド | 確認したいこと |
|---|---|---|
| 1 | `python question/question01.py` | エラーなく終了し、テーブルが作成される |
| 2 | `python question/question02.py` | 3件のMemoが追加される（`add_all()`は複数のオブジェクトをまとめて1回の`commit()`で保存できる） |
| 3 | `python question/question03.py` | 3件のMemoが表示される |
| 4 | `python question/question04.py` | 更新後、`id=1`の`title`が変わっている |
| 5 | `python question/question05.py` | `id=2`のMemoが削除され、残りは2件になる |
| 6 | `python question/question06.py` | 削除後の最終状態（2件）が表示される |

**正常な状態の見分け方**：どの問題も`with app.app_context():`の外でDB操作をすると`RuntimeError`になります（本章セクション2）。エラーが出た場合はまずインデントの範囲を確認してください。

---

## 7. 練習問題：メモデータをFlask-SQLAlchemyに移行しよう

> [challenge/challenge.py](challenge/challenge.py) — 問題 ｜ [challenge/answer/challenge.py](challenge/answer/challenge.py) — 解答

### 問題：メモデータの保存先を SQLAlchemy（生）から Flask-SQLAlchemy に変更しよう

`012_sqlalchemy`で作ったメモ一覧・詳細・メモ追加フォーム・リダイレクト（`challenge/challenge.py`にすでに実装済み）は、これまで自分で`engine`・`Session`を管理する生のSQLAlchemyで`memos.db`を操作していました。これを`Flask-SQLAlchemy`（`db.Model`・`db.session`・`app_context`）に置き換えます。

`Memo`モデルの定義（問題1）はすでに`db = SQLAlchemy(app)`の準備と合わせて用意されていますが、モデルのカラム定義と`db.create_all()`の呼び出しは`TODO`のままになっているので、まずこれを実装してください。`memos.json`は初回起動時にだけ`memos`テーブルへ投入するために使われます。

```bash
python 013_flask_sqlalchemy/challenge/challenge.py
```

#### 仕様

| エンドポイント | メソッド | 処理 |
|---|---|---|
| `/` | GET | `Memo.query`で全件取得する（`category`指定時は`filter_by(category=category)`で絞り込み） |
| `/memos/<int:memo_id>` | GET | `filter_by(id=memo_id).first()`で1件取得する |
| `/memos/new` | POST（バリデーション成功時） | `Memo(...)`を作って`db.session.add()`→`db.session.commit()`する |

#### ヒント

- モデル定義は`id`（主キー・自動採番）、`title`・`category`・`body`（すべて`NOT NULL`）の4カラム（`012_sqlalchemy`と同じ、本章セクション3）
- `init_db()`のようにスクリプト側からDBを操作する場合は`with app.app_context():`が必要（本章セクション2）。一方`@app.route`の中はFlaskが自動でコンテキストを用意するので不要（セクション2・4）
- `Memo.query.filter_by(...).all()` / `.first()`で結果を取得する（セクション5）
- 見た目やCSRFの仕組みは`012_sqlalchemy`から変更不要

### 動作確認：生SQLAlchemyからFlask-SQLAlchemyに変わっても同じ見た目で動くか

```bash
cd 013_flask_sqlalchemy/challenge
python challenge.py
```

| 確認する操作 | 確認したいこと |
|---|---|
| `http://127.0.0.1:5036/`にアクセスする | `012_sqlalchemy`のときと見た目が変わらずメモ一覧が表示される（`engine`/`Session`を自分で管理する書き方から`db = SQLAlchemy(app)`に変わっただけ） |
| `?category=仕事`を付けてアクセスする | `Memo.query.filter_by(category='仕事')`で絞り込まれる |
| メモ詳細ページにアクセスする | `filter_by(id=memo_id).first()`で取得した1件が表示される |
| `/memos/new`から新しいメモを追加する | 追加後、一覧に反映される |

**正常な状態の見分け方**：`012_sqlalchemy`のときと画面の動作が変わらないのが正しい状態です。起動時に`RuntimeError`が出る場合は、`init_db()`など`@app.route`の外でDBを操作している箇所に`with app.app_context():`が付いているか確認してください（本章セクション2）。
