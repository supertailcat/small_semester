#########################################################
#                                                       #
# 调用csv_to_json函数生成json文件，传参为scv文件的文件名    #
# 直接运行该文件则调用if函数                               #
#                                                       #
#########################################################
import csv
import json


def csv_to_json(filename):
    csv_filename = ""
    csv_file = open(filename, 'r')
    json_file = open('json_file.json', 'w')
    fieldnames = ("DATE", "MAXT", "MINT", "AVGT")
    reader = csv.DictReader(csv_file, fieldnames)
    for row in reader:
        json.dump(row, json_file)
        json_file.write('\n')


if __name__ == "__main__":
    csv_to_json("maxmin.csv")