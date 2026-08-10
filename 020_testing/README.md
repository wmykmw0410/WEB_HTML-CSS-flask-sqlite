# 020 自動テスト（pytest）

これまでの章では、機能を作るたびにブラウザや`curl`で手動確認していました。このチャプターでは、その確認作業を**コードとして書いて自動化**する方法（`pytest`・Flaskの`test_client`）を学びます。

## 前提

| チャプター | 使う知識 |
|---|---|
| 015_login | Flask-Login・ログイン処理 |
| 018_ownership_crud | db.Model・所有権パターン |
| 019_javascript | fetch()で呼び出すJSON API（toggle-pin） |

```bash
pip install pytest
```

## フォルダ構成

```
020_testing/
├── README.md
├── example/
│   ├── test_01_pytest_basics.py   pytestの基本（assert・fixture・parametrize）
│   ├── 02_app.py                   テスト対象の最小Flaskアプリ
│   └── test_02_flask_client.py     Flaskのtest_clientの基本
└── challenge/                      019_javascriptの続き（テストを書く）
    ├── conftest.py                 フィクスチャ（app/client/sample_user/sample_memo）
    ├── test_memos.py
    ├── test_pin.py
    ├── pytest.ini
    ├── app.py / models.py / ...    019_javascriptと同じメモ帳アプリ本体
    └── answer/
        ├── conftest.py
        ├── test_memos.py
        ├── test_pin.py
        ├── pytest.ini
        └── app.py / models.py / ...
```

---

## 1. pytestの基本

> [example/test_01_pytest_basics.py](example/test_01_pytest_basics.py)

```python
def add(a: int, b: int) -> int:
    return a + b

def test_add():
    assert add(2, 3) == 5
```

| 要素 | 説明 |
|---|---|
| `test_`で始まる関数名 | pytestが自動的にテストとして認識する |
| `assert 条件` | 条件が`False`ならそのテストは`FAILED`になる |
| `pytest.raises(例外クラス)` | `with`ブロック内でその例外が発生することを確認する |

### フィクスチャ（fixture）

```python
@pytest.fixture
def sample_list() -> list[int]:
    return [3, 1, 4, 1, 5, 9]

def test_sample_list_length(sample_list):
    assert len(sample_list) == 6
```

テスト関数の**引数名**をフィクスチャ名と一致させると、そのフィクスチャの戻り値が自動的に渡ってきます。前処理（データ準備）を複数のテストで使い回すための仕組みです。

### parametrize — 同じテストを複数の入力で実行する

```python
@pytest.mark.parametrize('a, b, expected', [
    (1, 1, 2),
    (2, 3, 5),
    (-1, 1, 0),
])
def test_add_parametrized(a, b, expected):
    assert add(a, b) == expected
```

### 実行方法

```bash
pytest 020_testing/example/test_01_pytest_basics.py -v
```

`-v`（verbose）を付けると、実行したテスト関数名が1つずつ表示されます。

### 動作確認：PASSEDとFAILEDの違いを実際に見る

| 確認する操作 | 確認したいこと |
|---|---|
| そのまま実行する | `test_add`・`test_sample_list_length`・`test_add_parametrized[...]`が3パターン、合計5件前後すべて`PASSED`（緑）になる |
| `test_add`の中の`assert add(2, 3) == 5`を`assert add(2, 3) == 999`のように**わざと間違えて**実行する | そのテストだけ`FAILED`（赤）になり、`assert 5 == 999`のように実際の値と期待値の差分が表示される。確認後は必ず元に戻す |
| `parametrize`の引数リストに`(2, 2, 999)`のような間違ったデータを1つ追加する | そのパラメータの組み合わせだけ`FAILED`になり、他の組み合わせは影響を受けず`PASSED`のまま |

**正常な状態の見分け方**：意図的に間違えた箇所だけが`FAILED`になり、それ以外のテストは`PASSED`のままであれば、テストが互いに独立して正しく検証できている証拠です。1箇所直しただけで無関係なテストまで失敗する場合は、フィクスチャの共有状態を疑ってください（本章セクション2で詳しく扱います）。

---

## 2. Flaskのtest_client

> [example/02_app.py](example/02_app.py)（テスト対象） | [example/test_02_flask_client.py](example/test_02_flask_client.py)（テストコード）

`app.test_client()`を使うと、実際にサーバーを起動せずに、Flaskアプリへリクエストを送ってレスポンスを検証できます。

### @app.get() などのショートカットデコレータ

`example/02_app.py`のルートは`@app.route('/tasks', methods=['GET'])`ではなく`@app.get('/tasks')`のように書かれています。Flask 2.0以降は、HTTPメソッドごとに`@app.get`・`@app.post`・`@app.put`・`@app.delete`というショートカットデコレータが使え、`methods=[...]`を書かずに済みます。`@app.route(..., methods=['GET'])`と完全に同じ意味です。

```python
@app.get('/tasks')          # @app.route('/tasks', methods=['GET']) と同じ
def list_tasks():
    return jsonify(TASKS)
```

