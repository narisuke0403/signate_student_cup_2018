import xgboost
import csv
import pickle
import numpy as np

# モデルの読み込み
mod = pickle.load(open("data/model.pkl","rb"))
mod2 = pickle.load(open("data/model2.pkl", "rb"))


# テストデータの読み込み
test_data = []
with open("data/test_data.csv", "r") as f:
    reader = csv.reader(f)
    for row in reader:
        test_data.append(list(map(int, row)))
X = np.array(test_data)

# 未来のテストデータの読み込み
future_test_data = []
with open("data/future_test_data.csv", "r") as f:
    reader = csv.reader(f)
    for row in reader:
        future_test_data.append(list(map(int, row)))
future_X = np.array(future_test_data)

y_predict = mod.predict(X)
future_y_predict = mod2.predict(future_X)

output = []
for i,n in enumerate(y_predict):
    line = [X[i][0], n]
    output.append(line)

for i,n in enumerate(future_y_predict):
    line = [future_X[i][0], n]
    output.append(line)

with open("data/submit.csv", "w") as f:
    writer = csv.writer(f, lineterminator='\n')
    writer.writerows(output)
