import uuid
from flask import render_template, request
from flask_login import login_required, current_user

def register_main_routes(app):

    @app.route('/')
    def home():
        return render_template('index.html')


    @app.route('/get-process-funcs')
    def get_all_process_functions():
        process_functions = [
            "Process",
            "Process Very Long Name For Test",
            "Other Funcs"
        ]
        return {"data": process_functions}

    @app.route('/list-sessions')
    @login_required
    def get_sessions():
        username = current_user.get_id()

        return render_template('history.html', username=username)

    @app.route('/submit-session', methods=['POST'])
    def submit_all_and_get_session_id():
        session_id = str(uuid.uuid4())
        return {"sessionId": session_id}

    @app.route('/fetch-session')
    def fetch_session_by_id():
        session_id = request.args.get('id')
        return render_template('session.html')