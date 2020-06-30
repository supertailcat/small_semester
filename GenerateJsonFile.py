#########################################################
#                                                       #
# 调用该类生成json文件，直接调用构造器，传参为scv文件文件名  #
#                                                       #
#########################################################
import csv
import json


class GenerateJsonFile:
    csv_filename = ""

    def __init__(self, filename):
        csv_file = open(filename, 'r')
        json_file = open('json_file.json', 'w')
        fieldnames = ("DATE", "MAXT", "MINT", "AVGT")
        reader = csv.DictReader(csv_file, fieldnames)
        for row in reader:
            json.dump(row, json_file)
            json_file.write('\n')


# gjf = GenerateJsonFile("maxmin.csv")