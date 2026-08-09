"""
練習問題：書籍データの保存先を sqlite3（生SQL）から SQLAlchemy（ORM）に変更しよう

011_sqliteで作った書籍一覧・詳細・追加フォーム・リダイレクトの見た目や機能はそのままです。
データの持ち方だけを、sqlite3モジュールで直接SQLを書く方式から
SQLAlchemyのORM（Book モデル + Session）に置き換えます。

以下の TODO コメントの箇所にコードを書いて完成させてください。
実行方法: python challenge/challenge.py
"""
import json
import os

from flask import Flask, redirect, render_template, request, url_for
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
from werkzeug.utils import secure_filename

from forms import BookForm

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

base_dir = os.path.dirname(__file__)
DB_PATH = os.path.join(base_dir, 'books.db')
SEED_JSON_PATH = os.path.join(base_dir, 'books.json')
STATIC_IMG_DIR = os.path.join(base_dir, 'static', 'img')

engine = create_engine('sqlite:///' + DB_PATH)
Base = declarative_base()
Session = sessionmaker(bind=engine)


# ============================================================
# 問題1：Book モデルを定義する
# カラムは id / title / author / price / image
# （id は主キー・自動採番、他は NOT NULL）
# ============================================================
class Book(Base):
    __tablename__ = 'books'
    pass  # ← ここを実装


def init_db():
    Base.metadata.create_all(engine)

    session = Session()
    count = session.query(Book).count()
    if count == 0:
        # 初回起動時のみ books.json から初期データを投入する
        with open(SEED_JSON_PATH, encoding='utf-8') as f:
            books_data = json.load(f)
        session.add_all([Book(**data) for data in books_data])
        session.commit()
    session.close()


init_db()


# ============================================================
# 問題2：書籍一覧を取得する
# author が指定されていれば filter_by(author=author) で絞り込み、
# 指定が無ければ全件取得すること
# ============================================================
@app.route('/')
def book_list():
    author = request.args.get('author')

    session = Session()
    # TODO: session.query(Book) を使って books を取得する
    books = []
    session.close()

    return render_template('top.html', books=books)


# ============================================================
# 問題3：id を指定して書籍を1件取得する
# 見つからない場合の表示（title/author_line/price_line/image）は
# これまでと同じ
# ============================================================
@app.route('/books/<int:book_id>')
def book_detail(book_id):
    session = Session()
    # TODO: session.query(Book).filter_by(id=book_id).first() で book を取得する
    book = None
    session.close()

    if book:
        title = book.title
        author_line = f"著者: {book.author}"
        price_line = f"¥{book.price}"
        image = f"/static/img/{book.image}"
    else:
        title = f'書籍ID {book_id} は見つかりません'
        author_line = ''
        price_line = ''
        image = '/static/img/not_found.png'

    return render_template(
        'detail.html',
        title=title,
        author_line=author_line,
        price_line=price_line,
        image=image,
    )


# ============================================================
# 問題4：新しい書籍を追加する
# Book インスタンスを作って session.add() → session.commit() すること
# ============================================================
@app.route('/books/new', methods=['GET', 'POST'])
def new_book():
    form = BookForm()

    if form.validate_on_submit():
        image_filename = 'not_found.png'
        if form.image.data and form.image.data.filename:
            image_filename = secure_filename(form.image.data.filename)
            os.makedirs(STATIC_IMG_DIR, exist_ok=True)
            form.image.data.save(os.path.join(STATIC_IMG_DIR, image_filename))

        session = Session()
        # TODO: Book(...) を作って session.add() → session.commit() する
        session.close()

        return redirect(url_for('book_list'))

    return render_template('new_book.html', form=form)


@app.route('/old-books')
def old_books():
    return redirect(url_for('book_list'))


if __name__ == '__main__':
    app.run(debug=True, port=5034)
