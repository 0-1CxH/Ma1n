import os 
import uuid
from flask import Flask, render_template, request
from flask_login import login_required
from src.backend.login import auth_blueprint, init_login_manager
from src.backend.user import User
from src.backend.route import register_main_routes

app = Flask(__name__, template_folder='src/templates', static_folder='src/static')

app.secret_key = os.getenv('FLASK_SECRET_KEY')

app.register_blueprint(auth_blueprint, url_url_prefix='/auth')
init_login_manager(app, 'auth.login')


register_main_routes(app)


if __name__ == '__main__':
    app.run()