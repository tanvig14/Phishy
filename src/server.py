import flask
from flask import jsonify, request

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    return "<h1>Looks Like the API is working just fine!</h1><p>This site is a prototype API for phishing detection</p>"

@app.route('/results', methods=["GET"])
def results():

    requestData = request.args
    url = requestData.get("url")
    print(url)

    result = [
    {'Link': url,
     'Result': '',
     'Confidence Score': '',}
    ]

    toReturn = jsonify(result)
    toReturn.headers.add('Access-Control-Allow-Origin', '*')
    return toReturn


app.run()