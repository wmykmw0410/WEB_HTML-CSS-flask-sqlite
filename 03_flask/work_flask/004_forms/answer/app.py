from flask import Flask, render_template
import os
from forms import ContactForm

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)


@app.route('/', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        return render_template('result.html',
                               name=form.name.data,
                               email=form.email.data,
                               category=dict(form.category.choices)[form.category.data],
                               message=form.message.data)
    return render_template('input.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
