#push
from flask import Flask
from flask import jsonify

app = Flask(__name__)

@app.route('/')
def hello():
    val = "hello world"
    return jsonify(val)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)