import uuid
from flask import Flask, render_template, request

app = Flask(__name__, template_folder='src/templates', static_folder='src/static')

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
def get_sessions():
    return render_template('history.html')

@app.route('/submit-session', methods=['POST'])
def submit_all_and_get_session_id():
    session_id = str(uuid.uuid4())
    return {"sessionId": session_id}

@app.route('/fetch-session')
def fetch_session_by_id():
    session_id = request.args.get('id')
    return render_template('session.html')


if __name__ == '__main__':
    app.run()