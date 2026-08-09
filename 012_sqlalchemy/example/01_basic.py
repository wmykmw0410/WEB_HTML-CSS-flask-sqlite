import os
from sqlalchemy import create_engine, Column, Integer, String, or_
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# ---- Engine（DB 接続）----
base_dir = os.path.dirname(__file__)
database = 'sqlite:///' + os.path.join(base_dir, 'data.sqlite')
engine = create_engine(database, echo=False)  # echo=True にすると SQL がターミナルに表示される

# ---- Base / Model ----
Base = declarative_base()

class Item(Base):
    __tablename__ = 'items'
    id    = Column(Integer, primary_key=True, autoincrement=True)
    name  = Column(String(255), nullable=False, unique=True)
    price = Column(Integer, nullable=True)

    def __init__(self, name, price):
        self.name  = name
        self.price = price

    def __str__(self):
        return f"Item(id={self.id}, name={self.name}, price={self.price})"


# ---- テーブル作成・セッション ----
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# ---- Create ----
print("=== Create ===")
item01 = Item('団子',     100)
item02 = Item('肉まん',   150)
item03 = Item('どら焼き', 200)
session.add_all([item01, item02, item03])
session.commit()
print("3件追加しました")

# ---- Read（全件）----
print("\n=== Read（全件）===")
items = session.query(Item).order_by(Item.id).all()
for item in items:
    print(item)

# ---- Read（1件・条件）----
print("\n=== Read（filter id=3）===")
target = session.query(Item).filter(Item.id == 3).first()
print(target)

# ---- Read（複数条件 or_）----
print("\n=== Read（id=1 OR id=2）===")
targets = session.query(Item).filter(or_(Item.id == 1, Item.id == 2)).all()
for t in targets:
    print(t)

# ---- Update（1件）----
print("\n=== Update（id=3 price=500）===")
target = session.query(Item).filter(Item.id == 3).first()
target.price = 500
session.commit()
target = session.query(Item).filter(Item.id == 3).first()
print("更新後:", target)

# ---- Update（複数）----
print("\n=== Update（id=1,2 price=999）===")
targets = session.query(Item).filter(or_(Item.id == 1, Item.id == 2)).all()
for t in targets:
    t.price = 999
session.commit()

# ---- Delete ----
print("\n=== Delete（id=1）===")
target = session.query(Item).filter(Item.id == 1).first()
session.delete(target)
session.commit()

items = session.query(Item).order_by(Item.id).all()
print("削除後:")
for item in items:
    print(item)

session.close()
