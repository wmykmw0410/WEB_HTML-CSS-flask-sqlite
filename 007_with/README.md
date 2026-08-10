# 007 with 文

Python の `with` 文（コンテキストマネージャー）を学びます。
ファイル操作を題材に、リソースを安全に扱う書き方を身につけます。

各章は「機能の学習」と「`000_my_app`を完成させるための機能追加」の2部構成です。前者は`example/`で単体のサンプルとして学び、後者は`challenge/`でメモ帳アプリを組み立てながら取り組みます。

## フォルダ構成

```
007_with/
├── README.md
├── example/
│   ├── 01_file.py      ファイルの読み書き（with open）
│   ├── 02_why.py       なぜ with を使うか（try/finally との比較）
│   ├── 03_multiple.py  複数のリソースを同時に開く
│   ├── 04_path.py      パス操作（os.path / pathlib）
│   ├── 05_csv.py       CSV の読み書き
│   └── 06_json.py      JSON の読み書き
├── question/            # 練習問題（ファイル操作の総合ドリル、1問1ファイル）
│   ├── question01.py〜question08.py
│   └── answer/
│       └── answer01.py〜answer08.py
└── challenge/           # 006_jinja2の続き（000_my_appに組み込む機能の追加分）
    ├── challenge.py
    ├── memos.json       # 読み込むメモデータ
    ├── static/
    ├── templates/
    └── answer/
        ├── challenge.py
        ├── memos.json
        ├── static/
        └── templates/
```

---

## 1. with 文とは

`with` 文は、**ブロックに入るときの前処理**と**ブロックを抜けるときの後処理**を自動化する仕組みです。

```python
with 対象 as 変数名:
    # 変数名を使って処理
# ← ここでブロックを抜けると後処理が自動で実行される
```

- 正常終了でも例外が起きても、後処理は**必ず**実行される
- `as 変数名` は省略できる（後処理のみが目的で変数が不要なとき）

---

## 2. ファイル操作（with open）

> [example/01_file.py](example/01_file.py)

ファイルを開いたら最後に `close()` しなければなりませんが、`with` を使うと自動で閉じてくれます。

### 書き込み

```python
with open('sample.txt', 'w', encoding='utf-8') as f:
    f.write('1行目\n')
    f.write('2行目\n')
# ← f.close() が自動で呼ばれる
```

### 読み込み（全体）

```python
with open('sample.txt', encoding='utf-8') as f:
    content = f.read()       # ファイル全体を1つの文字列で取得
    print(content)
```

### 読み込み（行ごと）

```python
with open('sample.txt', encoding='utf-8') as f:
    for line in f:           # ファイルオブジェクトはそのまま繰り返せる
        print(line.rstrip()) # rstrip() で末尾の改行を除去
```

### ファイルモード一覧

| モード | 意味 |
|---|---|
| `'r'` | 読み込み（デフォルト） |
| `'w'` | 書き込み（上書き）。ファイルがなければ作成 |
| `'a'` | 追記。ファイルがなければ作成 |
| `'rb'` / `'wb'` | バイナリで読み込み / 書き込み |

### 動作確認：read()・readlines()・forループの出力の違いを見る

```bash
cd 007_with/example
python 01_file.py
```

| 確認する操作 | 確認したいこと |
|---|---|
| `python 01_file.py`を実行する | ターミナルに「書き込み完了」の後、`--- read()：全体 ---`の下に3行分の文字列が改行込みでまとめて表示される |
| `--- readlines()：リスト ---`の出力を見る | `['1行目\n', '2行目\n', '3行目\n']`のように、各要素に`\n`を含んだ**リスト**として表示される（`read()`の1つの文字列との違いを比較する） |
| `--- for ループ ---`の出力を見る | `1行目`・`2行目`・`3行目`が改行無しで1行ずつ表示される（`rstrip()`で末尾の`\n`が除去されているため） |
| 「追記後:」以降の出力を見る | 1〜3行目に加えて`4行目（追記）`が追加された4行が表示される（`'a'`モードで追記されたことを確認） |
| スクリプト終了後、`007_with/example/`フォルダを確認する | `sample.txt`が残っていない（スクリプト末尾の`os.remove(path)`で自動削除されるため。ファイルが消えているのは正常な後片付けで、バグではない） |