```python
@pytest.fixture
def client():
    app.config['TESTING'] = True
    return app.test_client()

def test_list_tasks(client):
    res = client.get('/tasks')
    assert res.status_code == 200
    assert res.get_json() == [{'id': 1, 'title': '買い物'}, {'id': 2, 'title': '掃除'}]

def test_create_task(client):
    res = client.post('/tasks', json={'title': '読書'})
    assert res.status_code == 201
```

| メソッド / 属性 | 説明 |
|---|---|
| `app.config['TESTING'] = True` | テストモードを有効にする。エラーが発生したとき、`@app.errorhandler`に処理させず**例外をそのまま送出**するようになるため、テストで原因を特定しやすくなる |
| `client.get(path)` / `client.post(path, json=...)` | 実際にHTTPリクエストを送るのと同じ結果が得られる |
| `res.status_code` | ステータスコード |
| `res.data` | レスポンス本文（バイト列）。文字列を含むか調べるときは`'文字列'.encode('utf-8') in res.data` |
| `res.get_json()` | JSONレスポンスを辞書/リストとして取得 |
| `follow_redirects=True` | リダイレクト先まで自動的についていく |

### 注意：テスト間で状態を共有しない

`example/02_app.py`の`TASKS`はただのグローバルなリストです。あるテストで`POST /tasks`をすると、そのテストが終わった後も`TASKS`にデータが残り続け、**他のテストの実行結果に影響してしまいます**。

```python
@pytest.fixture(autouse=True)
def reset_tasks():
    app_module.TASKS.clear()
    app_module.TASKS.extend([{'id': 1, 'title': '買い物'}, {'id': 2, 'title': '掃除'}])
```

`autouse=True`を付けたフィクスチャは、明示的に引数へ書かなくても**すべてのテストの前に自動実行**されます。これでテストごとに状態をリセットし、実行順序に関係なく同じ結果になるようにしています。実際、このリセットを外した状態で`test_create_task`を`test_list_tasks`より先に実行すると、後者が失敗することが確認できます（テストの実行順序に依存する脆いテストの典型例）。

### 実行方法

```bash
pytest 020_testing/example/test_02_flask_client.py -v
```

### 動作確認：テスト間の状態リセットが効いているかを確認する

| 確認する操作 | 確認したいこと |
|---|---|
| そのまま実行する | `test_list_tasks`・`test_create_task`など全件`PASSED`になる |
| `reset_tasks`フィクスチャの`@pytest.fixture(autouse=True)`を`@pytest.fixture`（`autouse=True`を外す）に変更して実行する | 実行順序によっては`test_list_tasks`が`FAILED`になることがある（前のテストで`POST`した「読書」タスクが残ってしまい、期待した2件のリストと一致しなくなるため）。確認後は必ず`autouse=True`に戻す |
| `pytest 020_testing/example/test_02_flask_client.py -v -p no:randomly`のように実行順序を変えて試す（ランダム化プラグインが無い場合は通常の順序で複数回実行） | `autouse=True`が効いていれば、実行順序が変わっても結果は常に同じになる |

**正常な状態の見分け方**：テストの実行順序を変えても結果が変わらないのが正しい状態です。順序によって結果が変わる場合は、どこかのテストが他のテストの後始末に依存している（グローバルな状態を共有している）サインです。

---

## 3. DBを使うアプリのテスト — フィクスチャで使い捨てのDBを用意する

`018_ownership_crud`のようにDBを使うアプリをテストするときは、開発用のDBファイル（`memos.sqlite`）を直接使ってはいけません。テストのたびに**まっさらな状態**から始められるよう、インメモリのSQLiteに差し替えます。

```python
# conftest.py
@pytest.fixture
def app():
    flask_app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI='sqlite:///:memory:',   # ← ファイルではなくメモリ上にDBを作る
        WTF_CSRF_ENABLED=False,                          # ← テストではCSRFトークンのやり取りを省略する
    )
    with flask_app.app_context():
        db.create_all()
        yield flask_app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()
```

| 設定 | 理由 |
|---|---|
| `SQLALCHEMY_DATABASE_URI='sqlite:///:memory:'` | テストのたびに空のDBが作られ、実行後は消える。開発用DBを汚さない |
| `WTF_CSRF_ENABLED=False` | 本番ではCSRF保護は必須だが、テストでは`csrf_token`をHTMLから毎回取り出すのが面倒なため、テスト時だけ無効化する |
| `yield` の前後で`create_all()`/`drop_all()` | 各テストの実行前にテーブルを作り、実行後に消す（テスト同士が影響し合わないようにする） |

### ログイン済みの状態を使い回すフィクスチャ

```python
@pytest.fixture
def sample_user(app):
    user = User(username='alice')
    user.set_password('pass1234')
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture
def logged_in_client(client, sample_user):
    client.post('/auth/login', data={'username': 'alice', 'password': 'pass1234'})
    return client
```

フィクスチャは他のフィクスチャを引数として受け取れます（`logged_in_client`が`sample_user`に依存している）。これを使うと、「ログイン済みのユーザーとしてリクエストを送る」というテストで頻出のセットアップを1行で済ませられます。

---

## 実行方法

