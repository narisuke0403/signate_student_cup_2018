import xgboost
import numpy as np
import csv
import math
import pickle
from sklearn.model_selection import cross_val_score, GridSearchCV

# 訓練データの読み込み
train_data = []
with open("data/train_data.csv", "r") as f:
    reader = csv.reader(f)
    for row in reader:
        train_data.append(list(map(int,row)))
X = np.array(train_data)

# 教師データの読み込み
teacher_data = []
with open("data/teacher.csv", "r") as f:
    reader = csv.reader(f)
    for row in reader:
        teacher_data = list(map(int,row))
y = np.array(teacher_data)


# xgboostの初期化
mod = xgboost.XGBRegressor()
X = np.delete(X,0,1)
# ハイパーパラメータ探索
reg_cv = GridSearchCV(
    mod, {'max_depth': range(10), 'n_estimators': [50, 100, 200]}, verbose=1)
reg_cv.fit(X, y)
mod = xgboost.XGBRegressor(**reg_cv.best_params_)

# 学習

mod.fit(X,y)

# モデルの出力
pickle.dump(mod, open("data/model.pkl","wb"))


# 天気、湿度情報を抜いての学習
_X = X.T[0:93].T
_X = np.delete(_X, 0, 1)

# xgboostの初期化
mod2 = xgboost.XGBRegressor()

# ハイパーパラメータ探索
reg_cv = GridSearchCV(
    mod2, {'max_depth': range(10), 'n_estimators': [50, 100, 200]}, verbose=1)
reg_cv.fit(X, y)
mod2 = xgboost.XGBRegressor(**reg_cv.best_params_)


# 学習
mod2.fit(_X, y)

# モデルの出力
pickle.dump(mod2, open("data/model2.pkl", "wb"))

# 交差検証
scores = cross_val_score(mod, X, y)
scores2 = cross_val_score(mod2, _X, y)
# スコアの平均値
print('Average score: {}'.format(np.mean(scores)))
print('Average score2: {}'.format(np.mean(scores2)))
