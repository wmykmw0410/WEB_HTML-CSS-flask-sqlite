from flask import Blueprint, render_template

two_bp = Blueprint('two_app', __name__, url_prefix='/two')


@two_bp.route('/')
def show_template() -> str:
    return render_template('two/index.html')