```bash
pytest 020_testing/example/test_01_pytest_basics.py -v
pytest 020_testing/example/test_02_flask_client.py -v
```

---

## 4. 練習問題：メモ帳アプリのテストを書こう

> [challenge/](challenge/) — 問題（`test_memos.py`・`test_pin.py`） ｜ [challenge/answer/](challenge/answer/) — 解答

### 問題：019_javascriptのメモ帳アプリに対するテストを書こう

`019_javascript`で作ったメモ帳アプリ（`challenge/`にアプリ本体をそのままコピーしてあります）に対して、`test_memos.py`・`test_pin.py`のテストを完成させてください。フィクスチャ（`client`・`sample_user`・`sample_memo`・`logged_in_client`）は`conftest.py`にすでに用意されています。

```bash
cd 020_testing/challenge
pytest -v
```

#### 仕様

| ファイル | テスト | 内容 |
|---|---|---|
| `test_memos.py` | `test_memo_list_shows_title` | 未ログインでもメモ一覧にタイトルが表示される |
| `test_memos.py` | `test_memo_detail_shows_owner` | メモ詳細に追加者のユーザー名が表示される |
| `test_memos.py` | `test_new_memo_requires_login` | 未ログインで`/memos/new`にアクセスするとログイン画面に転送される |
| `test_memos.py` | `test_other_user_cannot_edit_memo` | 他人のメモの編集ページは404になる |
| `test_pin.py` | `test_toggle_pin_requires_login` | 未ログインで`toggle-pin`にアクセスするとログイン画面に転送される |
| `test_pin.py` | `test_toggle_pin_flips_state` | `toggle-pin`を呼ぶと`is_pinned`が反転し、JSONで返る |
| `test_pin.py` | `test_toggle_pin_twice_returns_to_original` | 2回呼ぶと元の状態に戻る |
| `test_pin.py` | `test_pinned_memo_appears_first` | ピン留めしたメモが一覧の先頭に表示される |

#### ヒント

- `client.get(...)` / `client.post(...)`の戻り値の`.data`（バイト列）に、期待する文字列が含まれるか`in`で確認する（本章セクション2）
- ログインが必要な操作は`logged_in_client`フィクスチャを使う（セクション3）
- `test_pin.py`は画面ではなくJSONを返すルート（`019_javascript`の`toggle-pin`）が対象。`response.get_json()`で辞書として結果を取得する（セクション2の`res.get_json()`と同じ）
- **`pass`だけのテスト関数は、アサーションが1つもないので必ず「成功」してしまいます。** 実装が終わるまでは`pytest.fail('TODO: 実装してください')`が残るようにしてあるので、これが消えて`assert`が正しく書けていることを確認してから提出してください
- `challenge/`で`pytest`を実行すると`challenge/answer/`のテストまで一緒に収集してしまいそうですが、`pytest.ini`の`norecursedirs = answer`で除外されています（同名の`test_memos.py`が2箇所にあるとpytestの収集がエラーになるため）
- `challenge/answer/`にも空の`pytest.ini`を置いてあります。これが無いと、`answer/`の中で`pytest`を実行してもpytestが親ディレクトリの`challenge/pytest.ini`まで探しに行ってrootdirを`challenge/`だと判断し、`challenge/conftest.py`（問題側）まで一緒に読み込んでしまいます（`conftest.py`は`rootdir`から実行対象のディレクトリまで、経路上のものが全て読み込まれるため）。`answer/`に空でも`pytest.ini`を置いておくことで、pytestがそこで探索を打ち切り、`answer/`だけで完結させられます

解答は`challenge/answer/`を参照してください。

### 動作確認：未実装（challenge）と完成版（answer）でテスト結果がどう違うか

```bash
cd 020_testing/challenge
pytest -v
```

| 確認する操作 | 確認したいこと |
|---|---|
| 実装前に`challenge/`で`pytest -v`を実行する | 8件のテストすべてが`FAILED`になる。エラーメッセージに`Failed: TODO: 実装してください`が表示される（`pytest.fail(...)`によるもの） |
| 1つのテスト（例: `test_memo_list_shows_title`）だけ実装して再実行する | そのテストだけ`PASSED`に変わり、残り7件は`FAILED`のまま |
| 全問実装後に`pytest -v`を実行する | 8件すべて`PASSED`になる |
| `cd 020_testing/challenge/answer`で`pytest -v`を実行する | 同じく8件すべて`PASSED`になる（最初から完成しているため） |
| `challenge/`のトップディレクトリ（`020_testing/`）で`pytest`を実行する | `challenge/`と`challenge/answer/`のテストが重複収集されず、エラーにならない（`pytest.ini`の`norecursedirs`設定が効いている） |

**正常な状態の見分け方**：実装が終わっていないテストは`FAILED`になるべきで、**`pass`だけで何もしないテストが`PASSED`として紛れ込んでいないか**が最大の注意点です（ヒント参照）。全問実装後は`challenge/`と`challenge/answer/`の結果が完全に一致する（どちらも8件`PASSED`）のが正しい状態です。

## 次のステップ

続きは [021_webapi](../021_webapi) で、`requests`を使って外部APIを呼び出す方法を学びます。
