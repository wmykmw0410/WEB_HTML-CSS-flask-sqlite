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

### 動作確認：組み込み関数の挙動をその場で試す

```bash
python3 -c "print(len('abc')); print(type(123)); print(sum([1, 2, 3]))"
```

| 確認する操作 | 確認したいこと |
|---|---|
| 上記コマンドを実行する | ターミナルに`3`・`<class 'int'>`・`6`の3行が順番に表示される |
| `import builtins; print(dir(builtins))`を実行する | `'print'`・`'len'`・`'sum'`など、上の表に出てきた関数名を含む長いリストが表示される |

**正常な状態の見分け方**：`print()`のように何も返さない関数はターミナルに直接出力されますが、`len()`や`sum()`は**戻り値**を返すだけなので、`print()`で包まないと画面には何も表示されません。この違いが体感できていればOKです。

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

### 動作確認：3通りの呼び出し方が同じ結果になるか

| 確認する操作 | 確認したいこと |
|---|---|
| `ex01.py`を実行する | ターミナルに`3`が**3行**表示される（`add(1, 2)`・`add(a=1, b=2)`・`add(b=2, a=1)`のいずれも同じ結果になる） |
| コメントアウトされている`add(b=2, 1)`を有効にして実行する | 実行前（構文解析の時点）で`SyntaxError`になる（キーワード引数の後に位置引数を置けないため） |

**正常な状態の見分け方**：引数の渡し方（位置指定・キーワード指定・キーワードの順不同）を変えても結果が変わらないことが正しい挙動です。

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

### 動作確認：省略した引数がどう補われるか

| 確認する操作 | 確認したいこと |
|---|---|
| `ex02.py`を実行する | `add1()`（両方省略）で`3`、`add1(3, 2)`（両方指定）で`5`、`add2(3)`（`b`省略）と`add2(a=3)`（同じく`b`省略）がどちらも`5`と表示される（デフォルト引数は指定しなかった分だけデフォルト値で補われる） |
| `ex03.py`を実行する | `show_args(1, 2, 3)`で`(1, 2, 3)`と`<class 'tuple'>`、`show_args()`（引数なし）で空タプル`()`が表示される |
| `ex03.py`の`show_kwargs`・`show_both`の出力を見る | `show_kwargs(x=1, y=2)`で`{'x': 1, 'y': 2}`、`show_both(1, 2, x=3, y=4)`で`args: (1, 2)`と`kwargs: {'x': 3, 'y': 4}`のように、位置引数とキーワード引数がそれぞれ別の変数に分かれて渡っている |

**正常な状態の見分け方**：`*args`は常に**タプル**、`**kwargs`は常に**辞書**として受け取られ、引数を渡さなければそれぞれ空の`()`・`{}`になります。型が`tuple`/`dict`になっていない場合は書き方（`*`/`**`の付け忘れなど）を疑ってください。

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

### 動作確認：`return`の有無・複数値・早期returnの挙動

```bash
python3 -c "
def min_max(numbers):
    return min(numbers), max(numbers)
def divide(a, b):
    if b == 0:
        return None
    return a / b
def greet(name):
    print(f'Hello, {name}')
lo, hi = min_max([3, 1, 4, 1, 5])
print(lo, hi)
print(divide(10, 0))
print(divide(10, 2))
print(greet('Alice'))
"
```

| 確認する操作 | 確認したいこと |
|---|---|
| 上記コマンドを実行する | `1 5`（複数値のアンパック）、`None`（`b=0`の早期return）、`5.0`（通常の割り算）、`Hello, Alice`に続けて`None`（`greet`は`return`が無いため戻り値が`None`）の順で表示される |

**正常な状態の見分け方**：`return`を書かない関数は必ず`None`を返します。`print(greet('Alice'))`の出力の最後の行が`None`になっていれば、`return`の有無が戻り値に反映されていることが確認できます。

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

### 動作確認：`None`と`[]`の違い、`is`と`==`の違い

```bash
python3 -c "
result = None
print(result is None)
print(result == None)
print(type(result))
empty_list = []
print(empty_list is None)
print(len(empty_list))
"
```

| 確認する操作 | 確認したいこと |
|---|---|
| 上記コマンドを実行する | `True`・`True`・`<class 'NoneType'>`・`False`・`0`の順に表示される。`None`と`[]`はどちらも「空」に見えるが、`empty_list is None`が`False`になることで**別物**だとわかる |

**正常な状態の見分け方**：`is None`と`== None`はこのケースではどちらも`True`になりますが、値の存在チェックには慣例として`is None`を使います。`[]`（空リスト）に対して`is None`が`True`になってしまう場合は、変数の中身を勘違いしている可能性があります。

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

### 動作確認：スコープの境界と`global`の効果

| 確認する操作 | 確認したいこと |
|---|---|
| `ex04.py`を実行する | `Hello, Alice`とだけ表示される（コメントアウトされた`print(name)`を有効にすると`NameError`になることも確認しておく） |
| `ex05.py`を実行する | `こんにちは`と表示される（関数の中からグローバル変数を**参照**するだけなら`global`宣言は不要） |
| `ex06.py`を実行する | `0`（`increment()`呼び出し前）に続けて`1`（呼び出し後）と表示される。`increment_wrong()`を呼び出すコードに変えて実行すると`UnboundLocalError`になる（`global`宣言が無いと、関数内での代入によりローカル変数扱いになるため） |

**正常な状態の見分け方**：グローバル変数は関数内から**参照するだけ**なら`global`が無くても動きますが、関数内で**代入（変更）**しようとすると`global`宣言が無い限りエラーになります。この「参照はOK、変更はNG」という非対称性が体感できていれば理解できています。

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

