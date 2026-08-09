from flask import Flask, render_template
from api.views import api_bp

app = Flask(__name__)
app.register_blueprint(api_bp)


@app.route('/map')
def show_map() -> str:
    return render_template('map.html')


if __name__ == '__main__':
    app.run(debug=True, port=5064)
