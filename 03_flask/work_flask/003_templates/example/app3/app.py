from flask import Flask, render_template

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
@app.route("/detail/<int:id>")
def item_detail(id):
    return render_template('detail.html', show_id=id)


# Run
if __name__ == '__main__':
    app.run()