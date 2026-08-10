import json
import os

from flask import Flask, redirect, render_template, request, url_for

from forms import MemoForm

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

MEMOS_PATH = os.path.join(os.path.dirname(__file__), 'memos.json')

with open(MEMOS_PATH, encoding='utf-8') as f:
    memos_list = json.load(f)

memos = {i + 1: memo for i, memo in enumerate(memos_list)}


@app.route('/')
def memo_list():
    category = request.args.get('category')

    memo_list_data = [{"id": memo_id, **memo} for memo_id, memo in memos.items()]

    if category:
        memo_list_data = [m for m in memo_list_data if m["category"] == category]

    return render_template('top.html', memos=memo_list_data)


@app.route('/memos/<int:memo_id>')
def memo_detail(memo_id):
    memo = memos.get(memo_id)

    if memo:
        title = memo['title']
        category = memo['category']
        body = memo['body']
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
        new_memo_data = {
            'title': form.title.data,
            'category': form.category.data,
            'body': form.body.data,
        }
        memos_list.append(new_memo_data)
        memos[len(memos_list)] = new_memo_data

        with open(MEMOS_PATH, 'w', encoding='utf-8') as f:
            json.dump(memos_list, f, ensure_ascii=False, indent=2)

        return redirect(url_for('memo_list'))

    return render_template('new_memo.html', form=form)


@app.route('/old-memos')
def old_memos():
    return redirect(url_for('memo_list'))


if __name__ == '__main__':
    app.run(debug=True, port=5031)
