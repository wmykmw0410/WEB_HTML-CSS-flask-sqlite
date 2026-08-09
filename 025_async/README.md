# 025 同期処理と非同期処理

Python の `asyncio` を使った非同期処理の基礎を学び、それを Flask のビュー関数に組み込みます。`021_webapi`で`requests`を使って外部API（zipcloud API）を1件ずつ呼び出しましたが、複数件を**同時に**呼び出すとどれだけ速くなるかを実際に計測して確認します。

## 前提

| チャプター | 使う知識 |
|---|---|
| 016_typehints | 基本の型ヒント |
| 021_webapi | requestsで外部APIを呼び出す方法（zipcloud API） |
| 022_flask_api | FlaskでのJSON API作成 |

## 目次

1. [同期処理と非同期処理の基礎](#1-同期処理と非同期処理の基礎)
2. [Flaskのasyncビューで外部APIを並行に呼ぶ](#2-flaskのasyncビューで外部apiを並行に呼ぶ)
3. [Flaskのasyncの限界](#3-flaskのasyncの限界)

---

## フォルダ構成

```
example/
├── 01_asyncio_basics/
│   └── main.py          asyncio.sleepとgatherの基礎
└── 02_flask_async/
    └── app.py            Flaskの同期/非同期ビューの比較(zipcloud APIを複数同時に呼ぶ)

question/                 練習問題（1問1ファイル）
├── question01.py〜question04.py
└── answer/
    └── answer01.py〜answer04.py
```

---

## 1. 同期処理と非同期処理の基礎

> [example/01_asyncio_basics/main.py](example/01_asyncio_basics/main.py)

`time.sleep`（同期）と`asyncio.sleep`（非同期）を比較します。

```python
import time
import asyncio

# ---- 同期処理 ----
def sync_task(name: str) -> None:
    print(f"{name} Start")
    time.sleep(1)
    print(f"{name} End")

def run_sync_tasks() -> None:
    sync_task("Task1")
    sync_task("Task2")
    sync_task("Task3")

# ---- 非同期処理 ----
async def async_task(name: str) -> None:
    print(f"{name} Start")
    await asyncio.sleep(1)
    print(f"{name} End")

async def run_async_tasks() -> None:
    await asyncio.gather(
        async_task("TaskA"),
        async_task("TaskB"),
        async_task("TaskC"),
    )

asyncio.run(run_async_tasks())
```

### 実行結果

```
=== 同期処理 ===
経過時間: 3.01秒   ← 1秒 × 3件が順番に実行される

=== 非同期処理 ===
経過時間: 1.00秒   ← 3件が同時に待たれる
```

### ポイント

| 要素 | 説明 |
|---|---|
| `async def` | 非同期関数を定義する |
| `await` | 「ここで待っている間、他の処理に切り替えてよい」という目印 |
| `asyncio.sleep(n)` | `time.sleep(n)`の非同期版。待っている間に他のタスクを実行できる |
| `asyncio.gather(A, B, C)` | 複数の非同期関数を**同時に**開始し、すべて完了するまで待つ |
| `asyncio.run(main())` | 非同期処理のスタート地点。イベントループを作って`main()`を実行する |

### 実行方法

```bash
python 025_async/example/01_asyncio_basics/main.py
```

---

## 2. Flaskのasyncビューで外部APIを並行に呼ぶ

> [example/02_flask_async/app.py](example/02_flask_async/app.py)

`021_webapi`と同じzipcloud APIに対して、3件の郵便番号を検索します。同期版と非同期版を同じアプリに用意し、所要時間を比較します。

```bash
pip install flask asgiref httpx
```

Flaskで`async def`のビュー関数を使うには、`asgiref`のインストールが必要です（`pip install flask[async]`でもよい）。

### 同期版（021_webapiと同じ書き方）

`requests.get(url, params=辞書)`で外部APIにGETリクエストを送り、`res.json()`でレスポンス本文を辞書として受け取ります。

```python
import requests

@app.get('/sync')
def get_addresses_sync():
    results = []
    for zip_code in ZIP_CODES:
        res = requests.get("https://zipcloud.ibsnet.co.jp/api/search", params={"zipcode": zip_code})
        results.append(res.json())
    return jsonify({"results": results})
```

### 非同期版（httpx.AsyncClient + asyncio.gather）

```python
import asyncio
import httpx

async def fetch_address(client: httpx.AsyncClient, zip_code: str) -> dict:
    res = await client.get("https://zipcloud.ibsnet.co.jp/api/search", params={"zipcode": zip_code})
    return res.json()

@app.get('/async')
async def get_addresses_async():
    async with httpx.AsyncClient() as client:
        results = await asyncio.gather(*(fetch_address(client, z) for z in ZIP_CODES))
    return jsonify({"results": results})
```

`requests`は同期専用のライブラリなので、非同期版では**`httpx`**（非同期対応のHTTPクライアント）を使います。書き方は`requests`とよく似ていますが、`await client.get(...)`のように`await`を付けて呼び出します。

### 実測結果（3件の郵便番号を検索）

| エンドポイント | 所要時間 |
|---|---|
| `GET /sync` | 約1.1秒（1件ずつ順番に通信） |
| `GET /async` | 約0.4秒（3件同時に通信） |

同じ3件のAPI呼び出しでも、`asyncio.gather`で同時に実行すると**約1/3の時間**で終わることが実測できます。

### 実行方法

```bash
cd 025_async/example/02_flask_async
python app.py
```

```bash
curl http://127.0.0.1:5071/sync
curl http://127.0.0.1:5071/async
```

---

## 3. Flaskのasyncの限界

ここまでで「Flaskでも`async def`を使えば速くなる」ことを確認しましたが、これには**重要な条件**があります。

### 何が速くなったのか

上の実験で速くなったのは、**1回のリクエストの中で行う複数のI/O待ち**です。1人のユーザーが`/async`にアクセスしたとき、その1回のリクエストの中で3件のAPI呼び出しを同時に行えるので速くなりました。

### 何が速くならないのか

Flaskは**WSGI**という同期前提の仕組みの上で動いています。`async def`のビューを書いても、Flaskは内部で「そのリクエストのためだけに一時的なイベントループを作って実行し、終わったら閉じる」という変換を行っているだけです。そのため、**複数のユーザーから同時に来たリクエストを並行して処理する能力**は、`async def`にしても向上しません。

```
Flask（WSGI）:
  リクエストA ──▶ [ワーカー1] async def ビュー実行(内部で一時的にイベントループ) ──▶ レスポンス
  リクエストB ──▶ [ワーカー2] async def ビュー実行(別の一時的なイベントループ) ──▶ レスポンス
  → 同時に処理できる数は、相変わらずワーカー（スレッド/プロセス）の数で決まる

FastAPI（ASGI）:
  リクエストA ──┐
  リクエストB ──┼─▶ 1つのイベントループが複数リクエストのI/O待ちを効率的に裁く
  リクエストC ──┘
  → I/O待ちの間に他のリクエストの処理を進められる
```

### まとめ

| | Flask + async def | FastAPI（ASGI） |
|---|---|---|
| 1リクエスト内の複数I/O待ち（`asyncio.gather`など） | 速くなる（今回実験した通り） | 速くなる |
| 大量の同時アクセスをさばく能力 | 向上しない（WSGIのワーカー数に依存） | 向上する（ASGIが本来得意とする領域） |
| 必要な追加パッケージ | `asgiref` | 不要（標準でASGI） |

「1つのリクエストの中で複数のI/O待ちをまとめて速くしたい」ならFlaskの`async def`でも十分効果がありますが、「大量の同時アクセスを効率よくさばきたい」場合は、**ASGI対応のFastAPI**の方が本来の土俵です。

---

## 練習問題

> [question/](question/) — 問題（1問1ファイル） ｜ [question/answer/](question/answer/) — 解答

`question/questionN.py` を開き、コメントの指示に従ってコードを完成させてください。各ファイルは独立して実行できます。

```bash
pip install httpx
python 025_async/question/question01.py
```

#### 問題一覧

| 問題 | 内容 | ポイント | 解答 |
|---|---|---|---|
| 1 | 3つの`asyncio.sleep`タスクを直列実行と`asyncio.gather`での並列実行で比較し、所要時間の差を確認する | `asyncio.gather` | [question/answer/answer01.py](question/answer/answer01.py) |
| 2 | `asyncio.gather`の戻り値（渡した順番のリスト）を使う | `gather`の戻り値 | [question/answer/answer02.py](question/answer/answer02.py) |
| 3 | 一部のタスクが例外を送出しても、`return_exceptions=True`で他の結果を受け取る | `return_exceptions` | [question/answer/answer03.py](question/answer/answer03.py) |
| 4 | `httpx.AsyncClient`で複数の郵便番号を同時に検索する（インターネット接続が必要） | `httpx.AsyncClient` | [question/answer/answer04.py](question/answer/answer04.py) |

#### ヒント

- 問題1は`time.perf_counter()`で計測した時間そのものにアサーションを付けています。TODOを実装しないと`assert`が失敗するようになっているので、実装が終わるまでは失敗して当然です
- 問題4は本章セクション2の`example/02_flask_async/app.py`と同じ考え方を、Flaskを使わずスクリプト単体で実装したものです

## 次のステップ

ここまでで基本チャプターは一区切りです。続きは発展編の [100_bookstore_api](../100_bookstore_api) で、画像アップロード・カート・ロール管理・API連携を組み合わせたブックストアに挑戦します。
