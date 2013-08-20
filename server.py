import json

from flask import Flask, request, g
from writer import log_writer

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['PROPAGATE_EXCEPTIONS'] = True

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST" and request.form['entry']:
        entry = request.form['entry']
        json_entry = json.loads(entry)
        g.db.insert_data({
            "timestamp":json_entry['timestamp'],
            "logger":json_entry['logger'],
            "data":json_entry['data']
        })
        return str(entry)
    elif request.method == "GET" :
        
    return "Hello"

@app.before_request
def before_request():
    g.db = log_writer()

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
