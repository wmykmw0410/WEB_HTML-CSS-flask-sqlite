from flask import Flask, render_template, session, redirect, url_for
import os
from forms import InputForm

# Create Instance
app = Flask(__name__)
# Set a random number
app.config['SECRET_KEY'] = os.urandom(24)


# Routing
# Input
@app.route('/', methods=['GET', 'POST'])
def input():
    form = InputForm()

    # POST
    if form.validate_on_submit():
        session['name'] = form.name.data
        session['email'] = form.email.data
        return redirect(url_for('output'))
    
    # GET
    if 'name' in session:
        form.name.data = session['name']
    if 'email' in session:
        form.email.data = session['email']
    return render_template('input.html', form=form)


# Output
@app.route('/output')
def output():
    return render_template('output.html')


# Run
if __name__ == '__main__':
    app.run(debug=True, port=5027) 