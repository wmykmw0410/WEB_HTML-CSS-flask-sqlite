# 012 SQLAlchemy

SQLAlchemy ORM を使って Python オブジェクトとしてデータベースを操作する方法を学びます。
最後に Flask と組み合わせた **Flask-SQLAlchemy** も扱います。

## 前提

- 011_sqlite を終えていること（Python から SQLite を操作する基礎）
- `sqlalchemy` と `flask-sqlalchemy` がインストール済みであること

```bash
pip install sqlalchemy flask-sqlalchemy
```

## フォルダ構成

```
012_sqlalchemy/
├── README.md
├── example/
│   ├── 01_basic.py           CRUD の基本（Engine / Model / Session）
│   ├── 02_query.py           クエリ詳細（filter / order_by / limit / func）
│   ├── 03_join.py            JOIN（join / outerjoin）
│   ├── 04_relationship.py    1対多リレーション（ForeignKey / relationship）
│   └── 05_many_to_many.py    多対多リレーション（secondary）
├── question/                  練習問題（1問1ファイル）
│   ├── question01.py〜question05.py
│   └── answer/
│       └── answer01.py〜answer05.py
└── challenge/                 011_sqliteの続き（000_my_appに組み込む機能の変更分）
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

## SQLAlchemy とは

**SQLAlchemy** は Python の ORM（Object-Relational Mapper）ライブラリです。

### ORM とは

データベースのテーブルを **Python クラス** として、レコードを **Python オブジェクト** として扱えるようにする仕組みです。

```
通常（011 sqlite3）:  SQL 文字列を直接書く
ORM（SQLAlchemy）:   Python オブジェクトを操作する → SQLAlchemy が SQL を生成
```

### 011 sqlite3 との比較

| | 011 sqlite3 | 012 SQLAlchemy |
|---|---|---|
| SQL の書き方 | 文字列として直接書く | Python のメソッドとして書く |
| テーブル定義 | `cur.execute("CREATE TABLE ...")` | `class Item(Base):` で定義 |
| データ操作 | `cur.execute("INSERT ...")` | `session.add(item)` |
| 取得結果 | タプル or `sqlite3.Row` | クラスのインスタンス |
| SQL の確認 | — | `echo=True` で自動ログ出力 |

> Flask と組み合わせた **Flask-SQLAlchemy** は → [013_flask_sqlalchemy](../013_flask_sqlalchemy/README.md)

---

## 1. SQLAlchemy の基本構成

> [example/01_basic.py](example/01_basic.py)

```python
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
```

### Engine — DB との接続

```python
engine = create_engine('sqlite:///data.sqlite', echo=True)
# echo=True で実行した SQL がターミナルに表示される
```

### Base — モデルの基底クラス

```python
Base = declarative_base()
```

### Model — テーブルの定義

```python
class Item(Base):
    __tablename__ = 'items'
    id    = Column(Integer, primary_key=True, autoincrement=True)
    name  = Column(String(255), nullable=False, unique=True)
    price = Column(Integer)
```

| 引数 | 意味 |
|---|---|
| `primary_key=True` | 主キー |
| `autoincrement=True` | 自動採番 |
| `nullable=False` | NOT NULL |
| `unique=True` | 重複禁止 |

### Session — DB 操作の窓口

```python
Base.metadata.create_all(engine)   # テーブル作成
Session = sessionmaker(bind=engine)
session = Session()
```

### CRUD

```python
# Create
item = Item(name='団子', price=100)
session.add(item)
session.commit()

# Read（全件）
items = session.query(Item).order_by(Item.id).all()

# Read（1件・条件指定）
item = session.query(Item).filter(Item.id == 1).first()

# Update
item.price = 200
session.commit()

