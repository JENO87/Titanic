import pandas as pd
from variables import BasePaths

#https://www.kaggle.com/competitions/titanic/data

train = pd.read_csv(BasePaths.train_path)
test = pd.read_csv(BasePaths.test_path)

print(train.head())
print(test.head())
