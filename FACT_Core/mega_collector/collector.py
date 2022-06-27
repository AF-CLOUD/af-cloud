"""
============================================
    "collector" Module
============================================
.. moduleauthor:: Siyoon Kim <kim_3738@korea.ac.kr>

.. note::
    'TITLE'             : MEGA - Authenticator and Explorer in AF-Forensics\n
    'AUTHOR'            : Siyoon Kim\n
    'TEAM'              : DFRC\n
    'VERSION'           : 0.0.3\n
    'RELEASE-DATE'      : 2022-06-17\n

--------------------------------------------

Description
===========

    MEGA Cloud 에 대해서 원하는 기능을 제공 하는 모듈

    도구이름    : Forensics Acquisition & Criminal investigation Tool(FACT)\n
    프로젝트    : 안티-포렌식 기술 대응을 위한 데이터 획득 및 분석 기술 연구\n
    연구기관    : 고려대학교(Korea Univ.)\n
    지원기관    : 경찰청, 과학기술정보통신부

History
===========

    * 2022-05-20 : 초기 버전
    * 2022-06-15 : 다운로드 기능 추가
    * 2022-06-17 : 다운로드 파일 이름 수정 추가

"""

from mega_collector.authenticator_with_explorer import *

class Collector:
    def __init__(self, auth_data):
        self.__mega_data = auth_data
        self.__raw_file_list = self.__mega_data.get_file_list()
        self.__real_file_list = []
        self.__file_n = ['']
        self.__m = self.__mega_data.get_m()
        self.__set_file_list()


    def show_file_list(self):
        new_list = list()

        for f in self.__real_file_list:
            if len(f[1]) >= 20:
                tmp = f[1]
                f[1] = f[1][:20] + '....'
                new_list.append((f[:7]))
                f[1] = tmp
            else:
                new_list.append((f[:7]))

        file_count = len(self.__real_file_list)
        print()
        print("======DRIVE_FILE_LIST======")
        print("FILE_COUNT:", file_count - 1)
        print(tabulate.tabulate(new_list, headers="firstrow", tablefmt='github', showindex=range(1, file_count),
                                numalign="left"))


    def __set_file_list(self):
        self.__real_file_list.append(['Id', 'Name', 'Size', 'Type', 'Is_Trashed', 'Added Time', 'Path'])
        for key1, value1 in self.__raw_file_list.items():
            id = ''
            name = ''
            size = 0
            type = ''
            is_trashed = False
            add_time = 0
            path = ''
            for key2, value2 in value1.items():
                try:
                    if key2 == 'a':
                        for key3, value3 in value2.items():
                            if key3 == 'n':
                                self.__file_n.append(value3)
                                name = value3.encode().decode('utf-8').encode('latin1').decode('utf-8')
                            elif key3 == 'rr':
                                is_trashed = True
                    elif key2 == 'h':
                        id = value2
                    elif key2 == 'p':
                        path = value2
                    elif key2 == 's':
                        size = value2
                    elif key2 == 't':
                        if value2 == 0:
                            type = 'File'
                        elif value2 == 1:
                            type = 'Folder'
                        elif value2 == 2:
                            type = 'Cloud Drive'
                        elif value2 == 3:
                            type = 'Inbox'
                        elif value2 == 4:
                            type = 'Rubbish Bin'
                    elif key2 == 'ts':
                        add_time = datetime.datetime.fromtimestamp(value2)
                except Exception as e:
                    continue

            self.__real_file_list.append([id, name, size, type, is_trashed, add_time, path])
            if name == '':
                self.__file_n.append(name)


        flag = 0
        for i in self.__real_file_list:
            if flag == 0:
                i[6] = 'Path'
                flag = 1
            else:
                path = i[6]
                parent_path = ' '
                for j in self.__real_file_list:
                    if path == j[0]:
                        parent_path = j[1]
                i[6] = parent_path

        for i in self.__real_file_list:
            for j in self.__real_file_list:
                if i[6] == j[1]:
                    i[6] = j[6] + '\\' + i[6]

        for i in self.__real_file_list:
            if '\\Rubbish Bin' in i[6]:
                i[4] = True
            if i[6] == ' ':
                i[6] = '\\'

        if len(self.__real_file_list) == 0:
            return FC_ERROR
        return FC_OK


    def get_num_of_file_list(self):
        return len(self.__real_file_list)


    def download_file(self, download_number):
        file_name = self.__file_n[download_number]
        self.__m = self.__mega_data.get_m()
        file = self.__m.find(file_name)

        if not (os.path.isdir('./download')):
            os.makedirs('./download')

        try:
            self.__m.download(file, './download')
        except:
            pass

        try:
            os.rename('./download/' + file_name, './download/' + self.__real_file_list[download_number][1])
        except:
            pass


    def search_file(self, q):
        search_result = []
        search_result.append(['Id', 'Name', 'Size', 'Type', 'Is_Trashed', 'Added Time', 'Path'])
        search_response = self.__real_file_list

        if len(search_response) == 0:
            print("No Items.")
        else:
            for child in search_response:
                if q in child[1]:
                    search_result.append(child)

        self.show_file_list_local(search_result)


    def search_file_by_date(self, start, end):
        search_result = []
        search_result.append(['Id', 'Name', 'Size', 'Type', 'Is_Trashed', 'Added Time', 'Path'])
        s_time = datetime.datetime.strptime(start, "%Y-%m-%d")
        e_time = datetime.datetime.strptime(end, "%Y-%m-%d")
        search_response = self.__real_file_list

        for file in search_response:
            if file == search_response[0]:
                continue
            a_time = file[5]
            if s_time <= a_time and a_time <= e_time:
                search_result.append(file)
                continue

        return self.show_file_list_local(search_result)


    @staticmethod
    def show_file_list_local(file_list):
        result = list()

        for f in file_list:
            if len(f[1]) >= 20:
                tmp = f[1]
                f[1] = f[1][:20] + '....'
                result.append((f[:7]))
                f[1] = tmp
            else:
                result.append((f[:7]))

        file_count = len(file_list)
        print()
        print("======DRIVE_FILE_LIST======")
        print("FILE_COUNT:", file_count - 1)
        print(tabulate.tabulate(result, headers="firstrow", tablefmt='github', showindex=range(1, file_count),
                                numalign="left"))