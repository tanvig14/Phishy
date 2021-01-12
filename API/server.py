import flask
import sys
import pickle
from flask import jsonify, request, render_template
sys.path.append("..")
from src.extract import extractAllFeatures
import csv
import time

app = flask.Flask(__name__)
app.config["DEBUG"] = True

model = pickle.load(open('../models/final_model.pkl', 'rb'))

@app.route('/', methods=['GET'])
def home():
    result = {
    'working': True}

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
        list = [features[x] for x in features]
        featureList = [list]

        prediction = model.predict(featureList)
        counter = 0
        for val in list:
            if int(val) == prediction[0]:
                counter = counter + 1
            
        csv_columns = [
            "Time",
            "URL",
            "having_IP_Address",
            "URL_Length",
            "Shortining_Service",
            "having_At_Symbol",
            "double_slash_redirecting",
            "Prefix_Suffix",
            "having_Sub_Domain",
            "SSLfinal_State",
            "Favicon",
            "port",
            "HTTPS_token",
            "Submitting_to_email",
            "Redirect",
            "age_of_domain",
            "Result"
            ]
        dict_data = [
            {
            'Time':time.localtime(),
            'URL':URL,         
            "having_IP_Address": features["having_IP_Address"],
            "URL_Length": features["URL_Length"],
            "Shortining_Service": features["Shortining_Service"],
            "having_At_Symbol": features["having_At_Symbol"],
            "double_slash_redirecting": features["double_slash_redirecting"],
            "Prefix_Suffix": features["Prefix_Suffix"],
            "having_Sub_Domain": features["having_Sub_Domain"],
            "SSLfinal_State": features["SSLfinal_State"],
            "Favicon": features["Favicon"],
            "port": features["port"],
            "HTTPS_token": features["HTTPS_token"],
            "Submitting_to_email": features["Submitting_to_email"],
            "Redirect": features["Redirect"],
            "age_of_domain": features["age_of_domain"],
            "Result": prediction[0],}
            ]
        csv_file = "data/results.csv"
        with open(csv_file, 'a') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            for data in dict_data:
                writer.writerow(data)

        result = {
            'URL': URL,
            'Result': str(prediction[0]),
            'Confidence Score': str(counter/14),}
        
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
        list = [features[x] for x in features]
        featureList = [list]

        prediction = model.predict(featureList)
        counter = 0
        for val in list:
            if int(val) == prediction[0]:
                counter = counter + 1

        csv_columns = [
            "Time",
            "URL",
            "having_IP_Address",
            "URL_Length",
            "Shortining_Service",
            "having_At_Symbol",
            "double_slash_redirecting",
            "Prefix_Suffix",
            "having_Sub_Domain",
            "SSLfinal_State",
            "Favicon",
            "port",
            "HTTPS_token",
            "Submitting_to_email",
            "Redirect",
            "age_of_domain",
            "Result"
            ]
        dict_data = [
            {
            'Time':time.localtime(),
            'URL':URL,         
            "having_IP_Address": features["having_IP_Address"],
            "URL_Length": features["URL_Length"],
            "Shortining_Service": features["Shortining_Service"],
            "having_At_Symbol": features["having_At_Symbol"],
            "double_slash_redirecting": features["double_slash_redirecting"],
            "Prefix_Suffix": features["Prefix_Suffix"],
            "having_Sub_Domain": features["having_Sub_Domain"],
            "SSLfinal_State": features["SSLfinal_State"],
            "Favicon": features["Favicon"],
            "port": features["port"],
            "HTTPS_token": features["HTTPS_token"],
            "Submitting_to_email": features["Submitting_to_email"],
            "Redirect": features["Redirect"],
            "age_of_domain": features["age_of_domain"],
            "Result": prediction[0],}
            ]
        csv_file = "data/results.csv"
        with open(csv_file, 'a') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            for data in dict_data:
                writer.writerow(data)

        result = {
            'URL': URL,
            'Result': str(prediction[0]),
            'Confidence Score': counter/14,
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

@app.route('/report/', methods=["GET"])
def logReport():
    requestData = request.args
    URL = requestData.get("url")

    try:
        features = extractAllFeatures(URL)
        del features['Domain_registration_length']
        list = [features[x] for x in features]
        featureList = [list]

        prediction = model.predict(featureList)
        counter = 0
        for val in list:
            if int(val) == prediction[0]:
                counter = counter + 1

        csv_columns = [
            "Time",
            "URL",
            "having_IP_Address",
            "URL_Length",
            "Shortining_Service",
            "having_At_Symbol",
            "double_slash_redirecting",
            "Prefix_Suffix",
            "having_Sub_Domain",
            "SSLfinal_State",
            "Favicon",
            "port",
            "HTTPS_token",
            "Submitting_to_email",
            "Redirect",
            "age_of_domain",
            "Result"
            ]
        dict_data = [
            {
            "Time": time.localtime(),    
            'URL':URL,         
            "having_IP_Address": features["having_IP_Address"],
            "URL_Length": features["URL_Length"],
            "Shortining_Service": features["Shortining_Service"],
            "having_At_Symbol": features["having_At_Symbol"],
            "double_slash_redirecting": features["double_slash_redirecting"],
            "Prefix_Suffix": features["Prefix_Suffix"],
            "having_Sub_Domain": features["having_Sub_Domain"],
            "SSLfinal_State": features["SSLfinal_State"],
            "Favicon": features["Favicon"],
            "port": features["port"],
            "HTTPS_token": features["HTTPS_token"],
            "Submitting_to_email": features["Submitting_to_email"],
            "Redirect": features["Redirect"],
            "age_of_domain": features["age_of_domain"],
            "Result": prediction[0],}
            ]
        csv_file = "data/reports.csv"
        with open(csv_file, 'a') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            for data in dict_data:
                writer.writerow(data)

        result = {
            'URL': URL,
            'Logged': True,
            'Time': time.localtime(),
        }
        
        toReturn = jsonify(result)
        toReturn.headers.add('Access-Control-Allow-Origin', '*')
        return toReturn
    except:
        result = {
            'URL': URL,
            'Logged': False,
            'Time': time.localtime(),
        }

        toReturn = jsonify(result)
        toReturn.headers.add('Access-Control-Allow-Origin', '*')
        return toReturn
    


app.run()