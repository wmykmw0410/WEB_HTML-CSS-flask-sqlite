from flask import Flask, request

# Create Instance
app = Flask(__name__)

# Routing
# Get data with "GET"
@app.route("/get")
def do_get():
    name = request.args.get('name')
    return f'Hello, {name}!'


# Get data with "POST"
@app.route("/", methods=['GET', 'POST'])
def do_get_post():
    if request.method == 'POST':
        name = request.form.get('name')
        return f'Hello, {name}!'
    
    return """
    <h2>Send with POST</h2>
    <form method="post">
    Name : <input type="text" name="name">
    <input type="submit" value="post">
    </form>
    """

# Run
if __name__ == '__main__':
    app.run(debug=True)