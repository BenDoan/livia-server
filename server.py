"""
TODO:
- edit logger descriptions
"""
import json

from functools import wraps
from flask import Flask, request, g, make_response, send_file, request, Response, redirect
from db_handler import db_handler

DATABASE = '/tmp/data.db'
USERNAME = "admin"
PASSWORD = "password"

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['TRAP_BAD_REQUEST_ERRORS'] = True

def check_auth(username, password):
    """defines username and password"""
    return username == USERNAME and password == PASSWORD

def authenticate():
    """helper method for authenticator"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    """a decorator for adding authentication to a route"""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

@app.route('/partials/<partial>')
def partials(partial):
    """send the partials (views) required by angular"""
    return send_file('partials/%s' % partial)

@app.route('/', methods=['GET', 'POST'])
@requires_auth
def index():
    """servers the angular main page"""
    return make_response(open('templates/index.html').read())

@app.route('/projects/<projectname>/', methods=['GET'])
def return_data(projectname):
    """returns data for a project in json format"""
    if request.method == "GET" :
        from functools import reduce
        vals={}
        checklist=["logger","mintime","maxtime"]
        for check in checklist :
            if check in request.args :
                vals[check]=request.args[check]
        #dat = list(map(lambda x : '{{"logger":{logger},"timestamp":{timestamp},"data":"{data}"}}'.format(x),g.db.get_data(projectname,**vals)))
        dat=list(map(lambda x : '{{"timestamp":{},"logger":{},"data":{} }}'.format(x["timestamp"],x["logger"],x["data"]),g.db.get_data(projectname,**vals)))
        if len(dat) :
            return "["+reduce(lambda x,y : x + "," + y,dat) + "]"
        return "[]"
    return "I dont know what you are talking about"

@app.route('/projects/<projectname>/submit', methods=['POST'])
def add_data(projectname):
    """used by loggers to submit data"""
    if request.method == "POST":
        if request.form.get('apikey', None) in g.db.get_api_keys():
            entry = request.form['entry']
            json_entry = json.loads(entry)
            logger = g.db.get_logger(request.form['apikey'])
            g.db.add_data(projectname,{
                "timestamp":json_entry['timestamp'],
                "logger":logger,
                "data":json.dumps(json_entry['data'])
            })
            return "success"
        else:
            return "Wrong api key: " + str(request.form.get('apikey', None))
    return "Error"

@app.route('/projects/<projectname>/addlogger/', methods=['get'])
@requires_auth
def add_logger(projectname):
    """adds a new logger, used internally"""
    if request.method == "GET":
        if request.args.get('description', None):
            return str(g.db.add_logger(projectname, request.args['description']))
    return "NO SOUP FOR YOU!"

@app.route('/projects/')
@requires_auth
def getprojects():
    """returns a json list of all projects"""
    return json.dumps(g.db.get_projects())

@app.route('/loggers/', methods=['GET'])
def getloggers():
    """returns a json list of all projects"""
    if "project" in request.args :
        return json.dumps(g.db.get_loggers(request.args["project"]))
    return json.dumps(g.db.get_loggers())

@app.route('/data/', methods = ['GET'])
def getdatatree():
    """a more complex api for getting data"""
    hide=[]
    if "hide" in request.args :
        hidden=json.loads(request.args["hide"])
    projects=g.db.get_projects()
    tree = {}
    for project in projects :
        tree[project]=g.db.get_loggers(project)
        for logger in tree[project] :
            logger["data"]=g.db.get_data(project,logger=logger["id"],**request.args)
    return json.dumps(tree)

@app.before_request
def before_request():
    """instantiates a new database object and stores it as a global variable"""
    g.db = db_handler(DATABASE)

@app.teardown_request
def teardown_request(exception):
    """closes the database"""
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

if __name__ == "__main__":
    app.run(host="0.0.0")
