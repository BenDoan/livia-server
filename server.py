import json

from flask import Flask, request, g, make_response, send_file
from db_handler import db_handler

DATABASE = '/tmp/data.db'

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['TRAP_BAD_REQUEST_ERRORS'] = True

@app.route('/partials/<partial>')
def partials(partial):
    return send_file('partials/%s' % partial)

@app.route('/', methods=['GET', 'POST'])
def index():
    return make_response(open('templates/index.html').read())

@app.route('/projects/<projectname>/', methods=['GET', 'POST'])
def handle(projectname):
    if request.method == "POST":
        if request.form.get('entry', None):
            entry = request.form['entry']
            json_entry = json.loads(entry)
            g.db.insert_data(projectname,{
                "timestamp":json_entry['timestamp'],
                "logger":json_entry['logger'],
                "data":json_entry['data']
            })
        elif request.form.get('authentication', None):
            return "0"
        else:
            return str(g.db.add_logger(projectname))
            #return "1"
        return "hello"
    elif request.method == "GET" :
        #if projectname == "loggers" :
        #    return str(g.db.get_loggers("asdf"))
        vals={}
        checklist=["logger","mintime","maxtime"]
        for check in checklist :
            if check in request.args :
                vals[check]=request.args[check]
        return g.db.get_data(projectname,**vals)
    return "Hello"
@app.route('/loggers', methods=['GET'])
def getloggers():
    if "project" in request.args :
        return json.dumps(g.db.get_loggers(request.args["project"]))
    return json.dumps(g.db.get_loggers())

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
