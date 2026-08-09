import os
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

base_dir = os.path.dirname(__file__)
database = 'sqlite:///' + os.path.join(base_dir, 'data.sqlite')
engine = create_engine(database, echo=False)
Base   = declarative_base()


class Item(Base):
    __tablename__ = 'items'
    item_id   = Column(Integer, primary_key=True)
    item_name = Column(String(255), nullable=False, unique=True)
    price     = Column(Integer, nullable=False)


class Shop(Base):
    __tablename__ = 'shops'
    shop_id   = Column(Integer, primary_key=True)
    shop_name = Column(String(255), nullable=False, unique=True)


class Stock(Base):
    __tablename__ = 'stocks'
    shop_id = Column(Integer, primary_key=True)
    item_id = Column(Integer, primary_key=True)
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
session.add_all([
    Shop(shop_id=1, shop_name='Tokyo'),
    Shop(shop_id=2, shop_name='Osaka'),
])
# コンビーフ（item_id=4）は在庫なし → OUTER JOIN で NULL になる
session.add_all([
    Stock(shop_id=1, item_id=1, stock=10),
    Stock(shop_id=1, item_id=2, stock=20),
    Stock(shop_id=1, item_id=3, stock=30),
    Stock(shop_id=2, item_id=1, stock=100),
    Stock(shop_id=2, item_id=2, stock=200),
    Stock(shop_id=2, item_id=3, stock=300),
])
session.commit()

# ---- INNER JOIN（3テーブル）----
print("=== INNER JOIN（Shop / Item / Stock）===")
rows = (
    session.query(Shop, Item.item_name, Stock.stock)
    .join(Stock, Shop.shop_id == Stock.shop_id)
    .join(Item,  Item.item_id  == Stock.item_id)
    .all()
)
for row in rows:
    print(f"  {row.Shop.shop_name} → {row.item_name} : {row.stock}個")

print()

# ---- OUTER JOIN（在庫なし商品も含む）----
print("=== OUTER JOIN（Item LEFT JOIN Stock）===")
rows = (
    session.query(Item, Stock.stock)
    .outerjoin(Stock, Item.item_id == Stock.item_id)
    .all()
)
for row in rows:
    stock_str = f"{row.stock}個" if row.stock is not None else "在庫なし"
    print(f"  {row.Item.item_name} : {stock_str}")

session.close()
