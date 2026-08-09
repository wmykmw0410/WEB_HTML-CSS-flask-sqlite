from flask import Flask

# Create instance
app = Flask(__name__)


# Routing
# Top Page
@app.route("/")
def index():
    return '<h1>Top Page</h1>'


# Item List
@app.route("/list")
def item_list():
    return '<h1>Item List Page</h1>'


# Item Detail
@app.route("/detail")
def item_detail():
    return '<h1>Item Detail Page</h1>'


# Run
if __name__ == '__main__':
    app.run(debug=True, port=5002)