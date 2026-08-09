# 019 カート機能と注文確定

Flaskの`session`を使った**ショッピングカート**の実装方法を学び、`018_ownership_crud`のブックストアに「カートに入れる」→「注文を確定する」という購入フローを追加します。

## 前提

| チャプター | 使う知識 |
|---|---|
| 009_forms | session（Cookie）の基本 |
| 018_ownership_crud | db.Model・Blueprint・所有権パターン |

## フォルダ構成

```
019_cart/
├── README.md
├── example/
│   └── 01_cart_basics.py      セッションカードの基本（DB不使用）
└── challenge/                 018_ownership_crudの続き（000_my_appに組み込む機能の変更分）
    ├── app.py
    ├── models.py
    ├── forms.py
    ├── config.py
    ├── auth/views.py
    ├── books/views.py
    ├── cart/views.py           カートBlueprint（新規）
    ├── static/
    ├── templates/
    └── answer/
        ├── app.py
        ├── models.py
        ├── forms.py
        ├── config.py
        ├── auth/views.py
        ├── books/views.py
        ├── cart/views.py
        ├── static/
        └── templates/
```

---

## カートはなぜDBではなくsessionに保存するのか

| | DB（例: `Book`） | session（Cookie） |
|---|---|---|
| 保存場所 | サーバーのDB | ブラウザのCookie |
| 有効期間 | ずっと残る | ブラウザを閉じるまで（クリアされることもある） |
| 向いている用途 | 確定した記録（注文履歴など） | 「まだ確定していない」一時的な状態 |

カートの中身は「まだ買うと決めたわけではない、一時的な状態」なので、確定前のデータをわざわざDBに保存する必要はありません。**注文が確定した瞬間だけ**DBに書き込む、という役割分担がポイントです。

---

## 1. セッションカートの基本

> [example/01_cart_basics.py](example/01_cart_basics.py)

```python
from flask import session

@app.route('/cart/add/<int:book_id>', methods=['POST'])
def add_to_cart(book_id):
    cart = session.get('cart', {})       # {'1': 2, '3': 1} のような辞書
    key = str(book_id)
    cart[key] = cart.get(key, 0) + 1
    session['cart'] = cart               # ← 辞書を書き換えただけでは保存されない。再代入が必要
    return redirect(url_for('index'))
```

### なぜ`session['cart'] = cart`の再代入が必要か

Flaskは`session`オブジェクトへの**代入**（`session['cart'] = ...`）は自動的に検知して保存しますが、すでに`session`に入っている辞書やリストを`.update()`や`[key] = value`で**直接書き換えただけ**では変更が検知されず、レスポンスに反映されないことがあります。`cart = session.get('cart', {})`で取り出した辞書を書き換えたら、必ず`session['cart'] = cart`で書き戻してください。

### 実行方法

```bash
python 019_cart/example/01_cart_basics.py
```

---

## 2. 数量の管理

カートのキーを`book_id`の文字列、値を数量にした辞書として持つと、追加・更新・削除がシンプルになります。

```python
cart: dict[str, int] = session.get('cart', {})

# 追加（+1）
cart[key] = cart.get(key, 0) + 1

# 数量を直接指定して更新（0以下なら削除）
if quantity <= 0:
    cart.pop(key, None)
else:
    cart[key] = quantity

# 削除
cart.pop(key, None)

session['cart'] = cart
```

小計・合計はカートの中身から都度計算します（DBに保存するわけではないので、常に「今の価格 × 数量」で計算し直します）。

```python
def get_cart_items():
    cart = session.get('cart', {})
    items = []
    for book_id_str, quantity in cart.items():
        book = Book.query.get(int(book_id_str))
        if book:
            items.append({'book': book, 'quantity': quantity, 'subtotal': book.price * quantity})
    return items
```

---

## 3. 注文確定（チェックアウト）— sessionからDBへ

カートは「確定前の一時データ」でしたが、注文を確定した瞬間に**DBの記録として保存**します。ここで`Order`（注文）と`OrderItem`（注文明細）という2つのモデルを新しく作ります。

