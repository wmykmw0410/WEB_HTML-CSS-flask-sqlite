"""
練習問題2：カテゴリと紐づけてタスクを追加してください

カテゴリ: '仕事', '家事'
タスク:
  '仕事' → '資料作成', 'メール返信'
  '家事' → '掃除'
"""
import os
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

base_dir = os.path.dirname(__file__)
database = 'sqlite:///' + os.path.join(base_dir, 'question02.sqlite')
engine = create_engine(database, echo=False)
Base = declarative_base()


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    tasks = relationship('Task', back_populates='category')


class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    done = Column(Integer, default=0)
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship('Category', back_populates='tasks', uselist=False)


Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# TODO: Category と Task を作成し、relationship.append で紐づけて
#       session.add_all() → commit() してください


print("問題2: データ追加完了")

session.close()

# クリーンアップ
db_path = database.replace('sqlite:///', '')
if os.path.exists(db_path):
    os.remove(db_path)
