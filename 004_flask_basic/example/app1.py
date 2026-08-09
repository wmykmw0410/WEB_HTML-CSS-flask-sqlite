from flask import Flask

# Create instance
app = Flask(__name__)

# Routing
@app.route("/")
def hello_world():
    return '<h1>Hello World!</h1>'

# Run
if __name__ == '__main__':
    app.run(debug=True, port=5001)