"""
練習問題：メモデータの保存先を sqlite3（生SQL）から SQLAlchemy（ORM）に変更しよう

011_sqliteで作ったメモ一覧・詳細・追加フォーム・リダイレクトの見た目や機能はそのままです。
データの持ち方だけを、sqlite3モジュールで直接SQLを書く方式から
SQLAlchemyのORM（Memo モデル + Session）に置き換えます。

以下の TODO コメントの箇所にコードを書いて完成させてください。
実行方法: python challenge/challenge.py
"""
import json
import os

from flask import Flask, redirect, render_template, request, url_for
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

from forms import MemoForm

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

base_dir = os.path.dirname(__file__)
DB_PATH = os.path.join(base_dir, 'memos.db')
SEED_JSON_PATH = os.path.join(base_dir, 'memos.json')

engine = create_engine('sqlite:///' + DB_PATH)
Base = declarative_base()
Session = sessionmaker(bind=engine)


# ============================================================
# 問題1：Memo モデルを定義する
# カラムは id / title / category / body
# （id は主キー・自動採番、他は NOT NULL）
# ============================================================
class Memo(Base):
    __tablename__ = 'memos'
    pass  # ← ここを実装


def init_db():
    Base.metadata.create_all(engine)

    session = Session()
    count = session.query(Memo).count()
    if count == 0:
        # 初回起動時のみ memos.json から初期データを投入する
        with open(SEED_JSON_PATH, encoding='utf-8') as f:
            memos_data = json.load(f)
        session.add_all([Memo(**data) for data in memos_data])
        session.commit()
    session.close()


init_db()


# ============================================================
# 問題2：メモ一覧を取得する
# category が指定されていれば filter_by(category=category) で絞り込み、
# 指定が無ければ全件取得すること
# ============================================================
@app.route('/')
def memo_list():
    category = request.args.get('category')

    session = Session()
    # TODO: session.query(Memo) を使って memos を取得する
    memos = []
    session.close()

    return render_template('top.html', memos=memos)


# ============================================================
# 問題3：id を指定してメモを1件取得する
# 見つからない場合の表示（title/category/body）はこれまでと同じ
# ============================================================
@app.route('/memos/<int:memo_id>')
def memo_detail(memo_id):
    session = Session()
    # TODO: session.query(Memo).filter_by(id=memo_id).first() で memo を取得する
    memo = None
    session.close()

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
# Memo インスタンスを作って session.add() → session.commit() すること
# ============================================================
@app.route('/memos/new', methods=['GET', 'POST'])
def new_memo():
    form = MemoForm()

    if form.validate_on_submit():
        session = Session()
        # TODO: Memo(...) を作って session.add() → session.commit() する
        session.close()

        return redirect(url_for('memo_list'))

    return render_template('new_memo.html', form=form)


@app.route('/old-memos')
def old_memos():
    return redirect(url_for('memo_list'))


if __name__ == '__main__':
    app.run(debug=True, port=5034)
