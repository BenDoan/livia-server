import json

from functools import wraps
from flask import Flask, request, g, make_response, send_file, request, Response
from db_handler import db_handler

DATABASE = '/tmp/data.db'

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['TRAP_BAD_REQUEST_ERRORS'] = True

def check_auth(username, password):
    return username == 'admin' and password == 'password'

def authenticate():
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

@app.route('/partials/<partial>')
def partials(partial):
    return send_file('partials/%s' % partial)

@app.route('/', methods=['GET', 'POST'])
@requires_auth
def index():
    return make_response(open('templates/index.html').read())

@app.route('/projects/<projectname>/', methods=['GET', 'POST'])
def handle(projectname):
    if request.method == "POST":
        if request.form.get('entry', None):
            entry = request.form['entry']
            json_entry = json.loads(entry)
            g.db.insert_data(projectname,request.form['key'],{
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
    return ":)"

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

if __name__ == "__main__":
    app.run(host="0.0.0")
