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
    json_file.write('{\n\t')
    json_file.write('"data": [\n')
    count = 0;
    for row in reader:
        json_file.write('\t\t')
        json.dump(row, json_file)
        if count < 6 :
            json_file.write(',\n')
        count = count + 1
    json_file.write('\n\t]\n')
    json_file.write('}')


if __name__ == "__main__":
    csv_to_json("maxmin.csv")