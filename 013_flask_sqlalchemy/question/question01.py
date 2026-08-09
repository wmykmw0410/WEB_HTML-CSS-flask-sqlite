"""
練習問題1：Memo モデルを定義してテーブルを作成してください

カラム:
  id    Integer      PK / autoincrement
  title String(100)  NOT NULL
  body  String(500)
"""
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
base_dir = os.path.dirname(__file__)
app.config['SQLALCHEMY_DATABASE_URI']        = 'sqlite:///' + os.path.join(base_dir, 'question01.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# TODO: Memo クラスを db.Model で定義してください
class Memo(db.Model):
    pass  # ← ここを実装


with app.app_context():
    db.drop_all()
    db.create_all()
print("問題1: テーブル作成完了")

# クリーンアップ
db_path = os.path.join(base_dir, 'question01.sqlite')
if os.path.exists(db_path):
    os.remove(db_path)
