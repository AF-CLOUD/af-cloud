from onedrive_collector.explorer import *

class Collector:
    def __init__(self, onedrive_data):
        self.__onedrive = onedrive_data
        self.__total_file_list, self.__file_list, self.__folder_list = self.__onedrive.get_total_file_list()


    def download_file(self, file_num):
        total_file_list, file_list, folder_list  = self.__onedrive.get_total_file_list()
        # 기능 추가 후 포팅 예정

    def show_file_list(self):
        result = list()
        result.append(['file name', 'size(bytes)', 'mimeType', 'createdTime(UTC+9)', 'modifiedTime(UTC+9)', 'file id',
                       'personal?', 'downloadURL'])
        for file in self.__file_list:
            ticks = file['creationDate']
            converted_ticks = datetime.datetime(1, 1, 1, 9) + datetime.timedelta(microseconds=ticks / 10)
            converted_ticks.strftime("%Y-%m-%d %H:%M:%S")
            ticks_modi = file['modifiedDate']
            converted_ticks_modi = datetime.datetime(1, 1, 1, 9) + datetime.timedelta(microseconds=ticks_modi / 10)
            converted_ticks_modi.strftime("%Y-%m-%d %H:%M:%S")
            if file.get('vault') == None:
                result.append([file['name'] + file['extension'], file['size'], file['mimeType'], converted_ticks,
                               converted_ticks_modi,
                               file['id'], 'False', file['urls']['download']])
            else:
                result.append(
                    [file['name'] + file['extension'], file['size'], file['mimeType'], converted_ticks,
                     converted_ticks_modi, file['id'],
                     'True', file['urls']['download']])

        file_count = len(result)
        if file_count == 0:
            PRINTI("No FILE.")
            return None
        PRINTI("\n")

        print("======DRIVE_FILE_LIST======")
        print("FILE_COUNT:" + str(file_count - 1))
        print(tabulate.tabulate(result, headers="firstrow", tablefmt='github', showindex=range(1, file_count),
                                numalign="left"))
