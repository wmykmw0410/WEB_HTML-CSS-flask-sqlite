from flask import Flask, render_template
import os
from forms import InputForm

# Create Instance
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)


# Routing
@app.route('/', methods=['GET', 'POST'])
def input():
    form = InputForm()

    # POST: validate_on_submit() で CSRF 検証 + バリデーションを同時に行う
    if form.validate_on_submit():
        return render_template('output.html', name=form.name.data, email=form.email.data)

    # GET
    return render_template('input.html', form=form)


# Run
if __name__ == '__main__':
    app.run(debug=True) 