# Delete
session.delete(item)
session.commit()
```

### 練習問題

1. `products` モデルを定義して（name / price）、3件追加・全件取得してください
2. `filter` で price が 200 より大きい商品を取得してください
3. id=1 の price を 500 に更新してください
4. id=2 のレコードを削除してください

---

## 2. クエリ詳細

> [example/02_query.py](example/02_query.py)

### filter と filter_by の違い

| | `filter` | `filter_by` |
|---|---|---|
| 比較演算子 | `==` `>` `<` `.like()` `.between()` `.in_()` が使える | `col=val`（等値のみ） |
| 複数条件 | `filter(A, B)` または `.filter(A).filter(B)` | `filter_by(a=x, b=y)` |
| 使い分け | 範囲・部分一致など柔軟な条件が必要なとき | id 指定など単純な等値検索 |

```python
# filter：演算子・メソッドが使える
session.query(Item).filter(Item.price > 200).all()
session.query(Item).filter(Item.price.between(100, 300)).all()
session.query(Item).filter(Item.name.like('%まん%')).all()

# filter_by：等値のみ、カラム名をキーワード引数で書ける（シンプル）
session.query(Item).filter_by(id=1).first()
```

### order_by / limit / offset

```python
# 降順（.asc() で昇順、デフォルトも昇順）
session.query(Item).order_by(Item.price.desc()).all()

# ページネーション（per_page=2、page=2 なら 3〜4件目）
per_page = 2
page     = 2
session.query(Item).order_by(Item.id)\
    .offset((page - 1) * per_page)\
    .limit(per_page)\
    .all()
```

| ページ | offset | limit | 取得レコード |
|---|---|---|---|
| 1 | 0 | 2 | 1〜2件目 |
| 2 | 2 | 2 | 3〜4件目 |
| 3 | 4 | 2 | 5〜6件目 |

### 集計：func.count / func.avg

```python
from sqlalchemy import func

# 全件数（scalar() で単一の Python 値として受け取る）
count = session.query(func.count(Item.id)).scalar()

# 平均価格
avg = session.query(func.avg(Item.price)).scalar()

# カテゴリ別の件数・平均・最安・最高（GROUP BY + label）
rows = session.query(
    Item.category,
    func.count(Item.id).label('count'),
    func.avg(Item.price).label('avg_price'),
    func.min(Item.price).label('min_price'),
    func.max(Item.price).label('max_price'),
).group_by(Item.category).all()

for row in rows:
    print(f"{row.category}: {row.count}件, 平均{row.avg_price:.0f}円")
```

| 集計関数 | 説明 |
|---|---|
| `func.count(col)` | 件数 |
| `func.avg(col)` | 平均値 |
| `func.sum(col)` | 合計 |
| `func.max(col)` / `func.min(col)` | 最大値 / 最小値 |
| `.scalar()` | 集計結果を単一の Python 値として受け取る |
| `.label('名前')` | カラムに別名をつける（`row.名前` でアクセス） |

### 練習問題

1. `filter` で price が 200 以上の商品を取得してください
2. `filter` で name に '大' を含む商品を `.like()` で取得してください
3. price の降順で上位3件を取得してください（`order_by` + `limit`）
4. 2件ずつページネーションして、2ページ目を取得してください（`offset` + `limit`）
5. `func.count` で全件数を表示してください
6. `func.avg` と `group_by` でカテゴリ別の平均価格を表示してください

---

## 3. JOIN

> [example/03_join.py](example/03_join.py)

```python
# INNER JOIN（3テーブル）
results = session.query(Shop, Item.item_name, Stock.stock)\
    .join(Stock, Shop.shop_id == Stock.shop_id)\
    .join(Item,  Item.item_id  == Stock.item_id)\
    .all()

for row in results:
    print(f"{row.Shop.shop_name} → {row.item_name} : {row.stock}個")

# OUTER JOIN（一致しないレコードも含む）
results = session.query(Item, Stock.stock)\
    .outerjoin(Stock, Item.item_id == Stock.item_id)\
    .all()
