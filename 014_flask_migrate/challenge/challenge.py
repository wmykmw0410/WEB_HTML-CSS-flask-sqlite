"""
練習問題：メモデータの管理に Flask-Migrate を組み込もう

013_flask_sqlalchemyで作ったメモ一覧・詳細・追加フォーム・リダイレクトの見た目や機能はそのままです。
これまでは db.create_all() でテーブルが無ければ作るだけでしたが、
Flask-Migrate を組み込んで「flask db」コマンドでスキーマを管理する方式に変更し、
既存テーブルに due_date（期限）カラムを追加します。

以下の TODO コメントの箇所にコードを書いて完成させてください。

実行手順:
cd challenge

# 問題1：Migrate(app, db) を追加したら、まず既存のテーブルを
# マイグレーション管理下に置く
flask --app challenge db init
flask --app challenge db migrate -m "create memos table"
flask --app challenge db upgrade
python challenge.py   # これまで通り動くことを確認

# 問題2：Memo モデルに due_date カラムを追加したら、再度マイグレーション
flask --app challenge db migrate -m "add due_date column"
flask --app challenge db upgrade

# 問題3：ルートを due_date 対応にしたら、メモ追加フォームで動作確認
python challenge.py
"""
import json
import os

from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

from forms import MemoForm

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

base_dir = os.path.dirname(__file__)
app.config['SQLALCHEMY_DATABASE_URI']        = 'sqlite:///' + os.path.join(base_dir, 'memos.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
SEED_JSON_PATH = os.path.join(base_dir, 'memos.json')

db = SQLAlchemy(app)
# TODO: 問題1 Migrate(app, db) でマイグレーションを有効にする


class Memo(db.Model):
    __tablename__ = 'memos'
    id       = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title    = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    body     = db.Column(db.String, nullable=False)
    # TODO: 問題2 due_date カラムを追加する（既存データが壊れないよう nullable にする）


def init_db():
    # テーブル自体は flask db upgrade で作成するため、ここでは
    # db.create_all() を呼ばない
    with app.app_context():
        count = Memo.query.count()
        if count == 0:
            # 初回起動時のみ memos.json から初期データを投入する
            with open(SEED_JSON_PATH, encoding='utf-8') as f:
                memos_data = json.load(f)
            db.session.add_all([Memo(**data) for data in memos_data])
            db.session.commit()


@app.route('/')
def memo_list():
    category = request.args.get('category')

    query = Memo.query
    if category:
        query = query.filter_by(category=category)
    memos = query.all()

    return render_template('top.html', memos=memos)


@app.route('/memos/<int:memo_id>')
def memo_detail(memo_id):
    memo = Memo.query.filter_by(id=memo_id).first()

    if memo:
        title = memo.title
        category = memo.category
        body = memo.body
        # TODO: 問題3 memo.due_date を使って due_date_line を作る（未設定なら空文字）
        due_date_line = ''
    else:
        title = f'メモID {memo_id} は見つかりません'
        category = ''
        body = ''
        due_date_line = ''

    return render_template(
        'detail.html',
        title=title,
        category=category,
        body=body,
        due_date_line=due_date_line,
    )


@app.route('/memos/new', methods=['GET', 'POST'])
def new_memo():
    form = MemoForm()

    if form.validate_on_submit():
        new = Memo(
            title=form.title.data,
            category=form.category.data,
            body=form.body.data,
        )
        # TODO: 問題3 new.due_date = form.due_date.data を設定する
        db.session.add(new)
        db.session.commit()

        return redirect(url_for('memo_list'))

    return render_template('new_memo.html', form=form)


@app.route('/old-memos')
def old_memos():
    return redirect(url_for('memo_list'))


if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5039)
