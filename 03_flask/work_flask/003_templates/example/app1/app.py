from flask import Flask, render_template, url_for

# Create instance
app = Flask(__name__)


# Routing
# Top Page
@app.route("/")
def index():
    return render_template('top.html')


# Item List
@app.route("/list")
def item_list():
    return render_template('list.html')


# Item Detail
@app.route("/detail")
def item_detail():
    return render_template('detail.html')


# Run
if __name__ == '__main__':
    app.run()