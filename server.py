import json

from flask import Flask, request, g
from db_handler import db_handler

DATABASE = '/tmp/data.db'

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['PROPAGATE_EXCEPTIONS'] = True


@app.route('/projects/<projectname>/', methods=['GET', 'POST'])
def handle(projectname):
    if request.method == "POST":
        if request.form.get('entry', None):
            entry = request.form['entry']
            json_entry = json.loads(entry)
            g.db.insert_data({
                "timestamp":json_entry['timestamp'],
                "logger":json_entry['logger'],
                "data":json_entry['data']
            })
        elif request.form.get('authentication', None):
            return "0"
        else:
            return "1"
        return "hello"
    elif request.method == "GET" :
        vals={}
        checklist=["logger","mintime","maxtime"]
        for check in checklist :
            if check in request.args :
                vals[check]=request.args[check]
        return g.db.get_data(**vals)
    return "Hello"

@app.before_request
def before_request():
    g.db = db_handler(DATABASE)

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

def get_data(self): return {
                "timestamp":1376948822,
                "logger":1,
                "data":"5000"
            }

if __name__ == "__main__":
    app.run(host="0.0.0")
