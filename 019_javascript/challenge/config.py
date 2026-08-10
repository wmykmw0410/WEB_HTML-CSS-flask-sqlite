import os

basedir = os.path.abspath(os.path.dirname(__file__))
instance_dir = os.path.join(basedir, 'instance')
os.makedirs(instance_dir, exist_ok=True)  # SQLiteは親ディレクトリを自動作成しないため事前に作る


class Config:
    SECRET_KEY                     = 'dev-secret-key'
    SQLALCHEMY_DATABASE_URI        = 'sqlite:///' + os.path.join(instance_dir, 'memos.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
