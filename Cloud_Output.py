import csv
import os
from pathlib import Path
import datetime


class Export:

    def __init__(self, path, name):
        self.file_path = path
        self.file_name = name
        self.file_pointer = None

    def input_dict(self, file_list):
        Path(self.file_path).mkdir(parents=True, exist_ok=True)
        self.__open_file()

        column = file_list[0]
        wr = csv.DictWriter(self.file_pointer, fieldnames=column, delimiter='\t')
        wr.writeheader()
        for i in range(1, len(file_list)):
            tmp={}
            for row in range(len(column)):
                tmp[column[row]]=file_list[i][row]
            wr.writerow(tmp)

        self.__close_file()

    def __open_file(self):
        filename = self.file_path + os.sep + self.file_name + datetime.datetime.now().strftime('_%Y%m%d_%H-%M-%S') + ".csv"
        self.file_pointer = open(filename, 'w', newline='', encoding='UTF-16')

    def __close_file(self):
        self.file_pointer.close()


