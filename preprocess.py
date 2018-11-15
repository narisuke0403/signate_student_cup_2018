import csv
import glob
import os
import numpy as np
import math
import unicodedata
from sklearn.preprocessing import StandardScaler


# ファイル名の更生
path = "./data/*"
path_list = glob.glob(path)
for file in path_list:
    file_rename = file.replace("'", "").replace("'", "")
    os.rename(file,file_rename)

# 訓練データの格納
train_data = []
with open("data/train.csv", "r", encoding="utf-8_sig") as f:
    reader = csv.reader(f)
    header = next(reader)

    for row in reader:
        train_data.append(row)

# テストデータの格納
test_data = []
with open("data/test.csv", "r", encoding="utf-8_sig") as f:
    reader = csv.reader(f)
    header = next(reader)

    for row in reader:
        test_data.append(row)

# 休日データの格納
holiday = []
with open("data/holidays_in_japan.csv", "r", encoding="utf-8_sig") as f:
    reader = csv.reader(f)
    header = next(reader)

    for row in reader:
        holiday.append(row[0])

# スタジアム容量の格納
stadium = {}
with open("data/stadium_capacity_mapping.csv", "r", encoding="utf_8_sig") as f:
    reader = csv.reader(f)
    header = next(reader)

    for row in reader:
        stadium[row[0]] = int(row[1])

def check_day(day, _list):
    year = 

def check_holiday(day,_list):
    if day in holiday:
        _list.append(1)
    else:
        _list.append(0)

def check_class(class_list,class_parts,_list):
    a = class_list.index(class_parts)
    for i in range(len(class_list)):
        if i == a:
            _list.append(1)
        else:
            _list.append(0)
        

def check_stadium(stadium_name,_list):
    a = stadium[stadium_name]
    _list.append(a)

def comparison_class(class_list,class_parts,_list):
    check = True
    for k in class_list:
        if float(class_parts) < k and check:
            _list.append(1)
            check = False
        else:
            _list.append(0)

def crawling():
    # クラス分け
    list_data = np.array(train_data).T
    list_data_test = np.array(test_data).T

    # 日にち
    _day = list_data[1].tolist()
    month = []
    day = []
    for i, k in enumerate(_day):
        month.append(int(k[6:8]))
        day.append(int(k[9:11]))

    # 時間
    _time = list_data[2].tolist()
    for i, k in enumerate(_time):
        _time[i] = int(k[0:2])
    max_time = np.amax(_time)
    min_time = np.amin(_time)
    step = 1 + math.log2(len(_time))
    time_list = np.arange(min_time, max_time, (max_time-min_time)/step)

    # 節
    _section = list_data[3].tolist()
    for i, k in enumerate(_section):
        _section[i] = int(k[1])
    max_section = np.amax(_section)
    min_section = np.amin(_section)
    step = 1 + math.log2(len(_section))
    section_list = np.arange(min_section, max_section,(max_section-min_section)/step)

    # 日
    round_class = np.unique(np.hstack((list_data[4], list_data_test[4])))
    round_list = round_class.tolist()

    # チーム
    _team = list_data[5].tolist()
    _team3 = list_data[6].tolist()
    _team2 = list_data_test[5].tolist()
    _team4 = list_data_test[6].tolist()
    for i, k in enumerate(_team):
        list_data[5][i] = unicodedata.normalize("NFKC", k)
    for i, k in enumerate(_team3):
        list_data[6][i] = unicodedata.normalize("NFKC", k)
    for i, k in enumerate(_team2):
        list_data_test[5][i] = unicodedata.normalize("NFKC", k)
    for i, k in enumerate(_team4):
        list_data_test[6][i] = unicodedata.normalize("NFKC", k)
    all_team = np.hstack((list_data[5], list_data_test[5]))
    team_class = np.unique(all_team)
    team_list = team_class.tolist()

    # 天気
    weather_class = np.unique(np.hstack((list_data[8], list_data_test[8])))
    weather_list = weather_class.tolist()

    # 気温
    temperature_list = list(map(float, list_data[9].tolist()))
    max_temperature = np.amax(temperature_list)
    min_temperature = np.amin(temperature_list)
    step = 1 + math.log2(len(temperature_list))
    temperature_list = np.arange(min_temperature, max_temperature, (max_temperature-min_temperature)/step)

    # 湿度
    humidity_list = list(map(float, list_data[10].tolist()))
    max_humidity = np.amax(humidity_list)
    min_humidity = np.amin(humidity_list)
    step = 1 + math.log2(len(humidity_list))
    humidity_list = np.arange(min_humidity, max_humidity, (max_humidity-min_humidity)/step)

    return time_list, section_list, round_list, team_list, weather_list, temperature_list, humidity_list

time_list, section_list, round_list, team_list, weather_list, temperature_list, humidity_list = crawling()
def get_train_data():
    teacher_list = []
    output_train_data = []
    for i in train_data:
        line = []
        line.append(int(i[0]))
        check_holiday(i[1], line)
        comparison_class(time_list, int(i[2][0:2]), line)
        comparison_class(section_list, int(i[3][1]), line)
        check_class(round_list, i[4], line)
        check_class(team_list, unicodedata.normalize("NFKC", i[5]), line)
        check_class(team_list, unicodedata.normalize("NFKC", i[6]), line)
        check_stadium(i[7], line)
        check_class(weather_list, i[8], line)
        comparison_class(temperature_list, i[9], line)
        comparison_class(humidity_list, i[10], line)
        teacher_list.append(i[-1])
        output_train_data.append(line)

    # 学習データの出力
    with open("data/train_data.csv", "w") as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerows(output_train_data)

    # 教師データの出力
    with open("data/teacher.csv", "w") as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow(teacher_list)

def get_test_data():
    output_test_data = []
    for i in test_data[:459]:
        line = []
        line.append(int(i[0]))
        check_holiday(i[1], line)
        comparison_class(time_list, int(i[2][0:2]), line)
        comparison_class(section_list, int(i[3][1]), line)
        check_class(round_list, i[4], line)
        check_class(team_list, unicodedata.normalize("NFKC", i[5]), line)
        check_class(team_list, unicodedata.normalize("NFKC", i[6]), line)
        check_stadium(i[7], line)
        check_class(weather_list, i[8], line)
        comparison_class(temperature_list, i[9], line)
        comparison_class(humidity_list, i[10], line)
        output_test_data.append(line)
    
    output_future_test_data = []
    for i in test_data[459:]:
        line = []
        line.append(int(i[0]))
        check_holiday(i[1], line)
        comparison_class(time_list, int(i[2][0:2]), line)
        comparison_class(section_list, int(i[3][1]), line)
        check_class(round_list, i[4], line)
        check_class(team_list, unicodedata.normalize("NFKC", i[5]), line)
        check_class(team_list, unicodedata.normalize("NFKC", i[6]), line)
        check_stadium(i[7], line)
        output_future_test_data.append(line)
    
    # テストデータの出力
    with open("data/test_data.csv", "w") as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerows(output_test_data)

    # 未来のテストデータの出力
    with open("data/future_test_data.csv", "w") as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerows(output_future_test_data)

get_train_data()
get_test_data()
