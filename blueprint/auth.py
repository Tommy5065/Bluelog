from flask_login import login_user, current_user, logout_user, login_required
from bluelog.models import Admin
from bluelog.forms import LoginForm
from bluelog.helpers import redirect_up
from flask import Blueprint, flash, render_template

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST','GET'])
def login():
    if current_user.is_authenticated:
        return redirect_up()
    else:
        form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data
        admin = Admin.query.first()

        if admin:
            if username == admin.adminName and admin.validate_password_hash(password):
                login_user(admin,remember)  # remember参数为True，创建remember_token的cookie实现用户重新打开浏览器恢复之前的状态
                flash(f'Welcome back {admin.name}','info')
                return redirect_up()
            flash('Invalid username or password','warning')
        else:
            flash('No account','warning')

    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Successfully logout', 'info')
    return redirect_up()