```python
class Order(db.Model):
    __tablename__ = 'orders'
    id         = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id    = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    items      = relationship('OrderItem', back_populates='order')


class OrderItem(db.Model):
    __tablename__ = 'order_items'
    id       = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    book_id  = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    title    = db.Column(db.String(100), nullable=False)   # 注文時点のタイトルを保存
    price    = db.Column(db.Integer, nullable=False)        # 注文時点の価格を保存
    quantity = db.Column(db.Integer, nullable=False, default=1)
    order    = relationship('Order', back_populates='items')
```

### ポイント：なぜ`book_id`だけでなく`title`・`price`もコピーして保存するのか

`OrderItem`が`Book`への外部キー（`book_id`）だけを持っていたらどうなるか考えてみます。

```
1. ユーザーが「走れメロス」（¥440）を注文する
2. 半年後、管理者が価格を¥550に変更した
3. ユーザーが注文履歴を見ると…「走れメロス ¥550」と表示されてしまう（実際に払ったのは¥440なのに）
4. さらに、管理者がその本を削除したら、注文履歴の該当行が参照エラーになる
```

これを防ぐため、注文が確定した**その瞬間の**`title`と`price`を`OrderItem`に**コピーして保存**します。`book_id`は「どの本か」を示す参照として残しつつ、表示用の情報は独立して持たせるのが実務でもよく使われるパターンです。

### チェックアウト処理

```python
@cart_bp.route('/checkout', methods=['POST'])
@login_required
def checkout():
    items = get_cart_items()
    order = Order(user_id=current_user.id)
    for item in items:
        order.items.append(OrderItem(
            book_id=item['book'].id,
            title=item['book'].title,      # ← 現在の値をコピー
            price=item['book'].price,      # ← 現在の値をコピー
            quantity=item['quantity'],
        ))
    db.session.add(order)
    db.session.commit()

    session.pop('cart', None)   # 確定したのでカートを空にする
    return redirect(url_for('cart.complete', order_id=order.id))
```

---

## 実行方法

```bash
cd 019_cart/example
python 01_cart_basics.py
```

---

## 4. 練習問題：ブックストアにカート機能と注文確定を実装しよう

> [challenge/app.py](challenge/app.py) — 問題 ｜ [challenge/answer/app.py](challenge/answer/app.py) — 解答

### 問題：カートに入れる→注文を確定する、という一連の購入フローを実装しよう

`018_ownership_crud`で作った書籍一覧・詳細・追加・編集・削除の機能はそのままです。ここに「カートに入れる」「数量を調整する」「注文を確定する」「注文履歴を見る」機能を追加します。

```bash
cd 019_cart/challenge
flask db init
flask db migrate -m "create orders and order_items tables"
flask db upgrade
python app.py
```

#### 仕様

| 問題 | 内容 |
|---|---|
| 1 | `models.py`に`Order`・`OrderItem`モデルを定義する |
| 2 | `cart/views.py`の`update`で、カート内の数量をフォームの入力値で直接更新する（0以下なら削除） |
| 3 | `cart/views.py`の`checkout`で、カートの中身から`Order`・`OrderItem`を作成してDBに保存し、セッションのカートを空にする |

#### ヒント

- `Order`は`id`・`user_id`・`created_at`の3カラム、`OrderItem`は`id`・`order_id`・`book_id`・`title`・`price`・`quantity`の6カラム（本章セクション3）
- `quantity`の更新は`request.form.get('quantity', type=int)`で取得する（セクション2）
- `OrderItem`の`title`・`price`には`item['book'].title`・`item['book'].price`という**そのときの値**を代入する。`book_id`だけを保存してはいけない理由はセクション3を参照
- カートの追加・削除・クリア・注文完了ページ・注文履歴ページはすでに実装済み。`update`と`checkout`のロジックのみを実装すればよい
- 見た目やCSRF・所有権の仕組みは`018_ownership_crud`から変更不要

## 次のステップ

続きは [020_testing](../020_testing) で、ここまで作ってきた機能を自動テストで検証する方法を学びます。
