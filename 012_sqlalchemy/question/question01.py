"""
練習問題1：モデルを定義してください

Category テーブル:
  id   INTEGER  PK / autoincrement
  name String   NOT NULL / UNIQUE
  tasks → relationship（1対多）

Task テーブル:
  id          INTEGER  PK / autoincrement
  title       String   NOT NULL
  done        Integer  デフォルト 0
  category_id Integer  ForeignKey(categories.id)
  category  → relationship（多対1）
"""
import os
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

base_dir = os.path.dirname(__file__)
database = 'sqlite:///' + os.path.join(base_dir, 'question01.sqlite')
engine = create_engine(database, echo=False)
Base = declarative_base()


# TODO: Category クラスを定義してください
class Category(Base):
    __tablename__ = 'categories'
    pass  # ← ここを実装


# TODO: Task クラスを定義してください
class Task(Base):
    __tablename__ = 'tasks'
    pass  # ← ここを実装


Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
print("問題1: テーブル作成完了")

Session = sessionmaker(bind=engine)
session = Session()
session.close()

# クリーンアップ
db_path = database.replace('sqlite:///', '')
if os.path.exists(db_path):
    os.remove(db_path)
