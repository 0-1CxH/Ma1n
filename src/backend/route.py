import uuid
import os
from flask import render_template, request, url_for
from flask_login import login_required, current_user


def register_main_routes(app, conversation_manager):

    @app.route('/')
    @login_required
    def home():
        username = current_user.username
        return render_template('index.html', username=username)


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
        username = current_user.username
        all_session_info = conversation_manager.get_conversations_by_username(username)
        return render_template('history.html', username=username, all_session_info=all_session_info)

    @app.route('/submit-session', methods=['POST'])
    @login_required
    def submit_all_and_get_session_id():
        random_session_id = str(uuid.uuid4())
        username = current_user.username
        filepath = os.path.join(conversation_manager.conversation_store_root, username, random_session_id)
        conversation_manager.add_conversation_info(session_id=random_session_id, owner_username=username, file_path=filepath)
        return {"sessionId": random_session_id}

    @app.route('/fetch-session')
    @login_required
    def fetch_session_by_id():
        session_id = request.args.get('id')
        username = current_user.username
        return render_template('conversation.html', username=username, )