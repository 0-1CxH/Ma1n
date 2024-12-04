import uuid
import os
from flask import render_template, request, url_for, request
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
        conversation_manager.add_conversation_info(session_id=random_session_id, owner_username=username, conversation_folder=filepath)

        user_input = request.form.get('userInput', "")
        uploaded_files = request.files.getlist('uploadedFiles')
        if uploaded_files is None:
            uploaded_files = []
        entered_links = request.form.get('enteredLinks')
        if entered_links:
            entered_links = [_.strip() for _ in entered_links.split("\n")]
        else:
            entered_links = []
        selected_process_function = request.form.get('selectedProcessFunction', "")

        # print(f"{user_input=}, {uploaded_files=}, {entered_links=}, {selected_process_function=}")
        conversation_manager.add_conversation_abstract(
            conversation_folder=filepath, 
            title = user_input[:50],
            note = f"{selected_process_function} of {len(uploaded_files)} file(s) and {len(entered_links)} link(s)"
        )
        return {"sessionId": random_session_id}

    @app.route('/fetch-session')
    @login_required
    def fetch_session_by_id():
        session_id = request.args.get('id')
        username = current_user.username
        return render_template('conversation.html', username=username, )
    
    @app.route('/delete-session')
    def delete_session_by_id():
        session_id = request.args.get('id')
        conversation_manager.delete_conversation_info(session_id)
        return {"sessionId": session_id}