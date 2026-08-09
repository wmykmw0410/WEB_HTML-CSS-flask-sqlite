from flask import Flask, render_template, request

# Create Instance
app = Flask(__name__)


# Routing
from forms import UserInfoForm


# User Information : Input
@app.route('/', methods=['GET', 'POST'])
def show_enter():
    # Create form
    form = UserInfoForm(request.form)
    # POST
    if request.method == "POST":
        return render_template('result.html', form=form)
    # GET
    return render_template('enter.html', form=form)


# Run
if __name__ == '__main__':
    app.run(debug=True, port=5024)