import xgboost
import numpy as np
import csv
import math

# 訓練データの読み込み
train_data = []
with open("data/train_data.csv", "r") as f:
    reader = csv.reader(f)
    for row in reader:
        train_data.append(list(map(int,row)))
X = np.array(train_data)
print(X)

# 教師データの読み込み
teacher_data = []
with open("data/teacher.csv", "r") as f:
    reader = csv.reader(f)
    for row in reader:
        teacher_data = list(map(int,row))
y = np.array(teacher_data)

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.33)

mod = xgboost.XGBRegressor()
mod.fit(X_train,y_train)
y_train_pred = mod.predict(X_test)
a = 0
for i in range(len(y_test)):
    a += (math.log(y_test[i]+1)-math.log(y_train_pred[i]+1))**2
score = math.sqrt(a)/len(y)
from sklearn.metrics import r2_score
print('xgboost  score_test: {}'.format(score))
