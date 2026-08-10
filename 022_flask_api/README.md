# 022 Flask で作るAPI機能

`017_blueprint` までで学んだ Flask の知識だけで、画面(HTML)ではなく **JSON を返すAPI** を作ります。新しいライブラリは不要で、`jsonify()` の使い方と「エンドポイントの設計」を押さえるのが目的です。

## 前提

| チャプター | 使う知識 |
|---|---|
| 004_flask_basic | ルーティング・HTTPメソッド・パスパラメータ・クエリパラメータ |
| 016_typehints | 基本の型ヒント・Optional・Union |
| 017_blueprint | Blueprintによるルートの分割 |

## 目次

1. [jsonifyでJSONを返す](#1-jsonifyでjsonを返す)
2. [Blueprintで画面用とAPI用のルートを分ける](#2-blueprintで画面用とapi用のルートを分ける)
3. [`@app.get` / `@app.post` ショートカット](#3-appget--apppost-ショートカット)
4. [ステータスコードの使い分け](#4-ステータスコードの使い分け)
5. [地図に表示するデータを提供する](#5-地図に表示するデータを提供する)
6. [練習問題：メモデータを返すJSON APIを追加しよう](#6-練習問題メモデータを返すjson-apiを追加しよう)

---

## フォルダ構成

```
example/
├── app.py              # Blueprintの登録 + 地図ページのルート
├── api/
│   └── views.py         # APIのエンドポイント本体
└── templates/
    └── map.html          # Leafletで地図を表示するページ

challenge/               021_webapiの続き（000_my_appに組み込む機能の変更分）
├── app.py / models.py / ...   021_webapiと同じアプリ本体（メモ帳・postal_code対応済み）
├── api/views.py                メモデータを返すJSON API（新規）
└── answer/
    └── app.py / models.py / ...
```

---

## 1. jsonifyでJSONを返す

> [example/api/views.py](example/api/views.py)

Flaskで画面を作るときは文字列やHTMLを`return`していましたが、APIでは辞書やリストを`jsonify()`でくるんで返します。

```python
from flask import Blueprint, jsonify, Response

api_bp = Blueprint('api', __name__, url_prefix='/api')

books: list[dict[str, int | str]] = [
    {"id": 1, "title": "python"},
    {"id": 2, "title": "flask"},
]

@api_bp.get('/books')
def get_books() -> Response:
    return jsonify(books)
```

### ポイント

| 要素 | 説明 |
|---|---|
| `jsonify(データ)` | 辞書・リスト・文字列・数値などをJSONレスポンス(`Content-Type: application/json`)に変換する |

### `return {...}` だけでもJSONになる場合／ならない場合

Flask 1.1以降は、ビュー関数が**辞書やリストをそのまま`return`しても自動でJSONに変換**されます。ただし、これは辞書・リストに限った話で、**文字列や数値をそのまま返すとJSONにはなりません**。この違いは実際に動かして確認できます。

```python
@app.route('/dict')
def return_dict():
    return {"message": "hello"}       # OK: 自動でJSONになる({"message":"hello"})

@app.route('/str')
def return_str():
    return "hello"                    # NG: text/htmlとして返る("hello"という文字列のまま)

@app.route('/int')
def return_int():
    return 42                         # エラー: intは有効な戻り値として扱われない

@app.route('/str_json')
def return_str_json():
    return jsonify("hello")           # OK: 明示的にjsonify()すればJSONになる("hello"という文字列)
```

| 戻り値の型 | `return`だけ | `jsonify()`を使う |
|---|---|---|
| 辞書・リスト | 自動でJSONになる | 同じくJSONになる(挙動は変わらない) |
| 文字列・数値・真偽値 | JSONにならない(文字列はHTML扱い、数値・真偽値はそもそもエラー) | JSONになる |

**まとめ**：APIのレスポンスが辞書やリストである限り`jsonify()`を省略しても動きますが、「これはAPIのレスポンスである」ことを明示する・トップレベルが文字列や数値になるケースにも対応できるという理由で、このリポジトリでは一貫して`jsonify()`を使う書き方を採用しています。

---

## 2. Blueprintで画面用とAPI用のルートを分ける

> [example/app.py](example/app.py)

`017_blueprint` と同じ要領で、`url_prefix='/api'` を持つBlueprintを作ると、画面用のルートとAPI用のルートをきれいに分離できます。

```python
from flask import Flask
from api.views import api_bp

app = Flask(__name__)
app.register_blueprint(api_bp)
```

既存のアプリに画面用のBlueprint(`books_bp`など)がある場合も、これと並べて `app.register_blueprint(api_bp)` するだけでAPIを追加できます(`018_ownership_crud`にAPIを足す場合も同じ方法)。

### エンドポイント一覧

| メソッド | パス | 処理 |
|---|---|---|
| GET | `/api/books` | 書籍一覧を取得 |
| GET | `/api/books/<int:book_id>` | 1件取得(無ければ404) |
| POST | `/api/books` | 新規作成 |
| DELETE | `/api/books/<int:book_id>` | 削除(無ければ404) |

---

## 3. `@app.get` / `@app.post` ショートカット

Flask 2.0以降は `@app.route(..., methods=['GET'])` の代わりに、HTTPメソッドごとのショートカットデコレータが使えます。FastAPIの `@app.get` / `@app.post` と同じ書き味です。

```python
# 従来の書き方
@api_bp.route('/books', methods=['POST'])
def create_book():
    ...

# ショートカット(このチャプターではこちらを採用)
@api_bp.post('/books')
def create_book() -> tuple[Response, int]:
    data: dict = request.get_json()          # JSONボディを辞書として取得
    new_book: dict[str, int | str] = {"id": len(books) + 1, "title": data.get("title")}
    books.append(new_book)
    return jsonify(new_book), 201
```

### ポイント

| 要素 | 説明 |
|---|---|
| `request.get_json()` | リクエストボディのJSON文字列を辞書に変換して取得 |
| `Blueprint`にも`.get()`/`.post()`が使える | `app`だけでなく`Blueprint`インスタンスにも同じショートカットがある |

---

## 4. ステータスコードの使い分け

```python
@api_bp.get('/books/<int:book_id>')
def get_book(book_id: int) -> tuple[Response, int] | Response:
    book: Optional[dict[str, int | str]] = next((b for b in books if b["id"] == book_id), None)
    if book is None:
        return jsonify({"detail": "Book not found"}), 404
    return jsonify(book)

@api_bp.delete('/books/<int:book_id>')
def delete_book(book_id: int) -> tuple[str, int] | tuple[Response, int]:
    global books
    if not any(b["id"] == book_id for b in books):
        return jsonify({"detail": "Book not found"}), 404
    books = [b for b in books if b["id"] != book_id]
    # 204 No Content はレスポンスボディを持てない
    return '', 204
```

### ポイント

| コード | 使う場面 | このサンプルでの利用箇所 |
|---|---|---|
| 200 | 取得・更新が成功 | `GET /api/books` |
| 201 | 新規作成が成功 | `POST /api/books` |
| 204 | 成功したが返す内容が無い | `DELETE /api/books/<id>` |
| 404 | 対象が見つからない | 存在しない`book_id`を指定したとき |

**注意**：204は仕様上レスポンスボディを持てません。`jsonify({...}), 204` のように本文を付けて返すとクライアント側でJSONパースエラーになることがあるため、`return '', 204` のように空文字列で返します。

---

## 実行方法

```bash
cd 022_flask_api/example
python app.py
```

```bash
curl http://127.0.0.1:5064/api/books
curl http://127.0.0.1:5064/api/books/1
curl -X POST http://127.0.0.1:5064/api/books -H "Content-Type: application/json" -d '{"title": "新しい本"}'
curl -i -X DELETE http://127.0.0.1:5064/api/books/1
curl -i http://127.0.0.1:5064/api/books/99
```

### 動作確認：ステータスコードとJSONレスポンスの違い

| 確認する操作 | 確認したいこと |
|---|---|
| `curl http://127.0.0.1:5064/api/books` | 初期データ2件（`{"id":1,"title":"python"}`・`{"id":2,"title":"flask"}`）を含むJSON配列がそのまま返る |
| `curl http://127.0.0.1:5064/api/books/1` | `id`が一致する1件分のJSON（`{"id":1,"title":"python"}`）だけが返る（配列ではなく単一オブジェクト） |
| `curl -X POST ... -d '{"title": "新しい本"}'` | `id:3`が自動採番された新しい本のJSONが返る（`-i`を付ければステータスコードが**201**であることも確認できる） |
| `curl -i -X DELETE .../api/books/1` | レスポンスボディが空で、ステータスコードだけが**204**と表示される（`-i`を付けないと画面に何も表示されず失敗したように見えるので注意） |
| `curl -i http://127.0.0.1:5064/api/books/99` | 存在しない`id`なのでステータスコード**404**と`{"detail": "Book not found"}`が返る |
| DELETE実行後に`curl http://127.0.0.1:5064/api/books`をもう一度実行する | `id:1`の本が消えている（サーバーを再起動するとダミーデータの`books`リストが初期状態に戻る点に注意） |

**正常な状態の見分け方**：取得・作成が成功したときは200/201で本文にJSONが入り、削除成功時は204で本文が空、存在しないIDを指定したときだけ404で`{"detail": ...}`が返ります。本文が空なのに200が返る、あるいは404なのに本文が空、という組み合わせが出たら実装ミスを疑ってください。

---

## 5. 地図に表示するデータを提供する

> [example/api/views.py](example/api/views.py)（`get_shops`） | [example/templates/map.html](example/templates/map.html)

ここまでは「データを返すだけ」のAPIでしたが、実際にフロントエンド（ブラウザ）がそのJSONを使って何かを表示する例として、**地図上にピンを立てる**機能を作ります。地図の描画には **Leaflet.js**（OpenStreetMapのタイルを使う、APIキー不要のライブラリ）を使います。

### 地点データを返すAPI

```python
shops: list[dict[str, int | str | float]] = [
    {"id": 1, "name": "本店（東京駅）", "lat": 35.681236, "lng": 139.767125},
    {"id": 2, "name": "支店A（東京タワー）", "lat": 35.658581, "lng": 139.745433},
    {"id": 3, "name": "支店B（東京スカイツリー）", "lat": 35.710063, "lng": 139.810700},
]

@api_bp.get('/shops')
def get_shops() -> Response:
    return jsonify(shops)
```

`GET /api/books` と全く同じ考え方で、地点のリスト（緯度`lat`・経度`lng`を含む辞書）をJSONで返しているだけです。

### 地図ページ（`/map`）

`app.py` に画面用のルートを1つ追加し、`templates/map.html` を返します。

```python
from flask import Flask, render_template
from api.views import api_bp

app = Flask(__name__)
app.register_blueprint(api_bp)

@app.route('/map')
def show_map() -> str:
    return render_template('map.html')
```

`map.html` の中では、JavaScriptの `fetch('/api/shops')` で先ほどのAPIを呼び出し、返ってきたJSONを使ってピンを立てています。

```javascript
const map = L.map('map').setView([35.681236, 139.767125], 12);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

fetch('/api/shops')
    .then(res => res.json())
    .then(shops => {
        shops.forEach(shop => {
            L.marker([shop.lat, shop.lng])
                .addTo(map)
                .bindPopup(shop.name);
        });
    });
```

### ポイント

| 要素 | 説明 |
|---|---|
| `L.map('map').setView([lat, lng], zoom)` | 指定した座標を中心に地図を初期化する |
| `L.tileLayer(URL)` | 地図の背景画像（タイル）を読み込む。ここではOpenStreetMapの無料タイルを使用（APIキー不要） |
| `fetch('/api/shops')` | ブラウザからFlaskのAPIをJavaScriptで呼び出す（Python側の`requests`で外部APIを呼ぶのと同じ発想） |
| `L.marker([lat, lng]).bindPopup(name)` | 指定座標にピンを立て、クリックすると名前を表示する |

**Google Maps との違い**：Google Maps Platformは表示だけでも基本的にAPIキー（と課金設定）が必要ですが、Leaflet + OpenStreetMapは無料・APIキー不要で使えるため、学習用途に向いています。

### 実行方法

```bash
cd 022_flask_api/example
python app.py
```

ブラウザで `http://127.0.0.1:5064/map` にアクセスすると、3つの地点にピンが立った地図が表示される。

### 動作確認：APIのデータ件数と地図のピンの数が一致するか

| 確認する操作 | 確認したいこと |
|---|---|
| `curl http://127.0.0.1:5064/api/shops` | 3件の地点データ（本店・支店A・支店B）を含むJSON配列がステータス200で返る |
| ブラウザで`http://127.0.0.1:5064/map`にアクセスする | 地図上にピンが**3つ**表示される |
| 地図上のピンをそれぞれクリックする | ポップアップに`curl`で確認した`name`（例：「本店（東京駅）」）と同じ文字列が表示される |

**正常な状態の見分け方**：`/api/shops`が返すJSON配列の件数と、地図上のピンの数が常に一致していることが正しい状態です。ピンが1つも表示されない場合は、ブラウザの開発者ツール（コンソール／ネットワークタブ）で`fetch('/api/shops')`がエラーになっていないか確認してください。

---

## 6. 練習問題：メモデータを返すJSON APIを追加しよう

> [challenge/api/views.py](challenge/api/views.py) — 問題 ｜ [challenge/answer/api/views.py](challenge/answer/api/views.py) — 解答

### 問題：画面用のBlueprintとは別に、メモデータを返すAPIを追加しよう

`021_webapi`で作ったメモ一覧・詳細・追加・編集・削除・ピン留めの機能はそのままです。ここに、画面用のBlueprint（`memos_bp`など）とは別の`api_bp`を追加し、メモデータをJSONで参照できるようにします。

```bash
cd 022_flask_api/challenge
flask db init
flask db migrate -m "create tables"
flask db upgrade
python app.py
```

```bash
curl http://127.0.0.1:5080/api/memos
curl http://127.0.0.1:5080/api/memos?category=仕事
curl http://127.0.0.1:5080/api/memos/1
curl -i http://127.0.0.1:5080/api/memos/999
```

### 動作確認：一覧・絞り込み・詳細取得・404の違い

問題3（`api_bp`の登録）を完成させるまでは、以下のどの`curl`も**404**（Blueprint未登録のため`/api/memos`自体が存在しない）になります。まずは`http://127.0.0.1:5080/memos/new`から画面でメモを1件追加してから確認してください。

| 確認する操作 | 確認したいこと |
|---|---|
| `curl http://127.0.0.1:5080/api/memos` | 追加したメモを含むJSON配列がステータス200で返る |
| `curl http://127.0.0.1:5080/api/memos?category=仕事` | 追加したメモのカテゴリが「仕事」なら、そのメモだけに絞り込まれた配列が返る（一致するメモが無ければ空配列`[]`） |
| 追加したメモの`id`（例：`1`）を指定して`curl http://127.0.0.1:5080/api/memos/1` | そのメモ1件分のJSON（`title`・`category`・`body`・`owner`など）が返る |
| `curl -i http://127.0.0.1:5080/api/memos/999`（存在しないid） | ステータスコード**404**と`{"detail": "Memo not found"}`が返る。HTMLの404ページではなくJSONである点に注意（本章セクション6のヒント） |

**正常な状態の見分け方**：存在するidを指定したときは200＋メモのJSON、存在しないidのときは404＋`{"detail": ...}`のJSONになっているのが正しい状態です。問題3が未完成のうちは全てのURLが404（Blueprint未登録によるFlask標準の404）になりますが、これは「メモが見つからない404」とは別物なので混同しないよう注意してください。

#### 仕様

| 問題 | 内容 |
|---|---|
| 1 | `GET /api/memos`でメモ一覧をJSONで返す（`?category=`が指定されていれば絞り込む） |
| 2 | `GET /api/memos/<id>`で1件をJSONで返す。無ければ`{"detail": "Memo not found"}`を404で返す |
| 3 | `app.py`で`api_bp`を`app.register_blueprint()`する |

#### ヒント

- `memo_to_dict()`はすでに用意されている。`Memo`オブジェクトを辞書に変換して`jsonify()`に渡す（本章セクション1）
- 一覧の絞り込みは`memos.index`と同じ`request.args.get('category')` + `filter_by(category=category)`のパターン
- 1件取得は`Memo.query.get(memo_id)`を使い、`get_or_404()`は使わない（HTMLの404ページではなくJSONのエラーレスポンスを返したいため。本章セクション4のステータスコードの考え方）
- 問題3が終わるまでは`/api/memos`にアクセスしても404になる（Blueprintが未登録のため）。これは正常な状態
- 見た目やCSRF・所有権・ピン留めの仕組みは`021_webapi`から変更不要

## 次のステップ

続きは [023_crud_api](../023_crud_api) で、JSON APIに書き込み系（POST/PUT/DELETE）を揃える方法を学びます。