**正常な状態の見分け方**：`read()`は改行込みの1つの文字列、`readlines()`は改行込みの文字列のリスト、forループは`rstrip()`で改行を除いた文字列、という3通りの違いが出力から見分けられれば理解できています。

### 練習問題

1. `with open` で `memo.txt` に2行書き込んでください
2. `with open` で `memo.txt` を読み込み、行ごとに `print` してください

---

## 3. なぜ with を使うか

> [example/02_why.py](example/02_why.py)

`with` を使わずにファイルを操作すると、例外が起きたときに `close()` が呼ばれないままになります。

### with なし（危険）

```python
f = open('sample.txt')
content = f.read()
f.close()   # 例外が起きると、ここに到達しない
```

### try / finally（安全だが冗長）

```python
f = open('sample.txt')
try:
    content = f.read()
finally:
    f.close()   # 例外が起きても必ず実行される
```

### with（シンプルかつ安全）

```python
with open('sample.txt') as f:
    content = f.read()
# close() の書き忘れがなく、例外時も確実に閉じる
```

`with` は `try/finally` の前処理・後処理を内部でやっているのと同じです。

```
with 対象 as f:     →  f = 対象.__enter__()  ← 前処理
    処理               処理
                   →  対象.__exit__(...)      ← 後処理（例外の有無に関わらず実行）
```

### 動作確認：例外が起きてもwithが必ずcloseすることを確認する

```bash
cd 007_with/example
python 02_why.py
```

| 確認する操作 | 確認したいこと |
|---|---|
| `python 02_why.py`を実行する | `=== with なし ===`・`=== try / finally ===`・`=== with ===`の3つのセクションで、いずれも`読み込み: hello`が表示される（書き方が違うだけで結果自体は同じであることを確認する） |
| `=== 例外が起きたとき ===`以降の出力を見る | `例外発生。f.closed = True`と表示される。`with`ブロックの中で`ValueError`を発生させても、ブロックを抜けた時点でファイルが自動的に閉じられていることを`f.closed`で確認している |
| スクリプト終了後、`007_with/example/`フォルダを確認する | `why_sample.txt`が残っていない（末尾の`os.remove(path)`で削除される） |

**正常な状態の見分け方**：`f.closed`が`True`になっていれば、例外が起きても`with`が確実に`close()`を呼んでいる証拠です。`False`のままなら、`with`の対象がファイルオブジェクトになっていない、または例外処理の書き方に問題がある可能性を疑ってください。

### 練習問題

1. 次のコードを `with` を使って書き直してください

```python
f = open('data.txt', 'w')
f.write('hello')
f.close()
```

---

## 4. 複数のリソースを同時に開く

> [example/03_multiple.py](example/03_multiple.py)

1行の `with` で複数のリソースを同時に開けます。

```python
# カンマ区切りで複数のコンテキストマネージャーを並べる
with open('input.txt', encoding='utf-8') as f_in, \
     open('output.txt', 'w', encoding='utf-8') as f_out:
    for line in f_in:
        f_out.write(line.upper())   # 大文字に変換して書き込む
```

ネストして書く方法もありますが、1行にまとめる方が簡潔です。

```python
# ネスト（同じ動作だが読みにくい）
with open('input.txt') as f_in:
    with open('output.txt', 'w') as f_out:
        ...
```

### as なし

コンテキストマネージャーを使いたいが変数が不要なケースでは `as` を省略できます。

```python
import contextlib

with contextlib.suppress(FileNotFoundError):
    os.remove('maybe_exists.txt')   # ファイルがなくてもエラーにならない
```

### 動作確認：1行withとネストで結果がどう変わるか

```bash
cd 007_with/example
python 03_multiple.py
```

| 確認する操作 | 確認したいこと |
|---|---|
| `python 03_multiple.py`を実行する | `=== 1行の with で2ファイルを同時に開く ===`の下に、`input.txt`の内容（`apple`・`banana`・`cherry`）がすべて**大文字**（`APPLE`・`BANANA`・`CHERRY`）になって表示される |
| `=== ネスト（同じ動作だが読みにくい）===`の下の出力を見る | 今度はすべて**小文字**（`apple`・`banana`・`cherry`）になって表示される（`f_out.write(line.lower())`のため） |
| `=== as なし（変数が不要なとき）===`の下の出力を見る | 「ファイルがなくてもエラーにならなかった」と表示される（存在しない`not_exist.txt`を`os.remove`しても`contextlib.suppress(FileNotFoundError)`で例外が握りつぶされるため） |
| スクリプト終了後、`007_with/example/`フォルダを確認する | `input.txt`・`output.txt`のどちらも残っていない（末尾の`os.remove`で削除される） |

