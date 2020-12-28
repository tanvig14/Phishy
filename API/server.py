import flask
import sys
from flask import jsonify, request
sys.path.append("..")
from src.extract import extractAllFeatures

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    result = {
    'working': 'Yes!'}
    
    toReturn = jsonify(result)
    toReturn.headers.add('Access-Control-Allow-Origin', '*')
    return toReturn

@app.route('/results/', methods=["GET"])
def results():
    """
    Uses the API call to pass the URL through the model and returns a JSON with the passed URL, the result as determined 
    by the Model and a confidence score. 

    Returns:
        [JSON String]: [Contains the orignal URL, the models result and a confidence score]
    """

    requestData = request.args
    URL = requestData.get("url")
    features = extractAllFeatures(URL)
    print(features)

    result = {
        'URL': URL,
        'Result': '',
        'Confidence Score': '',}
    
    toReturn = jsonify(result)
    toReturn.headers.add('Access-Control-Allow-Origin', '*')
    return toReturn

@app.route('/adv_results/', methods=["GET"])
def adv_results():
    """
    Uses the API call to pass the URL through the model and returns a JSON with the passed URL, the result as determined 
    by the Model and a confidence score along with the indiviual feature classification

    Returns:
        [JSON String]: [Contains the orignal URL, the models result and a confidence score along with the indiviual feature results]
    """

    requestData = request.args
    URL = requestData.get("url")

    result = {
        'URL': URL,
        'Result': '',
        'Confidence Score': '',
        'Features':''}
    
    toReturn = jsonify(result)
    toReturn.headers.add('Access-Control-Allow-Origin', '*')
    return toReturn

@app.route('/sendIt/', methods=["GET"])
def sendIt():
    print("Send it")


app.run()