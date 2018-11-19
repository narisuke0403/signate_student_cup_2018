import pandas as pd
from sklearn.model_selection import GridSearchCV, cross_val_score
import xgboost


def get_data():
  return pd.read_csv("data/train_data.csv"), pd.read_csv("data/teacher.csv", header=None)

def full_train():
  train, teacher = get_data()

  # 学習モデル
  mod = xgboost.XGBRegressor()
  
  mod.fit(train, teacher)

  # 交差検証
  scores = cross_val_score(mod, train, teacher, cv=11)
  print('Cross-Validation scores: {}'.format(scores))

  """
  mod_cv = GridSearchCV(mod, {'max_depth': [2,4,6], 'n_estimators': [50,100,200]}, verbose=1)
  scores_cv = cross_val_score(mod_cv, train, teacher)
  print('Cross-Validation scores: {}'.format(scores_cv))
  """

full_train()
