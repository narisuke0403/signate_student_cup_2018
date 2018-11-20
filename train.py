import pickle
import pandas as pd
from sklearn.model_selection import GridSearchCV, cross_val_score, KFold
import xgboost


def _get_data():
  return pd.read_csv("data/train_data.csv"), pd.read_csv("data/teacher.csv", header=None)

def full_train():
  train, teacher = _get_data()
  train = train.drop("id" , axis=1)

  # 学習モデル
  mod = xgboost.XGBRegressor()
  
  mod.fit(train, teacher)

  # 交差検証
  scores = cross_val_score(mod, train, teacher, cv=KFold(shuffle=True, random_state=34))
  print('Cross-Validation scores: {}'.format(scores))

  param1 = {
  }
  mod_cv = GridSearchCV(xgboost.XGBRegressor(
    learning_rate = 0.2,
    n_estimators=100,
    min_child_weigh = 3,
    max_depth = 3,
    gamma = 0,
    subsample=0.8,
  ), param1, verbose=1)
  scores_cv = cross_val_score(mod_cv, train, teacher, cv=KFold(shuffle=True, random_state=34))
  mod_cv.fit(train, teacher)
  print(mod_cv.grid_scores_, mod_cv.best_params_, mod_cv.best_score_) 
  print('Cross-Validation scores: {}'.format(scores_cv))
  with open("data/model.pickle", mode="wb") as pk:
    pickle.dump(mod_cv, pk)


if __name__ == "__main__":
  full_train()