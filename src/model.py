import numpy as np
import pandas as pd
from scipy.io.arff import loadarff 

raw_data = loadarff(open('train.arff','r'))
pd.set_option("display.max_rows", None, "display.max_columns", None)
data = pd.DataFrame(raw_data[1])
print(data)
