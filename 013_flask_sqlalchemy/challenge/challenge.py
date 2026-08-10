"""
練習問題：メモデータの保存先を SQLAlchemy（生）から Flask-SQLAlchemy に変更しよう

012_sqlalchemyで作ったメモ一覧・詳細・追加フォーム・リダイレクトの見た目や機能はそのままです。
データの持ち方だけを、engine / Session を自分で管理する書き方から
Flask-SQLAlchemy（db.Model / db.session / app_context）に置き換えます。

以下の TODO コメントの箇所にコードを書いて完成させてください。
実行方法: python challenge/challenge.py
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


# ============================================================
# 問題1：Memo モデルを db.Model で定義してテーブルを作成する
# カラムは id / title / category / body（012_sqlalchemyと同じ）
# ============================================================
class Memo(db.Model):
    __tablename__ = 'memos'
    pass  # ← ここを実装


def init_db():
    with app.app_context():
        # TODO: db.create_all() でテーブルを作成する

        count = Memo.query.count()
        if count == 0:
            # 初回起動時のみ memos.json から初期データを投入する
            with open(SEED_JSON_PATH, encoding='utf-8') as f:
                memos_data = json.load(f)
            db.session.add_all([Memo(**data) for data in memos_data])
            db.session.commit()


init_db()


# ============================================================
# 問題2：メモ一覧を取得する
# category が指定されていれば filter_by(category=category) で絞り込み、
# 指定が無ければ全件取得すること
# @app.route の中は Flask がコンテキストを自動で用意するので
# with app.app_context(): は不要
# ============================================================
@app.route('/')
def memo_list():
    category = request.args.get('category')

    # TODO: Memo.query を使って memos を取得する
    memos = []

    return render_template('top.html', memos=memos)


# ============================================================
# 問題3：id を指定してメモを1件取得する
# 見つからない場合の表示（title/category/body）はこれまでと同じ
# ============================================================
@app.route('/memos/<int:memo_id>')
def memo_detail(memo_id):
    # TODO: Memo.query.filter_by(id=memo_id).first() で memo を取得する
    memo = None

    if memo:
        title = memo.title
        category = memo.category
        body = memo.body
    else:
        title = f'メモID {memo_id} は見つかりません'
        category = ''
        body = ''

    return render_template(
        'detail.html',
        title=title,
        category=category,
        body=body,
    )


# ============================================================
# 問題4：新しいメモを追加する
# Memo インスタンスを作って db.session.add() → db.session.commit() すること
# ============================================================
@app.route('/memos/new', methods=['GET', 'POST'])
def new_memo():
    form = MemoForm()

    if form.validate_on_submit():
        # TODO: Memo(...) を作って db.session.add() → db.session.commit() する

        return redirect(url_for('memo_list'))

    return render_template('new_memo.html', form=form)


@app.route('/old-memos')
def old_memos():
    return redirect(url_for('memo_list'))


if __name__ == '__main__':
    app.run(debug=True, port=5036)
