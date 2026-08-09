"""
Flask-Migrate の基本セットアップ

実行前に以下のコマンドでテーブルを作成してください:
    flask db init
    flask db migrate -m "create tasks table"
    flask db upgrade

    # is_completed カラムを追加する場合:
    flask db migrate -m "add is_completed column"
    flask db upgrade

その後 python example/01_basic.py で INSERT を実行できます。
"""
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

base_dir = os.path.dirname(__file__)
app.config['SECRET_KEY']                  = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI']     = 'sqlite:///' + os.path.join(base_dir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)   # この1行で flask db コマンドが使えるようになる


class Task(db.Model):
    __tablename__ = 'tasks'

    id           = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content      = db.Column(db.String(200), nullable=False)
    is_completed = db.Column(db.Boolean, default=False)

    def __str__(self):
        return f'Task(id={self.id}, content={self.content}, done={self.is_completed})'


def insert():
    with app.app_context():
        print('=== INSERT ===')
        task01 = Task(content='掃除')
        task02 = Task(content='洗濯')
        task03 = Task(content='買い物')
        db.session.add_all([task01, task02, task03])
        db.session.commit()
        print('3件追加しました')

        print('\n=== SELECT ===')
        for task in Task.query.all():
            print(f'  {task}')


if __name__ == '__main__':
    insert()
