import csv
import os
import time


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
        f = 'export/' + self.file_name + str(time.time()) + ".csv"
        filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), f)
        self.file_pointer = open(filename, 'w', newline='', encoding='UTF-16')

    def __close_file(self):
        self.file_pointer.close()


