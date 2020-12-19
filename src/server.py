import flask
from flask import jsonify, request

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"

@app.route('/results/', methods=["GET"])
def results():

    result = [
    {'Id': 0,
     'Link': '',
     'Result': '',
     'Confidence Score': '',
    ]

    toReturn = jsonify(result)
    toReturn.headers.add('Access-Control-Allow-Origin', '*')
    return toReturn


app.run()