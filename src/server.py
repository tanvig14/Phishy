import flask
from flask import jsonify, request

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    return "<h1>Looks Like the API is working just fine!</h1><p>This site is a prototype API for phishing detection</p>"

@app.route('/results', methods=["GET"])
def results():
    """
    Uses the API call to pass the URL through the model and returns a JSON with the passed URL, the result as determined 
    by the Model and a confidence score. 

    Returns:
        [JSON String]: [Contains the orignal URL, the models result and a confidence score]
    """

    requestData = request.args
    url = requestData.get("url")
    print(url)

    result = [
    {'URL': url,
     'Result': '',
     'Confidence Score': '',}
    ]

    toReturn = jsonify(result)
    toReturn.headers.add('Access-Control-Allow-Origin', '*')
    return toReturn


app.run()