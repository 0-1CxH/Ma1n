import uuid
import os
from flask import render_template, request, url_for, request, send_file
from flask_login import login_required, current_user
from flask_socketio import SocketIO
from ..intelligence.constants import supported_process_functions


def register_main_routes(app, conversation_manager):

    socketio = SocketIO(app)

    @app.route('/')
    @login_required
    def home():
        username = current_user.username
        return render_template('index.html', username=username)

    @app.route('/get-process-funcs')
    def get_all_process_functions():
        return {"data": supported_process_functions}

    @app.route('/list-sessions')
    @login_required
    def get_sessions():
        all_session_info = conversation_manager.get_conversations_by_username(current_user)
        return render_template('history.html', username=current_user.username, all_session_info=all_session_info)

    @app.route('/submit-session', methods=['POST'])
    @login_required
    def submit_all_and_get_session_id():
        random_session_id = str(uuid.uuid4())
        username = current_user.username
        
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
        # print(f"{type(uploaded_files[0])}, {uploaded_files[0].filename=}, {uploaded_files[0].mimetype=}")

        conversation_manager.add_conversation_info(
            session_id=random_session_id,
            owner_username=username,
            all_submitted_content={
                "user_input": user_input,
                "uploaded_files": uploaded_files,
                "entered_links": entered_links,
                "selected_process_function": selected_process_function
            },
            socketio=socketio
        )
        return {"sessionId": random_session_id}

    @app.route('/fetch-session')
    @login_required
    def fetch_session_by_id():
        session_id = request.args.get('id')
        call_step_when_load = request.args.get('step')
        if call_step_when_load == "0":
            call_step_when_load = False
        else:
            call_step_when_load = True
        ret_dict = conversation_manager.get_session_info_by_id(session_id, current_user)
        if ret_dict["code"] == 0:
            return render_template(
                'conversation.html', 
                username=current_user.username,
                is_owner = ret_dict["is_owner"],
                session_id=session_id,
                conv_folder=ret_dict["conv_folder"],
                conv_nodes_file_content=ret_dict["conv_nodes_file_content"],
                call_step_when_load=call_step_when_load,
            )
        else:
            return ret_dict

    
    @app.route('/delete-session')
    def delete_session_by_id():
        session_id = request.args.get('id')
        return conversation_manager.delete_conversation_info(session_id, current_user)
    
    @app.route('/step', methods=['POST'])
    def take_intelligence_step_by_id():
        session_id = request.form.get('sessionId')
        selected_node_ids = request.form.get('selectedNodes', None)
        if selected_node_ids == '':
            selected_node_ids = None
        if selected_node_ids:
            selected_node_ids = selected_node_ids.split(";")
        user_input = request.form.get('userInput', None)
        reset_node = request.form.get('resetNode', None)
        username = current_user.username
        return conversation_manager.take_intelligence_step(
            session_id, 
            username,
            selected_node_ids,
            user_input,
            reset_node,
            socketio=socketio
        )
    
    @app.route('/download')
    def download_file_by_path():
        file_path = request.args.get("path")
        if not (os.path.basename(os.path.dirname(file_path)) in ["input_material", "output_material" ] or "abst.json" in file_path or "nodes.json" in file_path):
            return {"code": -3, "reason": "Congrats! you found this vulnerability, but it is fixed."}
        user_store_root = os.path.join(conversation_manager.conversation_store_root, current_user.username) 
        if file_path.startswith(user_store_root) or current_user.has_view_all_permission():
            try:
                return send_file(file_path, as_attachment=True)
            except Exception as e:
                return {"code":-2, "reason": e.__str__()}
        else:
            return {"code": -1, "reason": "No permission."}



