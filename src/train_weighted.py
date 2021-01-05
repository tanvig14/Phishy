import numpy as np
import pandas as pd
from scipy.io.arff import loadarff 
from sklearn.model_selection import train_test_split
from sklearn.metrics import *
from sklearn.svm import SVC
import pickle

droppedFeatures = [
    'Abnormal_URL',
    'DNSRecord',
    'web_traffic',
    'Page_Rank',
    'Google_Index',
    'Links_pointing_to_page',
    'Statistical_report',
    'Request_URL',
    'URL_of_Anchor',
    'Links_in_tags',
    'SFH',
    'on_mouseover',
    'RightClick',
    'popUpWidnow',
    'Iframe',
    'Domain_registeration_length',
]

# Loading data and decoding it appropriately.
raw_data = loadarff(open('../data/data.arff','r',encoding='UTF-8'))
df = pd.DataFrame(raw_data[0])
str_df = df.select_dtypes([np.object]) 
int_df = str_df.stack().str.decode('utf-8').unstack().astype(float)

# Dropping the features which are not going to be used from the data frame.
int_df.drop(droppedFeatures, axis = 1, inplace = True)
int_df.replace(0,-1,inplace = True)

correlation = {
    "having_IP_Address": int_df["having_IP_Address"].corr(int_df["Result"]),
    "URL_Length": int_df["URL_Length"].corr(int_df["Result"]),
    "Shortining_Service": int_df["Shortining_Service"].corr(int_df["Result"]),
    "having_At_Symbol": int_df["having_At_Symbol"].corr(int_df["Result"]),
    "double_slash_redirecting": int_df["double_slash_redirecting"].corr(int_df["Result"]),
    "Prefix_Suffix": int_df["Prefix_Suffix"].corr(int_df["Result"]),
    "having_Sub_Domain": int_df["having_Sub_Domain"].corr(int_df["Result"]),
    "SSLfinal_State": int_df["SSLfinal_State"].corr(int_df["Result"]),
    "Favicon": int_df["Favicon"].corr(int_df["Result"]),
    "port": int_df["port"].corr(int_df["Result"]),
    "HTTPS_token": int_df["HTTPS_token"].corr(int_df["Result"]),
    "Submitting_to_email": int_df["Submitting_to_email"].corr(int_df["Result"]),
    "Redirect": int_df["Redirect"].corr(int_df["Result"]),
    "age_of_domain": int_df["age_of_domain"].corr(int_df["Result"])
}

# Loading values
x = int_df.values[:,0:30 - len(droppedFeatures)]
y = int_df.values[:,30 - len(droppedFeatures)]

# Adding weights
weigths = [correlation[x] for x in correlation]
for list in x:
    for i in range(len(list)):
        list[i] = float(list[i] * weigths[i])

# Splitting the dataset for training and testing.
x_tr, x_ts, y_tr, y_ts = train_test_split(x,y,test_size=0.20)

# Fitting the training data
model = SVC()
model.fit(x_tr,y_tr)

# Running prediction on the testing set
predict = model.predict(x_ts)

# Saving results
Accuracy = "Accuracy: " + str(accuracy_score(y_ts, predict))
F1_Score = "\nF1 Score: " + str(f1_score(y_ts, predict))
Precision = "\nPrecison: " + str(precision_score(y_ts, predict))
Recall = "\nRecall: " + str(recall_score(y_ts, predict))

text_file = open("../models/weighted_stats.txt", "w")
text_file.write(Accuracy + F1_Score + Precision + Recall)
text_file.close()

# Saving model
pickle.dump(model, open('../models/weighed_final_model.sav','wb'))