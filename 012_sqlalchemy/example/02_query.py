import os
from sqlalchemy import create_engine, Column, Integer, String, func
from sqlalchemy.orm import declarative_base, sessionmaker

base_dir = os.path.dirname(__file__)
database = 'sqlite:///' + os.path.join(base_dir, 'data.sqlite')
engine = create_engine(database, echo=False)
Base   = declarative_base()


class Item(Base):
    __tablename__ = 'items'
    id       = Column(Integer, primary_key=True, autoincrement=True)
    name     = Column(String(255), nullable=False, unique=True)
    category = Column(String(100))
    price    = Column(Integer, nullable=False)

    def __str__(self):
        return f"Item(id={self.id}, name={self.name}, category={self.category}, price={self.price})"


Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

session.add_all([
    Item(name='団子',       category='和菓子', price=100),
    Item(name='いちご大福', category='和菓子', price=300),
    Item(name='どら焼き',   category='和菓子', price=200),
    Item(name='肉まん',     category='中華',   price=150),
    Item(name='小籠包',     category='中華',   price=280),
    Item(name='コンビーフ', category='洋食',   price=500),
])
session.commit()

# ---- filter vs filter_by ----
print("=== filter vs filter_by ===")

# filter：演算子・メソッドが使える
print("filter price > 200:")
for item in session.query(Item).filter(Item.price > 200).all():
    print(f"  {item}")

print("filter price.between(100, 300):")
for item in session.query(Item).filter(Item.price.between(100, 300)).all():
    print(f"  {item}")

print("filter name.like('%まん%'):")
for item in session.query(Item).filter(Item.name.like('%まん%')).all():
    print(f"  {item}")

# filter_by：等値のみ。カラム名をキーワード引数で書ける
print("filter_by id=1:")
print(f"  {session.query(Item).filter_by(id=1).first()}")

# ---- order_by / limit / offset ----
print("\n=== order_by ===")
print("price DESC:")
for item in session.query(Item).order_by(Item.price.desc()).all():
    print(f"  {item.name}: {item.price}円")

print("\n=== limit / offset（ページネーション）===")
per_page = 2
for page in (1, 2, 3):
    items = (
        session.query(Item)
        .order_by(Item.id)
        .offset((page - 1) * per_page)
        .limit(per_page)
        .all()
    )
    names = [i.name for i in items]
    print(f"  page={page}: {names}")

# ---- 集計：func.count / func.avg ----
print("\n=== 集計 ===")

# scalar() で単一の値として受け取る
count = session.query(func.count(Item.id)).scalar()
avg   = session.query(func.avg(Item.price)).scalar()
print(f"全件数: {count}")
print(f"全体の平均価格: {avg:.1f}円")

# GROUP BY + label でカラムに別名をつける
print("\nカテゴリ別（GROUP BY）:")
rows = (
    session.query(
        Item.category,
        func.count(Item.id).label('count'),
        func.avg(Item.price).label('avg_price'),
        func.min(Item.price).label('min_price'),
        func.max(Item.price).label('max_price'),
    )
    .group_by(Item.category)
    .order_by(Item.category)
    .all()
)
for row in rows:
    print(f"  {row.category}: {row.count}件, 平均{row.avg_price:.0f}円, 最安{row.min_price}円, 最高{row.max_price}円")

session.close()
