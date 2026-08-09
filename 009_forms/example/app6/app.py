import os
from flask import Flask, render_template, redirect, url_for
from werkzeug.utils import secure_filename
from forms import UploadForm

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)   # CSRFトークンの署名に必要

base_dir = os.path.dirname(__file__)
app.config['UPLOAD_FOLDER'] = os.path.join(base_dir, 'static', 'uploads')

# 学習用に簡略化してグローバル変数に保持（本来はDBに保存する）
uploaded_filename = None


@app.route('/', methods=['GET', 'POST'])
def upload():
    global uploaded_filename
    form = UploadForm()

    if form.validate_on_submit():
        if form.image.data and form.image.data.filename:
            filename = secure_filename(form.image.data.filename)
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            form.image.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            uploaded_filename = filename
        return redirect(url_for('upload'))

    return render_template('upload.html', form=form, filename=uploaded_filename)


if __name__ == '__main__':
    app.run(debug=True, port=5028)
