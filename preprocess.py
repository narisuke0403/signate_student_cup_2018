import csv
import glob
import os


# ファイル名の更生
path = "./data/*"
list = glob.glob(path)
for file in list:
    file_rename = file.replace("'", "").replace("'", "")
    os.rename(file,file_rename)
print(list)

# 訓練データの格納
data = []
with open("data/train.csv", "r", encoding="utf-8_sig") as f:
    reader = csv.reader(f)
    header = next(reader)

    for row in reader:
        data.append(row)

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


def check_kick_off_time(time):
    return int(time[0:2],2)


def check_section_or_round(section_or_round):
    return int(section_or_round[1:3],2)


def make_data():
    for i in data:
        i[0] = int(i[0])
        i[1] = check_holiday(i[1])
        i[2] = check_kick_off_time(i[2])
        i[3] = check_section_or_round(i[3])
        i[4] = check_section_or_round(i[4])

    print(data)


make_data()
