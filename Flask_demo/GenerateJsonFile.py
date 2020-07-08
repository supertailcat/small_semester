#########################################################
#                                                       #
# 调用csv_to_json函数生成json文件，传参为scv文件的文件名    #
# 直接运行该文件则调用if函数                               #
#                                                       #
#########################################################
import csv
import json
import os


def csv_to_json(filename, path):
    csv_file = open(path + filename, 'r')
    l = filename.split(".")

    json_file = open("../Forecast/json/" + l[0] + ".json", 'w')
    fieldnames = ("DATE", "MAXT", "MINT", "AVGT")
    reader = csv.DictReader(csv_file, fieldnames)
    json_file.write('[')
    count = 0;
    for row in reader:
        json.dump(row, json_file)
        if count < 6:
            json_file.write(',')
        count = count + 1
    json_file.write(']')


def group_convert(path):
    fileList = os.listdir(path)
    for file in fileList:
        csv_to_json(file, path)


if __name__ == "__main__":
    dir = "../Forecast/csv/"
    group_convert(dir)
