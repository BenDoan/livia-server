import json

from flask import Flask, request, g, make_response, send_file
from db_handler import db_handler

import server_state

DATABASE = '/tmp/data.db'

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['TRAP_BAD_REQUEST_ERRORS'] = True

#@app.before_first_request
#def start():
#    g.loggeraccept=server_state.loggeraccept()

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
    elif request.method == "GET" :
        vals={}
        checklist=["logger","mintime","maxtime"]
        for check in checklist :
            if check in request.args :
                vals[check]=request.args[check]
        return g.db.get_data(projectname,**vals)

    return "I dont know what you are talking about"

@app.route('/projects/<projectname>/addlogger/')
def add_logger(projectname):
    l=server_state.loggeraccept("loggerconfig.json")
    if l.addlogger() :
        l.write("loggerconfig.json")
        return str(g.db.add_logger(projectname))
    else :
        return "NO SOUP FOR YOU!"

@app.route('/register/')
def register():
    l=server_state.loggeraccept("loggerconfig.json")
    if "usetime" in request.args :
        l.usetime=bool(request.args["usetime"])
    if "endtime" in request.args :
        l.endtime=float(request.args["endtime"])
    if "numleft" in request.args :
        l.numleft=int(request.args["numleft"])
    l.write("loggerconfig.json")
    return json.dumps({"usetime":l.usetime,"endtime":l.endtime,"numleft":l.numleft})

@app.route('/loggers/', methods=['GET'])
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
