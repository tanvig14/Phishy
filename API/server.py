import flask
import sys
import pickle
from flask import jsonify, request
sys.path.append("..")
from src.extract import extractAllFeatures

app = flask.Flask(__name__)
app.config["DEBUG"] = True

model = pickle.load(open('../models/final_model.pkl', 'rb'))

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
    try:
        features = extractAllFeatures(URL)
        del features['Domain_registration_length']
        featureList = [features[x] for x in features]
        featureList = [featureList]

        prediction = model.predict(featureList)
        print(prediction)

        result = {
            'URL': URL,
            'Result': str(prediction[0]),
            'Confidence Score': '',}
        
        toReturn = jsonify(result)
        toReturn.headers.add('Access-Control-Allow-Origin', '*')
        return toReturn
    except:
        result = {
            'URL': URL,
            'Result': 0,
            'Confidence Score': 0,}
        
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

    try:
        features = extractAllFeatures(URL)
        del features['Domain_registration_length']
        featureList = [features[x] for x in features]
        featureList = [featureList]

        prediction = model.predict(featureList)
        print(prediction)

        result = {
            'URL': URL,
            'Result': str(prediction[0]),
            'Confidence Score': '',
            'Features': features}
        
        toReturn = jsonify(result)
        toReturn.headers.add('Access-Control-Allow-Origin', '*')
        return toReturn
    except:
        result = {
            'URL': URL,
            'Result': 0,
            'Confidence Score': 0,
            'Features': None}
        
        toReturn = jsonify(result)
        toReturn.headers.add('Access-Control-Allow-Origin', '*')
        return toReturn
    

@app.route('/sendIt/', methods=["GET"])
def sendIt():
    print("Send it")


app.run()