# 021 Web API の基礎

これまでの章では自分が API を提供する側（サーバー）を作ってきました。このチャプターでは逆に、「Web API とは何か」を `requests` ライブラリで外部 API を叩く形で体験します。

## 前提

| チャプター | 使う知識 |
|---|---|
| 016_typehints | 基本の型ヒント・Union |
| 020_testing | 続きとして使うメモアプリ本体（テスト済み） |

## 目次

1. [郵便番号検索 — requestsの最初の一歩](#1-郵便番号検索--requestsの最初の一歩)
2. [Responseオブジェクトの基本](#2-responseオブジェクトの基本)
3. [POSTリクエスト](#3-postリクエスト)
4. [エラーハンドリングとタイムアウト](#4-エラーハンドリングとタイムアウト)
5. [練習問題：メモに場所を記録できるようにしよう](#5-練習問題メモに場所を記録できるようにしよう)

---

## フォルダ構成

```
example/
├── 01_get_request.py           # 1. 郵便番号検索(GETの基本)
├── 02_response_object.py      # 2. Responseオブジェクトの基本
├── 03_post_request.py         # 3. POSTリクエスト
└── 04_error_handling.py       # 4. エラーハンドリングとタイムアウト

challenge/                      020_testingの続き（000_my_appに組み込む機能の変更分）
├── app.py / models.py / ...    メモアプリ本体（020_testingと同じ・is_pinnedのfetch API実装済み）
├── memos/views.py               メモ登録・更新時に郵便番号から住所を解決する処理を追加
└── answer/
    └── app.py / models.py / ...
```

---

## 1. 郵便番号検索 — requestsの最初の一歩

郵便番号検索 API（[zipcloud](https://zipcloud.ibsnet.co.jp/doc/api)）に `requests` で GET リクエストを送り、JSON レスポンスから住所を取り出して表示するコマンドラインスクリプト。

### コード

> [example/01_get_request.py](example/01_get_request.py)

```python
import requests
import json

url: str = "https://zipcloud.ibsnet.co.jp/api/search"

# ユーザーが入力した郵便番号を受け取る
zip: str = input("Zipcode =>")

# クエリパラメータとしてセット
param: dict[str, str] = {"zipcode": zip}

# HTTP GET リクエストを送信
res: requests.Response = requests.get(url, param)

# JSON文字列を辞書に変換
data: dict = json.loads(res.text)

if data['results'] is not None:
    address_info = data['results'][0]
    zipcode = address_info['zipcode']
    address = f"{address_info['address1']}{address_info['address2']}{address_info['address3']}"
    print(f"Zipcode : {zipcode} Address : {address}")
else:
    print("No address information was found.")
```

### ポイント

| 要素 | 説明 |
|---|---|
| `requests.get(url, param)` | 第2引数の辞書がクエリパラメータ（`?zipcode=...`）として付加される |
| `res.text` | レスポンス本文を文字列で取得 |
| `json.loads(res.text)` | JSON 文字列を Python の辞書に変換 |
| `data['results']` | 該当住所がない場合は `None` になる |

### Flask（サーバー側）と requests（クライアント側）の違い

これまでのチャプターでは自分が **API を提供する側**（サーバー）を作ってきました。
このチャプターでは逆に、外部の API を **呼び出す側**（クライアント）を体験します。

```
これまで： ブラウザ ──リクエスト──▶ 自作の Flask サーバー
この章  ： このスクリプト ──リクエスト──▶ 外部の zipcloud API
```

### 実行方法

```bash
pip install requests
python 021_webapi/example/01_get_request.py
```

郵便番号（例: `7830060`）を入力すると住所が表示されます。

### 動作確認：存在する郵便番号と存在しない郵便番号の違い

（インターネット接続が必要です）

| 確認する操作 | 確認したいこと |
|---|---|
| `7830060`を入力する | `Zipcode : 783-0060 Address : 高知県南国市大そね甲`のように住所が表示される |
| 存在しない郵便番号（例: `0000000`）を入力する | `No address information was found.`と表示される（`data['results']`が`None`になるケース） |
| ハイフン付き（`783-0060`）を入力する | zipcloud APIはハイフンの有無を区別しないため、同じ結果が返る |

**正常な状態の見分け方**：該当する郵便番号なら住所が、存在しない郵便番号なら「見つからない」旨のメッセージが表示されれば正常です。何も表示されずスクリプトが止まる場合はインターネット接続、または`requests`のインストール漏れを疑ってください。

---

## 2. Responseオブジェクトの基本

> [example/02_response_object.py](example/02_response_object.py)

`requests.get()` の戻り値（`Response`オブジェクト）が持っている、よく使う属性・メソッドをまとめて確認します。

```python
import requests

url: str = "https://jsonplaceholder.typicode.com/posts/1"
res: requests.Response = requests.get(url)

print("status_code:", res.status_code)          # 200
print("ok:", res.ok)                            # 200番台ならTrue
print("headers:", res.headers["Content-Type"])  # レスポンスヘッダーを辞書のように参照
print("text:", res.text[:50], "...")            # 文字列としての本文
print("json:", res.json())                      # json.loads(res.text) と同じ結果を得るショートカット
```

### ポイント

| 属性・メソッド | 説明 |
|---|---|
| `res.status_code` | HTTPステータスコード（`200`, `404`など） |
| `res.ok` | ステータスコードが200番台なら`True`、それ以外は`False` |
| `res.headers` | レスポンスヘッダー。辞書のように`res.headers["Content-Type"]`で参照できる |
| `res.text` | レスポンス本文を**文字列**として取得 |
| `res.json()` | レスポンス本文をJSONとしてパースし、辞書/リストで取得（`1. 郵便番号検索`で使った`json.loads(res.text)`のショートカット） |

### 実行方法

```bash
python 021_webapi/example/02_response_object.py
```

### 動作確認：Responseオブジェクトの各属性が何を返すか

（インターネット接続が必要です）

| 確認する操作 | 確認したいこと |
|---|---|
| そのまま実行する | `status_code: 200`・`ok: True`が表示される（存在する投稿を取得しているため） |
| `url`を`.../posts/99999`のような存在しないIDに変更して実行する | `status_code: 404`・`ok: False`になる（`404`は`ok`が`False`になる境目） |
| `print("json:", res.json())`の出力を見る | `res.text`をJSONとしてパースした辞書（`{'userId': ..., 'id': 1, 'title': ..., 'body': ...}`）が表示される |

**正常な状態の見分け方**：`res.ok`は`res.status_code`が200番台のときだけ`True`になります。存在しないURLを指定したのに`ok: True`のままの場合、URLの指定ミスで別の（存在する）リソースを取得してしまっていないか確認してください。

---

## 3. POSTリクエスト

> [example/03_post_request.py](example/03_post_request.py)

ここまでは `GET` でしたが、データを送信する `POST` も基本の書き方は同じです。送信するデータの持たせ方に2種類あります。

```python
import requests

url: str = "https://jsonplaceholder.typicode.com/posts"

payload: dict[str, str | int] = {
    "title": "Flask学習",
    "body": "requestsモジュールでPOSTする例",
    "userId": 1,
}

# json= を使うと、辞書を自動でJSON文字列に変換し
# Content-Type: application/json も自動で付与してくれる
res: requests.Response = requests.post(url, json=payload)

print("status_code:", res.status_code)   # 201 Created
print("response:", res.json())
```

### ポイント

| 引数 | 用途 | Content-Type |
|---|---|---|
| `json=辞書` | JSON形式で送信したいとき(一般的なWeb API向け) | `application/json`（自動付与） |
| `data=辞書` | フォーム形式で送信したいとき(HTMLの`<form>`と同じ形式) | `application/x-www-form-urlencoded` |
| `params=辞書` | GETのクエリパラメータ（`1. 郵便番号検索`で使ったもの） | — |

`022_flask_api` で作った自分のAPI（`POST /api/memos`）も、`requests.post('http://127.0.0.1:5081/api/memos', json={'title': '...'})` のように同じ書き方で呼び出せます。

### 実行方法

```bash
python 021_webapi/example/03_post_request.py
```

### 動作確認：送信したデータがレスポンスに反映されているか

（インターネット接続が必要です。このAPIは実際には保存されないダミーのテスト用エンドポイントです）

| 確認する操作 | 確認したいこと |
|---|---|
| そのまま実行する | `status_code: 201`（Created）と表示される |
| `response:`の中身を見る | 送信した`payload`（`title`・`body`・`userId`）がそのまま含まれ、さらに`id`（新規採番されたID、通常`101`）が追加されている |
| `payload`から`title`を削除して実行する | このテスト用APIはバリデーションをしないため、`title`が無くてもエラーにはならず`201`のまま返ってくる点に注意（自作のAPIなら`022_flask_api`のように`400`を返すべき場面） |

**正常な状態の見分け方**：`status_code`が`201`で、レスポンスのJSONに送信したデータがそのまま含まれていれば正常です。

---

## 4. エラーハンドリングとタイムアウト

> [example/04_error_handling.py](example/04_error_handling.py)

`requests` は、通信自体が失敗したとき（例外）と、通信は成功したがサーバーがエラーを返したとき（`404`や`500`など）で扱いが異なります。

```python
import requests

# 1. 接続エラー(存在しないドメインなど)
try:
    requests.get("https://this-domain-does-not-exist-abc123xyz.com", timeout=3)
except requests.exceptions.ConnectionError:
    print("接続エラーが発生しました")

# 2. ステータスコードが400/500番台でも例外は起きない
res: requests.Response = requests.get("https://jsonplaceholder.typicode.com/posts/99999")
print("status_code:", res.status_code)  # 404

# raise_for_status() を呼ぶと、400/500番台のときだけ例外を送出してくれる
try:
    res.raise_for_status()
except requests.exceptions.HTTPError as e:
    print("HTTPエラーが発生しました:", e)

# 3. タイムアウトの指定(応答が遅いサーバーへの対策)
try:
    requests.get("https://jsonplaceholder.typicode.com/posts", timeout=0.001)
except requests.exceptions.Timeout:
    print("タイムアウトしました")
```

### ポイント

| ケース | 説明 |
|---|---|
| `requests.exceptions.ConnectionError` | ドメインが存在しない、ネットワークが繋がらない等で発生 |
| ステータスコードが400/500番台 | **例外にはならず**、`res.status_code`に反映されるだけ |
| `res.raise_for_status()` | 400/500番台のときだけ`HTTPError`を送出させる。呼ばなければ何もチェックしない |
| `timeout=秒数` | 指定時間内に応答が無いと`requests.exceptions.Timeout`を送出。**指定しないと応答がある限り無限に待ち続ける**ため、実務では必ず指定する |

**注意**：`requests`はデフォルトで`timeout`を設定しません。本番のコードで`timeout`を省略すると、相手サーバーが応答しない場合にプログラムが永遠に止まってしまうため、必ず指定する習慣をつけましょう。

### 実行方法

```bash
python 021_webapi/example/04_error_handling.py
```

### 動作確認：3種類のエラーがそれぞれ正しく捕まえられているか

（インターネット接続が必要です）

| 確認する操作 | 確認したいこと |
|---|---|
| そのまま実行する | 「接続エラーが発生しました」「status_code: 404」「HTTPエラーが発生しました: ...」「タイムアウトしました」の4行が順に表示される |
| 1つ目の`try`ブロックの`ConnectionError`を`Timeout`に変えて実行する | 存在しないドメインへの接続は`ConnectionError`（`Timeout`ではない）なので、`except`で捕まえられずに例外がそのまま送出されてプログラムが止まる。捕まえたい例外の種類が合っているかの確認になる |
| `res.raise_for_status()`をコメントアウトして実行する | 404が返ってきても例外にならず、「HTTPエラーが発生しました」の行が表示されなくなる（`raise_for_status()`を呼ばない限りステータスコードのチェックは自動では行われない） |
| `timeout=0.001`を`timeout=10`のような十分な値に変える | ほとんどの場合タイムアウトせずに応答が返り、「タイムアウトしました」が表示されなくなる |

**正常な状態の見分け方**：4種類のケースそれぞれで対応する`except`節が実行され、プログラムが例外で異常終了しないことが正常です。`Traceback`が表示されて止まった場合は、その例外を捕まえる`except`の型が合っているか確認してください。

---

## 5. 練習問題：メモに場所を記録できるようにしよう

> [challenge/memos/views.py](challenge/memos/views.py) — 問題 ｜ [challenge/answer/memos/views.py](challenge/answer/memos/views.py) — 解答

### 問題：メモの登録・編集時に郵便番号から住所を自動解決しよう

メモの一覧・詳細・追加・編集・削除・ピン留めの機能はそのままです（`020_testing`にすでに実装済み）。これに、メモを**場所に紐づけて記録できる**機能を追加します。フォームに郵便番号を入力すると、zipcloud APIで住所を自動解決してメモに保存します（郵便番号は任意入力）。

```bash
cd 021_webapi/challenge
flask db init
flask db migrate -m "add postal_code and address to memos"
flask db upgrade
python app.py
```

#### 仕様

| 問題 | 内容 |
|---|---|
| 1 | `memos/views.py`の`resolve_address(postal_code)`を実装する。zipcloud APIをGETで呼び出し、該当住所があればその文字列を、無ければ`None`を返す（`timeout`を指定すること） |
| 2 | `create()`・`update()`で、`postal_code`が入力されていれば`resolve_address()`を呼び、解決できた住所を`Memo`の`address`に保存する（`postal_code`が空なら何もせず保存する） |
| 3 | 住所が見つからない場合・通信に失敗した場合は、メモを作成/更新せずflashメッセージを出してフォーム画面に戻す |

#### ヒント

- `requests.get(ZIPCLOUD_URL, params={'zipcode': postal_code}, timeout=5)`（本章セクション1・4）
- レスポンスの`data['results']`が`None`なら該当住所なし（セクション1）
- 通信自体の失敗（接続エラー・タイムアウト）は`requests.exceptions.RequestException`で`try/except`する（セクション4）。この例外は`ConnectionError`・`Timeout`の親クラスなので、両方まとめて捕まえられる
- `Memo`の`postal_code`・`address`カラム、フォームの`postal_code`フィールド、テンプレートの入力欄・表示はすでに追加済み。マイグレーションを実行してから動作確認すること
- 見た目やCSRF・所有権・ピン留めの基本操作は変更不要（`018_ownership_crud`・`019_javascript`と同じパターン）

### 動作確認：郵便番号の有無・正誤で保存されるメモが変わるか

```bash
cd 021_webapi/challenge
python app.py
```

（インターネット接続が必要です）

| 確認する操作 | 確認したいこと |
|---|---|
| `http://127.0.0.1:5078/memos/new`で郵便番号を**入力せずに**メモを追加する | メモが作成され、詳細ページに住所は表示されない（`address`が`None`のまま） |
| 存在する郵便番号（例: `1000001`）を入力してメモを追加する | メモが作成され、詳細ページに解決された住所（例: `東京都千代田区千代田`）が表示される |
| 存在しない郵便番号（例: `0000000`）を入力してメモを追加する | メモは**作成されず**、flashメッセージ（「該当する住所が見つかりませんでした。」）とともにフォーム画面が再表示される |
| Wi-Fiを切るなどしてインターネット接続が無い状態で郵便番号を入力してメモを追加する | メモは作成されず、「住所の取得に失敗しました。」のようなflashメッセージが表示される（`requests.exceptions.RequestException`を捕まえている） |
| 既存メモの編集画面で郵便番号を後から追加・変更する | 保存後、詳細ページの住所表示が更新される |

**正常な状態の見分け方**：郵便番号を入力しなければメモはそのまま作成され、正しい郵便番号なら住所付きで作成され、間違った郵便番号や通信エラーの場合は**メモ自体が作成されずに**フォーム画面へ戻ることが正しい状態です。エラーなのにメモが作成されてしまう場合は、`resolve_address()`のエラーハンドリング（`return`のタイミング）を疑ってください。

## 次のステップ

続きは [022_flask_api](../022_flask_api) で、今度は Flask を使って **API を提供する側** を作る学習に入ります。
