from flask import Flask, render_template

app = Flask(__name__, template_folder='src/templates', static_folder='src/static')

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/procfuncs')
def get_all_process_functions():
    process_functions = [
        "Process A",
        "Process Very Long Name For Test",
        "Process C"
    ]
    return {"data": process_functions}


if __name__ == '__main__':
    app.run()