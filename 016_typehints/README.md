# 016 Python 型ヒント

`015_login`までの内容を終えたところで、Python の**型ヒント**構文を学びます。これ以降のチャプターでは、関数の引数・戻り値に型ヒントを付けるスタイルで進みます。

型ヒントが特に役立つのは、`User.query.filter_by(...).first()` のように「該当データが無ければ`None`が返る」ORMの検索結果を扱うときです。`015_login`のログイン処理ですでに`Optional[User]`という書き方が登場していますが、ここではその意味を体系的に整理します。

## 前提

| チャプター | 使う知識 |
|---|---|
| 015_login | `Optional[User]`など、型ヒントが実際に使われている箇所 |

## フォルダ構成

```
016_typehints/
├── 01_typehints.py     基本の型ヒント（int / str / float / list / dict）
├── 02_annotated.py      Annotated（メタデータ付き型）
├── 03_optional.py       Optional（省略可能な引数）
├── 04_union.py          Union（複数の型を許容）
└── challenge/           015_loginの続き（000_my_appに組み込む機能の変更分）
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

## 1. 基本の型ヒント

> [01_typehints.py](01_typehints.py)

引数と戻り値に型を明示する書き方。

```python
def add(num1: int, num2: int) -> str:
    result: str = 'The result of addition => '
    return result + str(num1 + num2)

def process_items(items: list[str]) -> None:
    for item in items:
        print(item)

def count_characters(word_list: list[str]) -> dict[str, int]:
    count_map: dict[str, int] = {}
    for word in word_list:
        count_map[word] = len(word)
    return count_map
```

### ポイント

| 書き方 | 意味 |
|---|---|
| `num1: int` | 引数 `num1` は `int` 型 |
| `-> str` | 戻り値は `str` 型 |
| `list[str]` | 文字列のリスト |
| `dict[str, int]` | キーが `str`、値が `int` の辞書 |

型ヒントは実行時に強制されるものではなく、あくまで**注釈**（IDE補完・静的解析・可読性向上のため）。

## 2. Annotated — メタデータ付き型

> [02_annotated.py](02_annotated.py)

型そのものに説明などのメタデータを付加できる。FastAPI では `Query` / `Path` などのバリデーション情報を型に埋め込むのに使われる。

```python
from typing import Annotated

def process_value(
    value: Annotated[int, "0〜100の整数"]
) -> None:
    if 0 <= value <= 100:
        print(f"受け取った値は範囲内です: {value}")
    else:
        raise ValueError(f"範囲外の値です。受け取った値: {value}")
```

`Annotated[型, メタデータ, ...]` の形で、型自体は変えずに追加情報を持たせられる。

## 3. Optional — 省略可能な引数

> [03_optional.py](03_optional.py)

`None` を許容する型。デフォルト値 `None` と組み合わせて「指定してもしなくてもよい引数」を表現する。

```python
from typing import Optional

def get_profile(
    email: str,
    username: Optional[str] = None,
    age: Optional[int] = None
) -> dict:
    profile = {"email": email}
    if username is not None:
        profile["username"] = username
    if age is not None:
        profile["age"] = age
    return profile
```

`Optional[str]` は `str | None` と同じ意味。FastAPI ではクエリパラメータや任意フィールドの定義に使う。

## 4. Union — 複数の型を許容

> [04_union.py](04_union.py)

複数の型のいずれかを許容する。Python 3.10 以降は `|` 演算子で書ける。

```python
def parse_input(value: int | str) -> str:
    if isinstance(value, int):
        return f"値は整数型です=> {value}"
    elif isinstance(value, str):
        return f"値は文字列型です=> {value}"
    else:
        raise ValueError("引数が整数型/文字列型ではありません")