**正常な状態の見分け方**：同じ`input.txt`を読んでいるのに、1行のwith（大文字）とネスト（小文字）で結果の大文字・小文字が違って出力されるのが正しい挙動です（`upper()`と`lower()`を呼び分けているだけで、複数リソースを扱えていること自体は同じ）。

### 練習問題

1. `original.txt` に3行書き込んでください
2. `original.txt` を読み込んで `copy.txt` にコピーしてください（1行の `with` で2ファイルを同時に開く）
3. `copy.txt` を読み込んで全行を `print` し、内容が同じか確認してください

---

## 5. パス操作（os.path / pathlib）

> [example/04_path.py](example/04_path.py)

ファイルパスを組み立てたり分解したりするための標準モジュールです。

### os.path

```python
import os

# __file__ は実行中のスクリプト自身のパス
base_dir = os.path.dirname(__file__)          # 親ディレクトリ
name     = os.path.basename(__file__)         # ファイル名だけ
path     = os.path.join(base_dir, 'data.txt') # パスを連結

stem, ext = os.path.splitext('report.csv')   # 名前と拡張子を分離
# → stem='report', ext='.csv'

os.path.exists(path)   # ファイル / ディレクトリが存在するか
os.path.isfile(path)   # ファイルか
os.path.isdir(path)    # ディレクトリか
```

| 関数 | 説明 |
|---|---|
| `os.path.dirname(p)` | 親ディレクトリを返す |
| `os.path.basename(p)` | ファイル名（末尾）を返す |
| `os.path.join(a, b, ...)` | パスを連結する |
| `os.path.splitext(p)` | `(名前, 拡張子)` のタプルを返す |
| `os.path.exists(p)` | 存在すれば `True` |

### pathlib.Path（モダンな書き方）

Python 3.4 以降で使える、オブジェクト指向スタイルのパス操作です。

```python
from pathlib import Path

p = Path(__file__)

p.parent    # 親ディレクトリ（os.path.dirname 相当）
p.name      # ファイル名（os.path.basename 相当）
p.stem      # 拡張子なしのファイル名
p.suffix    # 拡張子（'.py'）
p.exists()  # 存在確認

# / 演算子でパスを連結できる（os.path.join より直感的）
child = p.parent / 'data' / 'sample.txt'

# ディレクトリ内のファイル一覧
for item in p.parent.iterdir():
    print(item.name)

# 拡張子でフィルタ
py_files = list(p.parent.glob('*.py'))
```

### os.path と pathlib の使い分け

| | `os.path` | `pathlib.Path` |
|---|---|---|
| スタイル | 関数型 | オブジェクト指向 |
| パスの連結 | `os.path.join(a, b)` | `a / b` |
| 既存コードの多さ | 多い | 近年増えている |
| おすすめ | 既存コードとの互換 | 新規に書くとき |

### 動作確認：os.pathとpathlib.Pathが同じ結果を返すことを確認する

```bash
cd 007_with/example
python 04_path.py
```

| 確認する操作 | 確認したいこと |
|---|---|
| `python 04_path.py`を実行する | `=== os.path ===`の下で、`dirname`は`04_path.py`が置かれているディレクトリの絶対パス、`basename`は`04_path.py`という値になる |
| `splitext`の行を見る | `name=report, ext=.csv`と表示される（名前と拡張子が分離されている） |
| `exists(存在しないパス)`の行を見る | `False`と表示される（`/no/such/path`は実在しないため） |
| `=== pathlib.Path ===`以降の出力を見る | `.parent`・`.name`の値が、直前の`os.path`の`dirname`・`basename`と**それぞれ同じ値**になり、`.stem`は`04_path`、`.suffix`は`.py`になる |
| `=== ディレクトリ操作 ===`以降の出力を見る | `example/`フォルダ内のファイル一覧が表示され、最後に`.py ファイル数`として`6`（`01_file.py`〜`06_json.py`の数）が表示される |

**正常な状態の見分け方**：`os.path`で得た値と`pathlib.Path`で得た値（`dirname`↔`.parent`、`basename`↔`.name`）が一致していれば、書き方が違うだけで同じパス情報を扱えていることが確認できます。

