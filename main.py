import numpy as np
import pandas as pd

data_csv = pd.read_csv('data.csv')
data = pd.DataFrame(data_csv)

print(data)
