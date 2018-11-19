import pandas as pd

data1 = pd.read_csv("data/train.csv")
teacher = data1["attendance"]

# 無観客試合を除去
data1 = data1.drop(2479)
teacher = teacher.drop(2479)

data1 = data1.drop("attendance",axis=1)
data2 = pd.read_csv("data/test.csv")


def get_holiday():
    holiday_list = pd.read_csv("data/holidays_in_japan.csv")
    return dict(zip(holiday_list["holiday_date"], holiday_list["description"]))

def get_stadium_cap():
    stadium_cap = pd.read_csv("data/stadium_capacity_mapping.csv")
    return dict(zip(stadium_cap["stadium"], stadium_cap["capacity"]))

def get_data():
    data = pd.concat([data1, data2])

    # スタジアムの収容数と日付をカテゴリ変数化
    data["stadium_cap"] = data["venue"]
    data["stadium_cap"] = data["stadium_cap"].replace(get_stadium_cap())
    data = data.replace(get_holiday())
    data = data.replace("(.*)-(.*)-(.*)", "normal day", regex=True)

    # 時間をリスト化
    kick_off_time_list = pd.unique(data["kick_off_time"]).tolist()
    kick_off_time_list.sort()
    result = [kick_off_time_list[0:28],kick_off_time_list[28:76],kick_off_time_list[76:]]
    data.loc[data["kick_off_time"].isin(result[0]), "kick_off_time"] = "noon"
    data.loc[data["kick_off_time"].isin(result[1]), "kick_off_time"] = "evening"
    data.loc[data["kick_off_time"].isin(result[2]), "kick_off_time"] = "night"

    # セクションをリスト化
    section = pd.unique(data["section"]).tolist()
    result = [section[:2], section[2:-2], section[-2:]]
    data.loc[data["section"].isin(result[0]), "section"] = "start"
    data.loc[data["section"].isin(result[1]), "section"] = "playing"
    data.loc[data["section"].isin(result[2]), "section"] = "end"

    # 放送局カラムを削除
    data = data.drop("broadcasters", axis=1)
    
    # sectionとroundを削除
    data = data.drop("round", axis=1)

    # 天気を雨かそれ以外で分割
    data["weather"] = data["weather"].replace("^(?!.*雨).*$", "not rain", regex=True)
    data = data.replace("(.*)雨(.*)", "rain", regex=True)

    # チーム名を正規化
    data["home_team"] = data["home_team"].str.normalize("NFKC")
    data["away_team"] = data["away_team"].str.normalize("NFKC")
    return data

def get_train_data():
    data = get_data()

    # トレーニングデータのみを抽出
    data = data[data["id"] < 18200]

    # idを削除
    data = data.drop("id", axis = 1)
    
    # csvとして出力
    pd.get_dummies(data, drop_first=True).to_csv("data/train_data.csv", index=False)
    teacher.to_csv("data/teacher.csv", index=False)

def get_test_data():
    data = get_data()

    # テストデータのみを抽出
    data = data[data["id"] > 19075]

    # idを削除
    data = data.drop("id", axis = 1)

    # csvとして出力
    pd.get_dummies(data, drop_first=True).to_csv("data/test_data.csv", index=False)

    # 未来のデータと過去のデータに分割

if __name__ == "__main__":
    get_train_data()
    get_test_data()