### 練習問題

1. `os.path.dirname(__file__)` と `os.path.basename(__file__)` を表示してください
2. `os.path.join` で `base_dir / 'data' / 'test.txt'` を組み立ててください
3. `pathlib.Path` で同じパスを `parent / 'data' / 'test.txt'` で組み立ててください
4. `os.path.splitext('image.png')` を実行して名前と拡張子を表示してください

---

## 6. CSV の読み書き

> [example/05_csv.py](example/05_csv.py)

CSV（Comma-Separated Values）はスプレッドシートやデータ交換でよく使われる形式です。
Python 標準の `csv` モジュールで読み書きできます。

### 書き込み（csv.writer）

```python
import csv

with open('items.csv', 'w', encoding='utf-8', newline='') as f:
    # newline='' を指定しないと Windows で改行が二重になる
    writer = csv.writer(f)
    writer.writerow(['id', 'name', 'price'])   # 1行書き込む
    writer.writerows([                          # 複数行まとめて書き込む
        [1, 'りんご', 150],
        [2, 'バナナ', 120],
    ])
```

### 読み込み（csv.reader）

```python
with open('items.csv', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)   # ['id', 'name', 'price'] / ['1', 'りんご', '150']
        # 数値も文字列として読まれる → int(row[2]) で変換
```

### 辞書形式（DictReader / DictWriter）

```python
# 読み込み：1行目をヘッダーとして自動認識し、辞書で取得
with open('items.csv', encoding='utf-8') as f:
    for row in csv.DictReader(f):
        print(row['name'], row['price'])   # カラム名でアクセス

# 書き込み：辞書のリストを書き込む
fields = ['id', 'name', 'price']
with open('items.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()
    writer.writerows([{'id': 1, 'name': 'りんご', 'price': 150}])
```

| クラス | 戻り値 / 入力 | 用途 |
|---|---|---|
| `csv.reader` | リスト | シンプルな読み込み |
| `csv.writer` | — | シンプルな書き込み |
| `csv.DictReader` | 辞書 | カラム名でアクセスしたい |
| `csv.DictWriter` | 辞書 | 辞書のリストを書き込みたい |

### 動作確認：reader/DictReaderで読んだ値の型・形の違いを見る

```bash
cd 007_with/example
python 05_csv.py
```

| 確認する操作 | 確認したいこと |
|---|---|
| `python 05_csv.py`を実行する | `=== CSV 書き込み ===`の下に「（パス）を作成しました」と表示される |
| `=== csv.reader（リスト形式）===`の出力を見る | `['id', 'name', 'price']`のヘッダー行に続き、`['1', 'りんご', '150']`のように**値がすべて文字列**として読み込まれている（`150`ではなく`'150'`であることに注目） |
| `=== csv.DictReader（辞書形式）===`の出力を見る | `id=1  りんご  150円`のように、カラム名でアクセスした値が1行ずつ表示される |
| `=== csv.DictWriter（辞書形式）===`の出力を見る | `id,name,price`のヘッダーの後に`1,コーヒー,200`・`2,紅茶,180`の2行が表示される |
| スクリプト終了後、`007_with/example/`フォルダを確認する | `items.csv`・`items2.csv`のどちらも残っていない（末尾の`os.remove`で削除される） |

**正常な状態の見分け方**：`csv.reader`で読んだ値がクォート無しでも文字列型（`str`）であることに気づければ理解できています。数値として計算に使いたい場合は`int()`などで明示的に変換する必要がある、という点が重要です。

### 練習問題

1. `csv.writer` で `members.csv`（id / name / age）を3件書き込んでください
2. `csv.reader` で読み込んで全行を `print` してください
3. `csv.DictReader` で読み込んで `name` だけを表示してください

---

## 7. JSON の読み書き

> [example/06_json.py](example/06_json.py)

JSON（JavaScript Object Notation）は API レスポンスや設定ファイルで広く使われる形式です。
Python の辞書・リストと相互に変換できます。

### ファイルへの書き込み（json.dump）

```python
import json

data = {
    'name': '山田太郎',
    'age': 30,
    'skills': ['Python', 'Flask'],
}

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
    # ensure_ascii=False : 日本語をそのまま出力
    # indent=2           : 読みやすくインデント
```

### ファイルからの読み込み（json.load）

