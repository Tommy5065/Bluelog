from flask import Blueprint, render_template

bp = Blueprint('admin',__name__)

@bp.route('/Write')
def new_post():
    return render_template('')