import csv
import glob
import os
import numpy as np
import math


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




def check_holiday(day):
    if day in holiday:
        return 1
    else:
        return 10


def check_day(day):
    

def check_kick_off_time(time):
    a = int(time[0:2])
    t =  a
    return t


def check_section_or_round(section_or_round):
    a = int(section_or_round[1:2])
    t =  a
    return t

def check_class(class_list,class_parts):
    a = class_list.index(class_parts)
    t =  a
    return t

def check_stadium(stadium_name):
    a = stadium[stadium_name]
    return a

def comparison_class(class_list,class_parts):
    for i,k in enumerate(class_list):
        if float(class_parts) < k:
            t = i
            return t
    return (len(class_list))

def make_data(data):
    # クラス分け
    list_data = np.array(data).T

    # チーム
    team_class = np.unique(list_data[5])
    team_list = team_class.tolist()

    # 天気
    weather_class = np.unique(list_data[8])
    weather_list = weather_class.tolist()

    # 気温
    temperature_list = list(map(float,list_data[9].tolist()))
    max_temperature = np.amax(temperature_list)+1
    min_temperature = np.amin(temperature_list)
    step = 1 + math.log2(len(temperature_list))
    list_temperature = np.arange(min_temperature,max_temperature,(max_temperature-min_temperature)/step)

    # 湿度
    humidity_list = list(map(float,list_data[10].tolist()))
    max_humidity = np.amax(humidity_list)+10
    min_humidity = np.amin(humidity_list)
    step = 1 + math.log2(len(humidity_list))
    list_humidity = np.arange(min_humidity,max_humidity,(max_humidity-min_humidity)/step)
    
    teacher_list = []
    for i in data:
        i[0] = int(i[0])
        i[1] = check_holiday(i[1])
        i[2] = check_kick_off_time(i[2])
        i[3] = check_section_or_round(i[3])
        i[4] = check_section_or_round(i[4])
        i[5] = check_class(team_list,i[5])
        i[6] = check_class(team_list,i[6])
        i[7] = check_stadium(i[7])
        i[8] = check_class(weather_list,i[8])
        i[9] = comparison_class(list_temperature,i[9])
        i[10] = comparison_class(list_humidity,i[10])
        if data == train_data:
            teacher_list.append(int(i.pop(-1)))
        i.pop(-1)

    if data == train_data:
        # 学習データの出力
        with open("data/train_data.csv","w") as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerows(data) # 2次元配列も書き込める
        
        # 教師データの出力
        with open("data/teacher.csv","w") as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow(teacher_list)
    else:
        # テストデータの出力
        with open("data/test_data.csv","w") as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerows(data) # 2次元配列も書き込める

make_data(train_data)
#make_data(test_data)