```python
with open('data.json', encoding='utf-8') as f:
    loaded = json.load(f)   # dict として返る

print(loaded['name'])           # 山田太郎
print(loaded['skills'][0])      # Python
```

### 文字列との相互変換（dumps / loads）

ファイルを介さずに dict ↔ JSON 文字列を変換します。

```python
# dict → JSON 文字列
json_str = json.dumps(data, ensure_ascii=False)

# JSON 文字列 → dict
parsed = json.loads(json_str)
```

| 関数 | 方向 | 対象 |
|---|---|---|
| `json.dump(obj, f)` | dict → ファイル | ファイルに書き込む |
| `json.load(f)` | ファイル → dict | ファイルから読み込む |
| `json.dumps(obj)` | dict → 文字列 | 文字列に変換 |
| `json.loads(s)` | 文字列 → dict | 文字列から変換 |

### 動作確認：ensure_asciiの有無で出力がどう変わるか

```bash
cd 007_with/example
python 06_json.py
```

| 確認する操作 | 確認したいこと |
|---|---|
| `python 06_json.py`を実行する | `=== json.dump（ファイルに書き込む）===`の下に、`data.json`の中身がインデント付きで表示される。`"name": "山田太郎"`のように**日本語がそのまま**出力されている（`ensure_ascii=False`の効果。`True`だと`山...`のような文字コード表記になる） |
| `=== json.load（ファイルから読み込む）===`の出力を見る | `name`・`skills`・`city`（ネストした`address`辞書の中の値）がそれぞれ正しく取り出されて表示される |
| `=== json.dumps / json.loads ===`の出力を見る | `json.dumps`の行はJSON文字列の先頭部分、`json.loads`の行は文字列から辞書に戻した`name`の値（`山田太郎`）が表示される |
| スクリプト終了後、`007_with/example/`フォルダを確認する | `data.json`が残っていない（末尾の`os.remove`で削除される） |

**正常な状態の見分け方**：`ensure_ascii=False`を付けたときだけ日本語がそのまま読める形で出力されるのが正しい挙動です。`\uXXXX`のような文字コードの羅列になっている場合は`ensure_ascii`の設定を疑ってください。

### Python ↔ JSON の型対応

| Python | JSON |
|---|---|
| `dict` | `{}` オブジェクト |
| `list` | `[]` 配列 |
| `str` | `"文字列"` |
| `int` / `float` | 数値 |
| `True` / `False` | `true` / `false` |
| `None` | `null` |

### 練習問題

1. `{'title': 'Python入門', 'price': 2800, 'tags': ['入門', 'プログラミング']}` を `book.json` に書き込んでください
2. `book.json` を読み込んで `title` と `tags` を表示してください
3. `json.dumps` で dict を JSON 文字列に変換し、`json.loads` で元に戻してください

---

## 8. 練習問題

> [question/](question/) — 問題（1問1ファイル） ｜ [question/answer/](question/answer/) — 解答

### 問題：ファイル操作を総合的に練習しよう

`question/questionN.py` を開き、コメントの指示に従ってコードを完成させてください。

```bash
python 007_with/question/question01.py
```

#### 問題一覧

| 問題 | 内容 | ポイント | 解答 |
|---|---|---|---|
| 1 | `log.txt` にログを3行書き込む | `with open ... 'w'` | [question/answer/answer01.py](question/answer/answer01.py) |
| 2 | `log.txt` を読み込んで行番号付きで表示する | `with open ... enumerate` | [question/answer/answer02.py](question/answer/answer02.py) |
| 3 | `log.txt` に1行追記する | `'a'` モード | [question/answer/answer03.py](question/answer/answer03.py) |
| 4 | `log.txt` と `log_backup.txt` を同時に開いて内容をコピーする | 複数コンテキストマネージャー | [question/answer/answer04.py](question/answer/answer04.py) |
| 5 | try/finally で書かれたコードを with で書き直す | try/finally → with | [question/answer/answer05.py](question/answer/answer05.py) |
| 6 | `os.path` と `pathlib.Path` でパスを操作する | `dirname` / `basename` / `stem` / `suffix` | [question/answer/answer06.py](question/answer/answer06.py) |
| 7 | `products.csv` を書き込んで `DictReader` で読み込む | `csv.writer` / `csv.DictReader` | [question/answer/answer07.py](question/answer/answer07.py) |
| 8 | `config.json` を書き込んで `json.load` で読み込む | `json.dump` / `json.load` | [question/answer/answer08.py](question/answer/answer08.py) |