```

### まとめ

| 型ヒント | 意味 | 例 |
|---|---|---|
| `int` / `str` / `float` / `list` / `dict` | 基本の型 | `def f(x: int) -> str` |
| `Annotated[型, メタデータ]` | 型にメタデータを付加 | `Annotated[int, "0〜100"]` |
| `Optional[型]`（`型 \| None`） | `None` を許容 | `Optional[str] = None` |
| `型A \| 型B`（`Union`） | 複数の型を許容 | `int \| str` |

## 5. docstringの書き方

型ヒントは「引数・戻り値の**型**」を示しますが、それだけでは「関数が**何をするか**」までは伝わりません。それを補うのが**docstring**（関数の直後に`"""`で囲んで書く説明文）です。実際、`02_annotated.py`〜`04_union.py`はすでにこの書き方をしています。

### 基本形（Googleスタイル）

```python
def add(num1: int, num2: int) -> int:
    """
    2つの数値を加算する

    Args:
        num1: 1つ目の数値
        num2: 2つ目の数値

    Returns:
        num1 と num2 の合計
    """
    return num1 + num2
```

| セクション | 書く内容 | 省略可否 |
|---|---|---|
| 1行目（概要） | 関数が何をするかを1文で | 必須 |
| `Args:` | 各引数の意味 | 引数があれば書く |
| `Returns:` | 戻り値の意味（型は書かない。型ヒントとの役割分担） | 戻り値があれば書く |
| `Raises:` | 送出しうる例外とその条件 | 例外を送出する場合のみ |

### 型ヒントとdocstringの役割分担

| | 担当する情報 | 例 |
|---|---|---|
| 型ヒント | 「何の型か」 | `num1: int` |
| docstring | 「その値が何を意味するか」 | `Args:` の `num1: 1つ目の数値` |

型だけでは分からない「意味」をdocstringが補うことで、IDEの補完・`help()`表示・チーム開発時の可読性が上がります。

### 実行時にdocstringを確認する

```python
print(add.__doc__)
help(add)
```

---

## 6. 練習問題：書籍データの管理コードに型ヒントとdocstringを付けよう

> [challenge/challenge.py](challenge/challenge.py) — 問題 ｜ [challenge/answer/challenge.py](challenge/answer/challenge.py) — 解答

### 問題：既存のコードに型ヒント・docstringを後付けしよう

`015_login`で作った書籍一覧・詳細・追加フォーム・新規登録・ログイン・ログアウトの機能はそのままです（新しい機能は追加しません）。このチャプターで学んだ`Optional`・`Union`（`str | Response`）とdocstringを、既存のコードに付けていきます。

```bash
cd 016_typehints/challenge
flask --app challenge db init
flask --app challenge db migrate -m "create books and users tables"
flask --app challenge db upgrade
python challenge.py
```

#### 仕様

| 問題 | 内容 |
|---|---|
| 1 | `User`モデルの`set_password`/`check_password`に型ヒントを付ける |
| 2 | `load_user`に型ヒントを付ける（戻り値は`Optional[User]`） |
| 3 | `book_list`・`book_detail`・`register`・`login`・`logout`・`new_book`・`old_books`に型ヒントを付ける（`str`を返しうる関数は`str \| Response`） |
| 4 | `load_user`・`register`・`login`にGoogle形式のdocstringを追加する |

#### ヒント

- `set_password(self, raw: str) -> None` / `check_password(self, raw: str) -> bool`（本章セクション1）
- `load_user(user_id: str) -> Optional[User]`。`.get()`は該当データが無ければ`None`を返す（セクション3、`015_login`セクション3の`Optional[User]`と同じ考え方）
- `render_template(...)`は`str`、`redirect(...)`は`Response`を返すため、両方の可能性がある関数は`str | Response`と書く（セクション4）
- docstringは概要1行 + `Args:` + `Returns:`のGoogle形式で書く（セクション5）
- 見た目やCSRF・ファイルアップロードの仕組み、ルーティングやビジネスロジックは`015_login`から変更不要（型ヒントとdocstringのみを追加する）

## 実行方法

```bash
python 016_typehints/01_typehints.py
python 016_typehints/02_annotated.py
python 016_typehints/03_optional.py
python 016_typehints/04_union.py
```

## 次のステップ

続きは [017_blueprint](../017_blueprint) で、Blueprintとgオブジェクトを学びます。`015_login`で使った`Optional[User]`のような型ヒントを、これ以降も引き続き使っていきます。