```

| メソッド | SQL | 意味 |
|---|---|---|
| `.join()` | INNER JOIN | 両テーブルに存在するレコードだけ |
| `.outerjoin()` | LEFT OUTER JOIN | 左テーブルの全レコード＋右テーブルが一致しなければ NULL |

### 練習問題

1. INNER JOIN で Shop / Item / Stock を結合して、全在庫一覧を表示してください
2. OUTER JOIN で Item / Stock を結合し、在庫がない商品（stock が NULL）を確認してください

---

## 4. 1対多リレーション

> [example/04_relationship.py](example/04_relationship.py)

部署（Department）と社員（Employee）の例で **1対多**（1つの部署に複数の社員）を実装します。

```python
from sqlalchemy import ForeignKey
from sqlalchemy.orm import declarative_base, relationship

class Department(Base):
    __tablename__ = 'departments'
    id   = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    # 1対多：department.employees でその部署の社員一覧を取得
    employees = relationship('Employee', back_populates='department')


class Employee(Base):
    __tablename__ = 'employees'
    id            = Column(Integer, primary_key=True, autoincrement=True)
    name          = Column(String, nullable=False)
    department_id = Column(Integer, ForeignKey('departments.id'))   # 外部キー
    # 多対1：employee.department でその社員の部署を取得
    department = relationship('Department', back_populates='employees', uselist=False)
```

### 関係の登録と参照

```python
# 登録
dept.employees.append(emp)
session.add(dept)
session.commit()

# 参照：社員から部署を取得
emp = session.query(Employee).filter_by(id=1).first()
print(emp.department.name)

# 参照：部署から社員一覧を取得
dept = session.query(Department).filter_by(id=1).first()
for emp in dept.employees:
    print(emp.name)
```

| 引数 | 意味 |
|---|---|
| `ForeignKey('テーブル名.カラム名')` | 外部キーを指定 |
| `relationship('クラス名')` | 関連するモデルを指定 |
| `back_populates='属性名'` | 反対側のモデルで対応する属性名を指定 |
| `uselist=False` | 多対1 の向きでは単一オブジェクトを返す |

### 練習問題

1. `Category` と `Product` の1対多リレーションを実装してください
   - Category: id / name
   - Product: id / name / price / category_id（ForeignKey）
2. 「電子機器」カテゴリに3件の商品を追加してください
3. `product.category.name` でカテゴリ名を表示してください

---

## 5. 多対多リレーション

> [example/05_many_to_many.py](example/05_many_to_many.py)

商品（Item）と店舗（Shop）の例で **多対多**（1つの商品が複数の店舗で販売、1つの店舗が複数の商品を扱う）を実装します。中間テーブルは `secondary` で指定します。

```python
class Item(Base):
    __tablename__ = 'items'
    item_id   = Column(Integer, primary_key=True)
    item_name = Column(String(255))
    price     = Column(Integer)
    # secondary に中間テーブル名を指定
    shops = relationship('Shop', secondary='stocks', back_populates='items')


class Shop(Base):
    __tablename__ = 'shops'
    shop_id   = Column(Integer, primary_key=True)
    shop_name = Column(String(255))
    items = relationship('Item', secondary='stocks', back_populates='shops')


class Stock(Base):   # 中間テーブル
    __tablename__ = 'stocks'
    shop_id = Column(Integer, ForeignKey('shops.shop_id'), primary_key=True)
    item_id = Column(Integer, ForeignKey('items.item_id'), primary_key=True)
    stock   = Column(Integer)
```

### 参照

```python
shop = session.query(Shop).filter_by(shop_id=1).first()
for item in shop.items:   # その店舗が扱う商品一覧
    stock = session.query(Stock).filter_by(
        shop_id=shop.shop_id, item_id=item.item_id
    ).first()
    print(f"{item.item_name} : {stock.stock}個")