### 動作確認：正しく実装できたかを確認する

```bash
cd 007_with/question
python question01.py
```

| 確認する操作 | 確認したいこと |
|---|---|
| 各`questionN.py`を実行する | エラーで途中終了せず、末尾の「問題N: ...」というメッセージまで到達する（`with`の書き方を間違えると`NameError`や`AttributeError`で途中で止まる） |
| 実行前に、確認したい`questionN.py`の末尾にある`os.remove(...)`の行を一時的にコメントアウトしてから実行する | `log.txt`・`products.csv`・`config.json`などの生成ファイルが削除されずに残るので、エディタで開いて中身を直接確認できる（通常はスクリプトの最後で自動削除されるため、そのままでは実行後にファイルが残らない） |
| [question/answer/answerN.py](question/answer/) を実行し、自分の`questionN.py`の出力と見比べる | ターミナルに表示される行数・内容が一致する |

**正常な状態の見分け方**：どの問題も、実行後にエラーメッセージが出ずに末尾の「問題N: ...」のprintまで到達していれば、`with`の書き方は正しく機能しています。

---

## 9. 練習問題：メモデータをJSONファイルから読み込もう

> [challenge/challenge.py](challenge/challenge.py) — 問題 ｜ [challenge/answer/challenge.py](challenge/answer/challenge.py) — 解答

### 問題：memos.jsonからメモデータを読み込むようにしよう

`006_jinja2`で作ったメモ一覧・詳細ページ・リダイレクト（`challenge/challenge.py`にすでに実装済み）は、これまで`memos`辞書をPythonのコードにハードコードしていました。これを`memos.json`ファイルから読み込むように変更します。

実はこの先の章（`011_sqlite`の`challenge`など）でも、まったく同じやり方で`memos.json`からメモデータを読み込んでいます。

```python
json_path = os.path.join(os.path.dirname(__file__), 'data', 'memos.json')
with open(json_path, encoding='utf-8') as f:
    memos_data = json.load(f)
```

```bash
python 007_with/challenge/challenge.py
```

#### 仕様

| 項目 | 内容 |
|---|---|
| 読み込み元 | `challenge/memos.json`（`title`・`category`・`body`を持つオブジェクトのリスト） |
| 変換後の形 | これまでと同じ`{1: {...}, 2: {...}, ...}`という、idをキーにした辞書 |
| 画面の見た目 | `006_jinja2`のときと完全に同じ（データの取得方法だけが変わる） |

#### ヒント

- `os.path.join(os.path.dirname(__file__), 'memos.json')`で、このファイルと同じディレクトリの`memos.json`のパスを組み立てる（`5. パス操作`）
- `with open(パス, encoding='utf-8') as f:`で開く（`2. ファイル操作`）
- `json.load(f)`でリストとして読み込む（`7. JSONの読み書き`）
- `{i + 1: memo for i, memo in enumerate(リスト)}`のような辞書内包表記で、リストのインデックス（0始まり）を1始まりのidに変換する
- Python側の変更だけで完結します。`templates/`はこの章では変更しません

### 動作確認：memos.jsonの中身がそのまま画面に出ているか

```bash
python 007_with/challenge/challenge.py
```

| 確認する操作 | 確認したいこと |
|---|---|
| `http://127.0.0.1:5016/`にアクセスする | `006_jinja2`のときと同じ5枚のメモカードが表示される（データの取得元がPythonのハードコードから`memos.json`に変わっただけで、画面の見た目は変わらない） |
| `challenge/memos.json`をエディタで直接開く | 表示されているメモのタイトル・カテゴリ・本文が、このファイルの中身とそのまま一致している |
| `memos.json`の`title`の値を書き換えて保存し、`challenge.py`を再起動する | 一覧ページのタイトル表示が書き換えた内容に変わる（`memos`辞書が起動のたびにファイルから読み込まれていることを確認できる） |
| `http://127.0.0.1:5016/memos/2`にアクセスする | `memos.json`の2番目の要素（企画会議メモ、カテゴリ「仕事」）の内容が表示される |

**正常な状態の見分け方**：`memos.json`を書き換えてアプリを再起動すると画面の表示も連動して変わるなら、データがファイルから正しく読み込まれています。書き換えても画面が変わらない場合は、どこかにまだハードコードされたデータが残っていないか疑ってください。
