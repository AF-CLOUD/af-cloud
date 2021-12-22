import csv
import os
import datetime


class CSVExport:

    def __init__(self, name):
        self.file_name = name
        self.file_pointer = None

    def input_dict(self, file_list):
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
        f = self.file_name + datetime.datetime.now().strftime('_%Y%m%d_%H-%M-%S') + ".csv"
        self.file_pointer = open(f, 'w', newline='', encoding='UTF-16')

    def __close_file(self):
        self.file_pointer.close()


