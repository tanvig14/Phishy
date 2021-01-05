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
    'Links_in_tags','SFH',
    'on_mouseover',
    'RightClick',
    'popUpWidnow',
    'Iframe']

# Loading data and decoding it appropriately.
raw_data = loadarff(open('../data/train.arff','r',encoding='UTF-8'))
df = pd.DataFrame(raw_data[0])
str_df = df.select_dtypes([np.object]) 
int_df = str_df.stack().str.decode('utf-8').unstack().astype(int)
print(int_df)

# Dropping the features which are not going to be used from the data frame.
int_df.drop(droppedFeatures, axis = 1, inplace = True)
int_df.replace(0,-1)

# Loading values
x = int_df.values[:,0:15]
y = int_df.values[:,15]

# Splitting the dataset for training and testing.
x_tr, x_ts, y_tr, y_ts = train_test_split(x,y,test_size=0.20)

# Fitting the training data
model = SVC()
model.fit(x_tr,y_tr)

# Running prediction on the testing set
predict = model.predict(x_ts)

# Printing results
print("Accuracy: ",accuracy_score(y_ts, predict))
print("F1 Score: ",f1_score(y_ts, predict))

# Saving model
pickle.dump(model, open('final_model.sav','wb'))