```

### 練習問題

1. 「Osaka」店の取り扱い商品と在庫数を表示してください
2. 「コンビーフ」を扱っている店舗の一覧を `item.shops` で表示してください

---

## 6. 練習問題

> [question/](question/) — 問題（1問1ファイル） ｜ [question/answer/](question/answer/) — 解答

### 問題：タスク管理システムを作ろう

`question/questionN.py` を開き、コメントの指示に従ってコードを完成させてください。各ファイルは独立して実行できるように、必要なテーブル・データをファイル内で作り直してから処理を行う構成になっています。

```bash
python 012_sqlalchemy/question/question01.py
```

#### テーブル仕様

**categories テーブル**

| カラム | 型 | 制約 |
|---|---|---|
| id | Integer | PK / autoincrement |
| name | String | NOT NULL / UNIQUE |
| tasks | relationship | → Task（1対多） |

**tasks テーブル**

| カラム | 型 | 制約 |
|---|---|---|
| id | Integer | PK / autoincrement |
| title | String | NOT NULL |
| done | Integer | デフォルト 0 |
| category_id | Integer | ForeignKey(categories.id) |
| category | relationship | → Category（多対1）|

#### 問題一覧

| 問題 | 内容 | 解答 |
|---|---|---|
| 1 | モデルを定義してテーブルを作成する | [question/answer/answer01.py](question/answer/answer01.py) |
| 2 | カテゴリと紐づけてタスクを追加する（relationship の append を使う）| [question/answer/answer02.py](question/answer/answer02.py) |
| 3 | 全タスクを取得して `task.category.name` でカテゴリ名を表示する | [question/answer/answer03.py](question/answer/answer03.py) |
| 4 | id=1 のタスクを done=1 に更新する | [question/answer/answer04.py](question/answer/answer04.py) |
| 5 | category 名で絞り込み（filter + join）する | [question/answer/answer05.py](question/answer/answer05.py) |

---

## 7. 練習問題：書籍データをSQLAlchemyに移行しよう

> [challenge/challenge.py](challenge/challenge.py) — 問題 ｜ [challenge/answer/challenge.py](challenge/answer/challenge.py) — 解答

### 問題：書籍データの保存先を sqlite3（生SQL）から SQLAlchemy（ORM）に変更しよう

`011_sqlite`で作った書籍一覧・詳細・書籍追加フォーム・リダイレクト（`challenge/challenge.py`にすでに実装済み）は、これまで`sqlite3`モジュールで生SQLを書いて`books.db`を操作していました。これを`SQLAlchemy`のORM（`Book`モデル + `Session`）に置き換えます。

`Book`モデルの定義（問題1）はすでに`engine`・`Base`・`Session`の準備、`init_db()`（テーブル作成と初回シード投入）と合わせて用意されていますが、モデルのカラム定義は`pass`のままになっているので、まずこれを実装してください。`books.json`は初回起動時にだけ`books`テーブルへ投入するために使われます。

```bash
python 012_sqlalchemy/challenge/challenge.py
```

#### 仕様

| エンドポイント | メソッド | 処理 |
|---|---|---|
| `/` | GET | `session.query(Book)`で全件取得する（`author`指定時は`filter_by(author=author)`で絞り込み） |
| `/books/<int:book_id>` | GET | `filter_by(id=book_id).first()`で1件取得する |
| `/books/new` | POST（バリデーション成功時） | `Book(...)`を作って`session.add()`→`session.commit()`する |

#### ヒント

- モデル定義は`id`（主キー・自動採番）、`title`・`author`・`price`・`image`（すべて`NOT NULL`）の5カラム（本章セクション1）
- `session.query(Book).filter_by(...).all()` / `.first()`で結果を取得する（セクション2）
- テンプレート側では`book.title`のようにORMオブジェクトの属性へ直接アクセスできる（`dict()`への変換は不要）
- 見た目やCSRF・ファイルアップロードの仕組みは`011_sqlite`から変更不要
