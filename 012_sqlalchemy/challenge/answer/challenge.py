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


class Memo(Base):
    __tablename__ = 'memos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    category = Column(String, nullable=False)
    body = Column(String, nullable=False)


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


@app.route('/')
def memo_list():
    category = request.args.get('category')

    session = Session()
    query = session.query(Memo)
    if category:
        query = query.filter_by(category=category)
    memos = query.all()
    session.close()

    return render_template('top.html', memos=memos)


@app.route('/memos/<int:memo_id>')
def memo_detail(memo_id):
    session = Session()
    memo = session.query(Memo).filter_by(id=memo_id).first()
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


@app.route('/memos/new', methods=['GET', 'POST'])
def new_memo():
    form = MemoForm()

    if form.validate_on_submit():
        session = Session()
        new = Memo(
            title=form.title.data,
            category=form.category.data,
            body=form.body.data,
        )
        session.add(new)
        session.commit()
        session.close()

        return redirect(url_for('memo_list'))

    return render_template('new_memo.html', form=form)


@app.route('/old-memos')
def old_memos():
    return redirect(url_for('memo_list'))


if __name__ == '__main__':
    app.run(debug=True, port=5035)
