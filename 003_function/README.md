# 003 関数とデコレータ

Pythonの関数の基本（定義・呼び出し・引数・戻り値・スコープ）を学んだ上で、`@app.route()`の仕組みを理解するためのPythonデコレータを段階的に学びます。Flaskはまだ使いません。

## 目次

1. [組み込み関数（built-in functions）](#1-組み込み関数built-in-functions)
2. [関数の定義と呼び出し](#2-関数の定義と呼び出し)
3. [引数の種類](#3-引数の種類)
4. [戻り値の詳細](#4-戻り値の詳細)
5. [Noneとは](#5-noneとは)
6. [変数のスコープ](#6-変数のスコープ)
7. [関数はオブジェクト](#7-関数はオブジェクト) — 関数をオブジェクトとして扱う
8. [関数内関数（クロージャ）](#8-関数内関数クロージャ)
9. [デコレータ構文（@）](#9-デコレータ構文)
10. [可変長引数付きデコレータ](#10-可変長引数付きデコレータ)
11. [練習問題](#11-練習問題)

---

## フォルダ構成

```
003_function/
├── README.md
├── example/
│   ├── ex01.py   # 位置引数・キーワード引数
│   ├── ex02.py   # デフォルト引数
│   ├── ex03.py   # 可変長位置引数（*args）・可変長キーワード引数（**kwargs）
│   ├── ex04.py   # ローカル変数
│   ├── ex05.py   # グローバル変数
│   ├── ex06.py   # global宣言
│   ├── ex07.py   # 関数を引数に渡す
│   ├── ex08.py   # 関数は第一級オブジェクト
│   ├── ex09.py   # 関数内関数（クロージャ）
│   ├── ex10.py   # デコレータ構文（@）
│   └── ex11.py   # 可変長引数付きデコレータ
└── question/                 # 練習問題（関数1〜4、デコレータ5〜6）
    ├── question1.py〜question6.py
    └── answer/answer1.py〜answer6.py
```

---

## 1. 組み込み関数（built-in functions）

Pythonインタプリタが最初から用意している関数で、importせずにそのまま使えます。

| 関数名 | 概要 | 使用例 |
|---|---|---|
| `print()` | 画面に出力する | `print("Hello")` |
| `len()` | 要素数を返す | `len("abc")` → 3 |
| `type()` | データ型を返す | `type(123)` → `<class 'int'>` |
| `int()` | 整数に変換 | `int("10")` → 10 |
| `str()` | 文字列に変換 | `str(100)` → `"100"` |
| `list()` | リストに変換 | `list("abc")` → `['a','b','c']` |
| `range()` | 整数の範囲を生成（for文でよく使用） | `range(3)` → 0,1,2 |
| `sum()` | 合計を計算 | `sum([1, 2, 3])` → 6 |
| `max()` | 最大値を返す | `max([1, 5, 3])` → 5 |
| `min()` | 最小値を返す | `min([1, 5, 3])` → 1 |
| `abs()` | 絶対値を返す | `abs(-5)` → 5 |
| `input()` | 入力を受け取る（文字列） | `input("名前は？")` |

全部で70個以上あります。

```python
# 一覧の確認方法
import builtins
print(dir(builtins))
```

---

## 2. 関数の定義と呼び出し

```python
def func_name(arg1, arg2, ...):
    # process
    return return_value
```

| キーワード | 意味 |
|---|---|
| `def` | define（定義する） |
| `func_name` | スネークケースで記載する |
| `(arg1, arg2, ...)` | 引数（省略可） |
| `return return_value` | 戻り値（省略可。省略時は`None`が返される） |

### 命名のスタイル

| 用途 | 命名スタイル | 例 |
|---|---|---|
| 変数名 | スネークケース（小文字＋アンダースコア） | `user_name` |
| 関数名 | スネークケース | `calc_sum()` |
| クラス名 | キャメルケース（単語の先頭が大文字） | `MyClass` |
| 定数 | アッパーケース＋`_` | `MAX_SPEED`, `PI` |
| 特殊メソッド | ダブルアンダースコア（ダンダー） | `__init__` |

### 関数の呼び出し方

> [example/ex01.py](example/ex01.py)

```python
def add(a, b):
    print(a + b)

add(1, 2)
add(a=1, b=2)  # キーワード指定も可能
add(b=2, a=1)  # キーワード指定は順不同でも可
```

### 実行方法

```bash
python 003_function/example/ex01.py
```

---

## 3. 引数の種類

> [example/ex02.py](example/ex02.py)（デフォルト引数） | [example/ex03.py](example/ex03.py)（可変長位置引数・可変長キーワード引数）

| 種類 | 書き方 | 説明 | 例 |
|---|---|---|---|
| 位置引数 | `def func(a, b)` | 順番で渡す | `func(1, 2)` |
| デフォルト引数 | `def func(a=10)` | 省略可能。右側から指定する | `func()` → a=10 |
| キーワード引数 | `def func(a, b)` | 名前を指定して渡す（順番不問） | `func(b=2, a=1)` |
| 可変長位置引数 | `def func(*args)` | 複数の位置引数をタプルで受け取る | `func(1, 2, 3)` |
| 可変長キーワード引数 | `def func(**kwargs)` | 複数のキーワード引数を辞書で受け取る | `func(x=1, y=2)` |
| キーワード専用引数 | `def func(*, a)` | `*`より後はキーワード指定のみ | `func(a=1)` |
| 位置専用引数 | `def func(a, /)` | `/`より前は位置引数のみ | `func(1)` |

```python
# デフォルト引数
def add1(a=1, b=2):
    print(a + b)

add1()      # 3（両方デフォルト値）
add1(3, 2)  # 5

# デフォルト引数は右側から準備する（下記はSyntaxError）
# def add(a=1, b):
#     print(a + b)
```

```python
# 可変長位置引数（*args） — 複数の位置引数をタプルとして受け取る
def show_args(*args):
    print(args)

show_args(1, 2, 3)  # (1, 2, 3)

# 可変長キーワード引数（**kwargs） — 複数のキーワード引数を辞書として受け取る
def show_kwargs(**kwargs):
    print(kwargs)

show_kwargs(x=1, y=2)  # {'x': 1, 'y': 2}
```

> 練習問題：可変長位置引数は[question/question3.py](question/question3.py)、可変長キーワード引数は[question/question4.py](question/question4.py)で扱います（解答は[question/answer/](question/answer/)）。

### 実行方法

```bash
python 003_function/example/ex02.py
python 003_function/example/ex03.py
```

---

## 4. 戻り値の詳細

### 複数の値を返す

```python
def min_max(numbers):
    return min(numbers), max(numbers)  # タプルとして返される

lo, hi = min_max([3, 1, 4, 1, 5])
print(lo, hi)  # 出力: 1 5
```

### 早期return

条件を満たさない場合に関数を早く抜けます。

```python
def divide(a, b):
    if b == 0:
        return None  # 早期returnでゼロ除算を防ぐ
    return a / b
```

### Noneが返る条件

`return`を書かない、または`return`だけ書いた場合は`None`が返ります。

```python
def greet(name):
    print(f"Hello, {name}")  # returnなし

result = greet("Alice")
print(result)  # 出力: None
```

---

## 5. Noneとは

`None`はPythonの特殊な値で「何もない」「値が存在しない」ことを表します。

```python
x = None
print(x)        # 出力: None
print(type(x))  # 出力: <class 'NoneType'>
```

| 項目 | 内容 |
|---|---|
| 型 | `NoneType` |
| 真偽値 | `False`として扱われる |
| 比較 | `== None`より`is None`を使うのが慣例 |

```python
result = None

if result is None:
    print("値がありません")

if result is not None:
    print("値があります")
```

### Noneと空リスト`[]`の違い

どちらも「何もない」ように見えますが意味が異なります。

| | `None` | `[]` |
|---|---|---|
| 意味 | 値そのものが存在しない | リストは存在するが中身が空 |
| 型 | `NoneType` | `list` |
| 要素追加 | できない（エラー） | `append()`で追加できる |
| よく使う場面 | 関数が値を返せなかった時 | これから要素を追加する予定のリスト |

### 関数の使い方がわからない時

```python
help(関数名)          # 例: help(print)
print(関数名.__doc__)  # 例: print(len.__doc__)
```

---

## 6. 変数のスコープ

### ローカル変数（local variable）

> [example/ex04.py](example/ex04.py)

```python
def greet():
    name = "Alice"  # ローカル変数: 関数の中でのみ有効
    print("Hello,", name)

greet()
# print(name)  # エラー！関数の外からはアクセスできない
```

### グローバル変数（global variable）

> [example/ex05.py](example/ex05.py)

```python
message = "こんにちは"  # グローバル変数: プログラム全体で有効

def greet():
    print(message)  # 関数の中から参照できる

greet()  # 出力: こんにちは
```

関数の中でグローバル変数を**変更**するには`global`宣言が必要です。

> [example/ex06.py](example/ex06.py)

```python
count = 0

def increment():
    global count   # globalをつけないとUnboundLocalError
    count += 1

increment()
print(count)  # 出力: 1
```

### グローバル変数を避けるべき理由

| 理由 | 説明 |
|---|---|
| 予測しにくい | どこからでも変更できるため、バグの原因になりやすい |
| テストがしづらい | 特定の値に依存した関数は再利用性が下がる |
| 可読性が低くなる | 外部の変数が関数に影響することで、理解しにくいコードになる |

### 実行方法

```bash
python 003_function/example/ex04.py
python 003_function/example/ex05.py
python 003_function/example/ex06.py
```

---

## 7. 関数はオブジェクト

> [example/ex07.py](example/ex07.py) | [example/ex08.py](example/ex08.py)

ここから先は、`@app.route()`のようなデコレータの仕組みを理解するための内容です。Pythonでは関数もオブジェクトであり、変数への代入や引数として渡すことができます。

**example/ex07.py** — 関数を引数として受け取り実行する

```python
def a():
    print("A")

def b(func):
    print("---Start---")
    func()          # 引数として受け取った関数を実行
    print("---End---")

b(a)
```

**example/ex08.py** — 関数は第一級オブジェクト

```python
# ポイント1：関数は変数に代入できる
x = a       # () を付けない → 関数オブジェクトを代入
print(x)    # <function a at 0x...>
x()         # A

# ポイント2：関数オブジェクトの情報を確認する
print(a)    # <function a at 0x...>

# ポイント3：print(a) と print(a()) の違い
print(a)    # 関数オブジェクトそのものを表示
print(a())  # a() を実行 → 戻り値 None を表示
```

| 書き方 | 動作 |
|---|---|
| `x = a` | 関数オブジェクトを変数に代入（実行しない） |
| `x = a()` | 関数を実行してその戻り値を代入 |
| `b(a)` | 関数オブジェクトを引数として渡す |
| `b(a())` | 関数を実行した戻り値を引数として渡す |

### 用語：第一級オブジェクト・高階関数

| 用語 | 説明 |
|---|---|
| **第一級オブジェクト** | 変数への代入・引数への受け渡し・戻り値として返すことができる値。Pythonの関数は第一級オブジェクト |
| **高階関数** | 関数を引数として受け取ったり、戻り値として返したりする関数 |

### 実行方法

```bash
python 003_function/example/ex07.py
python 003_function/example/ex08.py
```

---

## 8. 関数内関数（クロージャ）

> [example/ex09.py](example/ex09.py)

関数の中に関数を定義し、それを戻り値として返すクロージャのパターンです。

### なぜ「関数を返す」必要があるのか

`7. 関数はオブジェクト`の`b(func)`は関数を受け取って**その場で実行**していました。これでは`b(a)`を呼んだ瞬間しか前後処理を挟めません。

```python
# 7 の方法：呼び出すたびに b() を経由する必要がある
b(a)   # ---Start--- A ---End---
a()    # A（前後処理なし）
```

`a()`を呼ぶだけで常に前後処理が実行されるようにするには、`a`自体を「前後処理付きの新しい関数」に置き換える必要があります。そのために「関数を返す」パターンを使います。

```python
def outer(func):
    def inner():
        print("---Start---")
        func()
        print("---End---")
    return inner         # inner 関数を返す（実行はしない）

result = outer(a)        # result = inner（前後処理付きの新しい関数）
result()                 # ---Start--- A ---End---
a = outer(a)             # a 自体を置き換えれば a() だけで前後処理が走る
```

### 用語：クロージャ

| 用語 | 説明 |
|---|---|
| **クロージャ** | 外側の関数の変数（ここでは`func`）を記憶しながら、内側の関数を戻り値として返すパターン |

`outer(a)`を呼ぶと`inner`関数が返ります。`inner`は`func`（= `a`）を覚えたまま後から実行できます。これがデコレータの核心的な仕組みです。

### 実行方法

```bash
python 003_function/example/ex09.py
```

---

## 9. デコレータ構文（@）

> [example/ex10.py](example/ex10.py)

クロージャを`@`構文で簡潔に書いたものがデコレータです。`@app.route()`の仕組みと同じです。

```python
@outer
def a():
    print("A")

# 上記は以下と同等
# a = outer(a)
```

### 用語：デコレータ・シンタックスシュガー

| 用語 | 説明 |
|---|---|
| **デコレータ** | 関数に処理を追加・変更する仕組み。`@関数名`の形で適用する |
| **シンタックスシュガー** | 同じ動作をより簡潔に書けるようにした構文。`@outer`は`a = outer(a)`の糖衣構文 |

`@app.route("/")`も同じ仕組みで、Flaskがビュー関数をラップしてルーティング情報を登録しています。

### 実行方法

```bash
python 003_function/example/ex10.py
```

---

## 10. 可変長引数付きデコレータ

> [example/ex11.py](example/ex11.py)

`*args` / `**kwargs`を使い、任意の引数を持つ関数にも対応したデコレータです。

```python
def outer(func):
    def inner(*args, **kwargs):
        print("---Start---")
        func(*args, **kwargs)
        print("---End---")
    return inner
```

`inner`が`*args` / `**kwargs`を受け取ることで、引数の数や種類を問わず任意の関数に適用できる汎用デコレータになります。

### 実行方法

```bash
python 003_function/example/ex11.py
```

---

## 11. 練習問題

> [question/](question/) — 問題（question1.py〜question6.py） ｜ [question/answer/](question/answer/) — 解答

### 関数の練習問題

| # | 問題 | 扱う内容 |
|---|---|---|
| 1 | 名前を受け取ってあいさつを表示する関数を作る（デフォルト値"ゲスト"） | デフォルト引数 |
| 2 | `show_info`を正しい引数の順序で呼び出す | 位置引数・キーワード引数 |
| 3 | 複数の食べ物リストを表示する関数を作る | 可変長位置引数（`*args`） |
| 4 | ユーザー情報のキーと値を表示する関数を作る | 可変長キーワード引数（`**kwargs`） |

### デコレータの練習問題

| # | 問題 | 扱う内容 |
|---|---|---|
| 5 | `greet`関数の前後に`=== 開始 ===`・`=== 終了 ===`を出力するデコレータ`log`を作る | デコレータの基本 |
| 6 | `add`・`multiply`の両方に使い回せる、結果を表示するデコレータ`show_result`を作る | 可変長引数付きデコレータ |

#### 問題5：[question/question5.py](question/question5.py)

`greet`関数を実行したとき、出力結果が下記になるようにデコレータ`log`を作成してください。

**期待する出力：**

```
=== 開始 ===
Hello!
=== 終了 ===
```

解答例 → [question/answer/answer5.py](question/answer/answer5.py)

#### 問題6：[question/question6.py](question/question6.py)

`add`関数と`multiply`関数の両方に適用できるデコレータ`show_result`を作成してください。

**期待する出力：**

```
add の結果 → 8
multiply の結果 → 15
```

解答例 → [question/answer/answer6.py](question/answer/answer6.py)
