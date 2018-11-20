import pickle
import numpy as np
import xgboost
import pandas as pd


def get_data():
    # テストデータの読み込み
    data = pd.read_csv("data/test_data.csv")

    # 過去と未来で分割
    past_test_data = data[:459]
    future_test_data = data[459:]
    return data, past_test_data, future_test_data


def past_predict():
    data,_,_ = get_data()

    # idの抽出
    id = data["id"].values
    data = data.drop("id", axis=1)

    # modelの読み込み
    mod = pickle.load(open("data/model.pickle","rb"))
    y = mod.predict(data)

    result = np.c_[id, y]
    np.savetxt("data/submit.csv", result, delimiter=',', fmt="%.5f")

"""
def future_predict():
    # modelの読み込み
    mod = pickle.load(open("data/model_light.pickle","rb"))

    y = mod.predict(future_test_data)
    return y
"""

if __name__ == "__main__":
    past_predict()
    # future_predict()