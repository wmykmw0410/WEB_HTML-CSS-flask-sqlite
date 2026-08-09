import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# ---- Flask / Flask-SQLAlchemy のセットアップ ----
app = Flask(__name__)

base_dir = os.path.dirname(__file__)
app.config['SECRET_KEY']                  = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI']     = 'sqlite:///' + os.path.join(base_dir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# ---- モデル定義（db.Model を継承）----
class Task(db.Model):
    __tablename__ = 'tasks'
    id      = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(200), nullable=False)

    def __str__(self):
        return f"Task(id={self.id}, content={self.content})"


# ---- テーブル作成 ----
def init_db():
    with app.app_context():  # Flask の外でも DB 操作するには app_context が必要
        print("=== テーブル初期化 ===")
        db.drop_all()
        db.create_all()

        task01 = Task(content='掃除')
        task02 = Task(content='洗濯')
        task03 = Task(content='買い物')
        db.session.add_all([task01, task02, task03])
        db.session.commit()
        print("3件追加しました")


# ---- CRUD 操作 ----
def insert():
    with app.app_context():
        print("\n=== Insert ===")
        task = Task(content='請求書を作成する')
        db.session.add(task)
        db.session.commit()
        print(f"追加: {task}")


def select_all():
    with app.app_context():
        print("\n=== Select All ===")
        tasks = Task.query.all()
        for task in tasks:
            print(f"  {task}")


def select_one(pk):
    with app.app_context():
        print(f"\n=== Select id={pk} ===")
        task = Task.query.filter_by(id=pk).first()
        print(f"  {task}")


def update(pk):
    with app.app_context():
        print(f"\n=== Update id={pk} ===")
        task = Task.query.filter_by(id=pk).first()
        print(f"  更新前: {task}")
        task.content = '（更新済み）'
        db.session.add(task)
        db.session.commit()
        task = Task.query.filter_by(id=pk).first()
        print(f"  更新後: {task}")


def delete(pk):
    with app.app_context():
        print(f"\n=== Delete id={pk} ===")
        task = Task.query.filter_by(id=pk).first()
        db.session.delete(task)
        db.session.commit()
        print(f"  削除: {task}")


# ---- 実行 ----
if __name__ == '__main__':
    init_db()
    insert()
    select_all()
    update(1)
    select_one(1)
    delete(2)
    select_all()