### 動作確認：関数オブジェクトそのものと、実行結果の違い

| 確認する操作 | 確認したいこと |
|---|---|
| `ex07.py`を実行する | `---Start---`・`A`・`---End---`の3行が順番に表示される（`b(a)`で渡した関数`a`が`b`の中で実行されている） |
| `ex08.py`を実行する | ポイント1で`<function a at 0x...>`のようなオブジェクト表現の後に`A`が表示され、ポイント3で`print(a)`は関数オブジェクトの表現、`print(a())`は`A`が表示されたあとに`None`が表示される |

**正常な状態の見分け方**：`print(a)`（`()`なし）は関数オブジェクトそのものの情報（`<function ...>`）を表示し、`print(a())`（`()`あり）は関数を**実行した結果**（このケースでは`None`、実行中に出力される`A`は別行）を表示します。この2つの出力が違う形になっていれば正しく理解できています。

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

### 動作確認：`result`が「前後処理付きの`a`」になっているか

| 確認する操作 | 確認したいこと |
|---|---|
| `ex09.py`を実行する | `---Start---`・`A`・`---End---`の3行が表示される（`result = outer(a)`で受け取った`inner`関数を`result()`として実行している） |
| `print(result)`を追加して実行する | `<function outer.<locals>.inner at 0x...>`のように表示され、`result`が`a`ではなく`outer`が返した`inner`という別の関数であることがわかる |

**正常な状態の見分け方**：`result()`を呼ぶだけで`---Start---`と`---End---`が自動的に付いてくることが正しい状態です。`A`だけしか表示されない場合は`outer(a)`の戻り値（`inner`）ではなく`a`自体を呼んでしまっている可能性があります。

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

### 動作確認：`@outer`が付いた関数だけ前後処理が付くか

| 確認する操作 | 確認したいこと |
|---|---|
| `ex10.py`を実行する | `a()`・`b()`のどちらの呼び出しでも、`---Start---`→`A`（または`B`）→`---End---`の3行セットが表示される（`@outer`を付けた関数はすべて同じ前後処理が自動で付く） |
| `ex10.py`の`@outer`を一時的にコメントアウトして`a()`を実行する（確認後は元に戻す） | `A`だけが表示され、`---Start---`・`---End---`が出なくなる（デコレータが`a = outer(a)`という置き換えをしていたことがわかる） |

**正常な状態の見分け方**：`@outer`が付いている関数は呼び出すたびに必ず前後処理が挟まります。コメントアウトした途端に前後処理だけ消えることを確認できれば、デコレータの動作原理を理解できています。

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

### 動作確認：引数の数が違う関数の両方に同じデコレータを使い回せるか

| 確認する操作 | 確認したいこと |
|---|---|
| `ex11.py`を実行する | `show_sum(nums)`（引数1つ）の実行で`---Start---`・`150`・`---End---`、`show_info(users)`（引数1つだが中身は辞書）の実行で`---Start---`・`Name:Tom, Age:30`など3人分・`---End---`が表示される |
| `ex10.py`（`inner()`が引数なし）の`@outer`を`show_sum`のような引数ありの関数に付け替えて実行してみる | `TypeError`になる（`ex10.py`の`inner()`は引数を受け取れないため）。これにより`*args`/`**kwargs`が無いデコレータは汎用的でないことが確認できる |

**正常な状態の見分け方**：`ex11.py`の`outer`は`inner(*args, **kwargs)`のおかげで、引数の数や型が異なる`show_sum`・`show_info`のどちらにも同じデコレータを適用できています。`ex10.py`版のデコレータで同じことをしようとするとエラーになる、という対比で違いを確認してください。

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

### 動作確認：解答（answer1〜answer6）を実行して期待通りか確かめる

```bash
python 003_function/question/answer/answer1.py
python 003_function/question/answer/answer2.py
python 003_function/question/answer/answer3.py
python 003_function/question/answer/answer4.py
python 003_function/question/answer/answer5.py
python 003_function/question/answer/answer6.py
```

| 確認する操作 | 確認したいこと |
|---|---|
| `answer1.py`を実行し、名前の入力を求められたら何か入力してEnterを押す（`input()`を使っているため対話的に入力が必要） | 入力した名前を使って`Hello, 〇〇.`と表示される。何も入力せず空欄でEnterを押した場合は`Hello, .`のようになる（デフォルト値`"guest"`は`input()`が空文字を返すため使われない点に注意） |
| `answer2.py`を実行する | コメント内の選択肢のうち、正しい呼び出し方として`B`が選ばれている（コード中に実行文が無いため、画面には何も表示されない） |
| `answer3.py`を実行する | `好きな食べ物：`の後に`カレー`・`寿司`・`ラーメン`が1行ずつ表示される |
| `answer4.py`を実行する | `name：太郎`・`age：20`・`hobby：ゲーム`が1行ずつ表示される |
| `answer5.py`を実行する | セクション本文に書いた「期待する出力」（`=== 開始 ===` → `Hello!` → `=== 終了 ===`）と一致する |
| `answer6.py`を実行する | セクション本文に書いた「期待する出力」（`add の結果 → 8` → `multiply の結果 → 15`）と一致する |

**正常な状態の見分け方**：`answer3.py`・`answer4.py`は、それぞれ`*args`・`**kwargs`で受け取った複数の値を漏れなく1行ずつ表示できていれば正解です。行数が入力した要素数と一致しない場合はループ処理（`for`文）の書き方を見直してください。
