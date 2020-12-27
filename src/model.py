import numpy as np
import pandas as pd
from scipy.io.arff import loadarff 

raw_data = loadarff(open('train.arff','r'))
data = pd.DataFrame(raw_data[0])
data["Result"] = str(data["Result"],'utf-8')
print(data)
c1 = data["URL_Length"]
c2 = data["Result"]
print(c1.corr(c2))
