from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user, LoginManager
from .user import User, load_user # Import the User class from user.py

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Here you would verify the login credentials
        user = User()
        # Assuming the user's ID is set to 1 for the example
        user.id = '1'
        print(f"Username: {request.form.get('username')}")
        print(f"Password: {request.form.get('password')}")
        login_user(user)
        return redirect(url_for('home'))
    return render_template('login.html')

@auth_blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

def init_login_manager(app, login_view):
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = login_view
    login_manager.user_loader(load_user)
    return login_manager