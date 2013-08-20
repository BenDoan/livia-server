from flask import Flask
from flask import request

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['PROPAGATE_EXCEPTIONS'] = True

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        print(request.form[0])
        return "Hello"
    return "Hello"

if __name__ == "__main__":
    app.run(host="0.0.0")
