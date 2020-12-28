import numpy as np
import pandas as pd
from scipy.io.arff import loadarff 

raw_data = loadarff(open('../data/train.arff','r',encoding='UTF-8'))
df = pd.DataFrame(raw_data[0])
str_df = df.select_dtypes([np.object]) 
int_df = str_df.stack().str.decode('utf-8').unstack().astype(int)
print(int_df)

