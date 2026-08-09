import os
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

base_dir = os.path.dirname(__file__)
database = 'sqlite:///' + os.path.join(base_dir, 'data.sqlite')
engine = create_engine(database, echo=False)
Base   = declarative_base()


# ---- モデル定義（多対多：1商品が複数店舗・1店舗が複数商品）----

class Item(Base):
    __tablename__ = 'items'
    item_id   = Column(Integer, primary_key=True)
    item_name = Column(String(255), nullable=False, unique=True)
    price     = Column(Integer, nullable=False)
    # secondary に中間テーブル名を指定
    shops = relationship('Shop', secondary='stocks', back_populates='items')


class Shop(Base):
    __tablename__ = 'shops'
    shop_id   = Column(Integer, primary_key=True)
    shop_name = Column(String(255), nullable=False, unique=True)
    items = relationship('Item', secondary='stocks', back_populates='shops')


class Stock(Base):  # 中間テーブル（shop と item の関係 + 在庫数）
    __tablename__ = 'stocks'
    shop_id = Column(Integer, ForeignKey('shops.shop_id'), primary_key=True)
    item_id = Column(Integer, ForeignKey('items.item_id'), primary_key=True)
    stock   = Column(Integer)


Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# ---- データ登録 ----
session.add_all([
    Item(item_id=1, item_name='団子',       price=100),
    Item(item_id=2, item_name='肉まん',     price=150),
    Item(item_id=3, item_name='どら焼き',   price=200),
    Item(item_id=4, item_name='コンビーフ', price=500),
])
session.commit()

session.add_all([
    Shop(shop_id=1, shop_name='Tokyo'),
    Shop(shop_id=2, shop_name='Osaka'),
])
session.commit()

# コンビーフは Tokyo のみ
session.add_all([
    Stock(shop_id=1, item_id=1, stock=10),
    Stock(shop_id=1, item_id=2, stock=20),
    Stock(shop_id=1, item_id=3, stock=30),
    Stock(shop_id=1, item_id=4, stock=5),
    Stock(shop_id=2, item_id=1, stock=100),
    Stock(shop_id=2, item_id=2, stock=200),
    Stock(shop_id=2, item_id=3, stock=300),
])
session.commit()

# ---- 参照：店舗から取り扱い商品 ----
print("=== 店舗 → 取り扱い商品 ===")
shop = session.query(Shop).filter_by(shop_id=1).first()
print(f"店舗: {shop.shop_name}")
for item in shop.items:
    stock = session.query(Stock).filter_by(
        shop_id=shop.shop_id, item_id=item.item_id
    ).first()
    print(f"  {item.item_name} : {stock.stock}個")

print()

# ---- 参照：商品からその商品を扱う店舗 ----
print("=== 商品 → 取り扱い店舗 ===")
item = session.query(Item).filter_by(item_id=4).first()
print(f"商品: {item.item_name}")
for s in item.shops:
    print(f"  {s.shop_name}")

session.close()
