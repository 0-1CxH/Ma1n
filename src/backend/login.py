from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user, LoginManager
from .user import User, UserManager # Import the User class from user.py

auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        is_correct = UserManager.user_manager_instance.authenticate(username, password)

        if is_correct:
            user = UserManager.user_manager_instance.load_user(username)
            login_user(user)
            next_page = request.form.get('next')
            print(f"{next_page}=")
            if not next_page:
                next_page = url_for('home')
            return redirect(next_page)
        else:
            return render_template('login.html', error="Invalid username or password")
    else:
        return render_template('login.html')

@auth_blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

def init_login_manager(app, login_view, user_db_path):
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = login_view
    global global_user_manager
    UserManager(user_db_path)
    login_manager.user_loader(UserManager.user_manager_instance.load_user)
    return login_manager