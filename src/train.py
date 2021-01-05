import numpy as np
import pandas as pd
from scipy.io.arff import loadarff 
from sklearn.model_selection import train_test_split
from sklearn.metrics import *
from sklearn.svm import SVC
import pickle

# Dropping Features that aren't used
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
    'Links_in_tags','SFH',
    'on_mouseover',
    'RightClick',
    'popUpWidnow',
    'Iframe',
    'Domain_registeration_length'
    ]

# Loading data and decoding it appropriately.
raw_data = loadarff(open('../data/data.arff','r',encoding='UTF-8'))
df = pd.DataFrame(raw_data[0])
str_df = df.select_dtypes([np.object]) 
int_df = str_df.stack().str.decode('utf-8').unstack().astype(int)

# Dropping the features which are not going to be used from the data frame.
int_df.drop(droppedFeatures, axis = 1, inplace = True)
int_df.replace(0,-1,inplace = True)

# Loading values
x = int_df.values[:,0:14]
y = int_df.values[:,14]

# Splitting the dataset for training and testing.
x_tr, x_ts, y_tr, y_ts = train_test_split(x,y,test_size=0.30)

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

text_file = open("../models/unweighted_stats.txt", "w")
text_file.write(Accuracy + F1_Score + Precision + Recall)
text_file.close()

# Saving model
pickle.dump(model, open('final_model.sav','wb'))